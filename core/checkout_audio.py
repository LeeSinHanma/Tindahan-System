"""Optional checkout audio selected by the user and kept outside the repository."""

import io
import re
import sqlite3
import threading
import uuid
from contextlib import closing
from pathlib import Path

from core.app_paths import user_data_directory
from db import database

SUPPORTED_EXTENSIONS = {".wav", ".ogg", ".mp3"}
MAX_FILE_BYTES = 10 * 1024 * 1024
_mixer_lock = threading.Lock()
_playing_sound = None


class AudioError(ValueError):
    """A file or audio device could not be used."""


def _managed_path(filename: str) -> Path | None:
    if not re.fullmatch(r"checkout-[0-9a-f]{32}\.(wav|ogg|mp3)", filename):
        return None
    return user_data_directory() / "sounds" / filename


def sound_info() -> dict:
    with closing(database.get_connection()) as connection:
        settings = dict(
            connection.execute(
                "SELECT key, value FROM settings WHERE key IN ('checkout_sound_file', 'checkout_sound_name', 'checkout_sound_enabled')"
            ).fetchall()
        )
    path = _managed_path(settings.get("checkout_sound_file", ""))
    available = path is not None and path.is_file()
    return {
        "name": settings.get("checkout_sound_name", ""),
        "path": path,
        "available": available,
        "enabled": settings.get("checkout_sound_enabled") == "1" and available,
    }


def _read_audio(path: Path) -> bytes:
    try:
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise AudioError("Choose a WAV, OGG, or MP3 audio file.")
        with path.open("rb") as source:
            payload = source.read(MAX_FILE_BYTES + 1)
    except OSError as exc:
        raise AudioError(
            "The sound file could not be opened. Choose it again."
        ) from exc
    if not payload or len(payload) > MAX_FILE_BYTES:
        raise AudioError("Choose a non-empty sound file smaller than 10 MB.")
    return payload


def _load_sound(payload: bytes):
    # All callers hold _mixer_lock; initialization and playback cannot race.
    try:
        import pygame

        if not pygame.mixer.get_init():
            pygame.mixer.init()
        sound = pygame.mixer.Sound(file=io.BytesIO(payload))
        if sound.get_length() <= 0:
            raise AudioError("The sound file contains no playable audio.")
        return pygame.mixer, sound
    except (ImportError, RuntimeError) as exc:
        raise AudioError("Audio is unavailable on this device.") from exc
    except Exception as exc:
        if isinstance(exc, AudioError):
            raise
        raise AudioError(
            "The file could not be played. Check your audio device or choose another WAV, OGG, or MP3 file."
        ) from exc


def choose_sound(source: str | Path) -> None:
    source = Path(source)
    payload = _read_audio(source)
    with _mixer_lock:
        _load_sound(payload)
    previous = sound_info()["path"]
    filename = f"checkout-{uuid.uuid4().hex}{source.suffix.lower()}"
    destination = _managed_path(filename)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("xb") as output:
            output.write(payload)
        with closing(database.get_connection()) as connection, connection:
            connection.executemany(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                [
                    ("checkout_sound_file", filename),
                    ("checkout_sound_name", source.name),
                    ("checkout_sound_enabled", "1"),
                ],
            )
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    if previous is not None:
        try:
            previous.unlink(missing_ok=True)
        except OSError:
            pass


def set_enabled(enabled: bool) -> None:
    if enabled and not sound_info()["available"]:
        raise AudioError("Choose a sound file first.")
    database.set_setting("checkout_sound_enabled", int(enabled))
    if not enabled:
        stop_playback()


def stop_playback() -> None:
    global _playing_sound
    with _mixer_lock:
        try:
            import pygame

            if pygame.mixer.get_init():
                pygame.mixer.stop()
        except (ImportError, RuntimeError):
            pass
        _playing_sound = None


def remove_sound() -> None:
    previous = sound_info()["path"]
    with closing(database.get_connection()) as connection, connection:
        connection.execute(
            "DELETE FROM settings WHERE key IN ('checkout_sound_file', 'checkout_sound_name', 'checkout_sound_enabled')"
        )
    stop_playback()
    if previous is not None:
        try:
            previous.unlink(missing_ok=True)
        except OSError:
            pass


def preview_sound() -> None:
    info = sound_info()
    if not info["available"]:
        raise AudioError("Choose a sound file first.")
    _play(info["path"])


def _play(path: Path, *, checkout: bool = False) -> None:
    global _playing_sound
    payload = _read_audio(path)
    with _mixer_lock:
        if checkout:
            current = sound_info()
            if not current["enabled"] or current["path"] != path:
                return
        mixer, sound = _load_sound(payload)
        mixer.stop()
        if sound.play() is None:
            raise AudioError("No audio channel is available. Try again.")
        _playing_sound = sound


def play_checkout_sound() -> threading.Thread | None:
    try:
        info = sound_info()
    except sqlite3.Error:
        return None
    if not info["enabled"]:
        return None

    def play():
        try:
            _play(info["path"], checkout=True)
        except (AudioError, OSError, sqlite3.Error):
            # A completed sale must remain successful if the device or file disappears.
            pass

    worker = threading.Thread(target=play, daemon=True, name="checkout-audio")
    worker.start()
    return worker
