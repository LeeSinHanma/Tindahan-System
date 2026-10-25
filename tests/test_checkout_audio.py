"""Local audio import, persistence, and failure isolation from checkout."""

import os
import sqlite3
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from core import checkout_audio
from db import database


def write_tone(path):
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(22050)
        output.writeframes(b"\x00\x00\x10\x00" * 2205)


class CheckoutAudioTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="tindahan-audio-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        for patcher in (
            patch.object(database, "DB_FILE", self.directory / "pos.db"),
            patch.object(
                checkout_audio,
                "user_data_directory",
                return_value=self.directory / "user data",
            ),
            patch.dict(
                os.environ,
                {"SDL_AUDIODRIVER": "dummy", "PYGAME_HIDE_SUPPORT_PROMPT": "1"},
            ),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.connections = []
        original_connect = sqlite3.connect

        def connect(*args, **kwargs):
            connection = original_connect(*args, **kwargs)
            self.connections.append(connection)
            return connection

        patcher = patch.object(database.sqlite3, "connect", side_effect=connect)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.close_connections)
        self.addCleanup(checkout_audio.stop_playback)
        database.init_database()
        self.source = self.directory / "my kaching.wav"
        write_tone(self.source)

    def close_connections(self):
        for connection in self.connections:
            try:
                connection.close()
            except sqlite3.ProgrammingError:
                # Worker-thread connections have already closed in their own context.
                pass

    def test_fresh_install_is_silent_without_starting_audio(self):
        with patch.object(checkout_audio, "_load_sound") as load:
            self.assertIsNone(checkout_audio.play_checkout_sound())
            load.assert_not_called()
        self.assertFalse(checkout_audio.sound_info()["enabled"])
        with self.assertRaises(checkout_audio.AudioError):
            checkout_audio.set_enabled(True)

    def test_imported_copy_survives_moving_original_and_restarting_database(self):
        checkout_audio.choose_sound(self.source)
        info = checkout_audio.sound_info()
        self.assertTrue(info["enabled"])
        self.assertEqual(info["name"], self.source.name)
        self.assertEqual(info["path"].read_bytes(), self.source.read_bytes())
        self.assertNotEqual(info["path"], self.source)
        self.source.unlink()
        database.init_database()
        self.assertEqual(checkout_audio.sound_info()["path"], info["path"])
        checkout_audio.preview_sound()
        worker = checkout_audio.play_checkout_sound()
        self.assertIsNotNone(worker)
        worker.join(timeout=5)
        self.assertFalse(worker.is_alive())

    def test_mute_keeps_selection_and_remove_keeps_original(self):
        checkout_audio.choose_sound(self.source)
        path = checkout_audio.sound_info()["path"]
        checkout_audio.set_enabled(False)
        self.assertIsNone(checkout_audio.play_checkout_sound())
        self.assertTrue(path.is_file())
        checkout_audio.preview_sound()
        checkout_audio.set_enabled(True)
        checkout_audio.remove_sound()
        self.assertFalse(path.exists())
        self.assertTrue(self.source.is_file())
        self.assertIsNone(checkout_audio.sound_info()["path"])
        self.assertIsNone(checkout_audio.play_checkout_sound())

    def test_replacement_removes_only_previous_managed_copy(self):
        checkout_audio.choose_sound(self.source)
        previous = checkout_audio.sound_info()["path"]
        other = self.directory / "replacement.WAV"
        write_tone(other)
        checkout_audio.choose_sound(other)
        self.assertFalse(previous.exists())
        self.assertTrue(self.source.exists())
        self.assertTrue(other.exists())
        self.assertEqual(checkout_audio.sound_info()["name"], other.name)

    def test_invalid_or_missing_audio_preserves_previous_selection(self):
        checkout_audio.choose_sound(self.source)
        previous = checkout_audio.sound_info()
        invalid = self.directory / "broken.mp3"
        invalid.write_bytes(b"this is not audio")
        for path in (
            invalid,
            self.directory / "missing.wav",
            self.directory / "document.txt",
        ):
            with self.subTest(path=path), self.assertRaises(checkout_audio.AudioError):
                checkout_audio.choose_sound(path)
            self.assertEqual(checkout_audio.sound_info(), previous)

    def test_empty_and_oversized_files_are_rejected(self):
        empty = self.directory / "empty.wav"
        empty.touch()
        with self.assertRaises(checkout_audio.AudioError):
            checkout_audio.choose_sound(empty)
        with patch.object(checkout_audio, "MAX_FILE_BYTES", 32):
            with self.assertRaises(checkout_audio.AudioError):
                checkout_audio.choose_sound(self.source)
        self.assertFalse(checkout_audio.sound_info()["available"])

    def test_missing_managed_file_makes_checkout_silent(self):
        checkout_audio.choose_sound(self.source)
        checkout_audio.sound_info()["path"].unlink()
        self.assertIsNone(checkout_audio.play_checkout_sound())
        self.assertFalse(checkout_audio.sound_info()["enabled"])
        with self.assertRaises(checkout_audio.AudioError):
            checkout_audio.preview_sound()

    def test_bad_saved_path_cannot_preview_or_remove_unrelated_file(self):
        database.set_setting("checkout_sound_file", str(self.source))
        database.set_setting("checkout_sound_enabled", "1")
        self.assertIsNone(checkout_audio.play_checkout_sound())
        checkout_audio.remove_sound()
        self.assertTrue(self.source.exists())

    def test_settings_failure_does_not_leave_imported_file(self):
        checkout_audio.choose_sound(self.source)
        previous = checkout_audio.sound_info()["path"]
        original_connect = database.get_connection
        calls = 0

        def fail_save():
            nonlocal calls
            calls += 1
            if calls > 1:
                raise sqlite3.OperationalError("test failed write")
            return original_connect()

        with patch.object(database, "get_connection", side_effect=fail_save):
            with self.assertRaises(sqlite3.OperationalError):
                checkout_audio.choose_sound(self.source)
        self.assertEqual(list(previous.parent.iterdir()), [previous])
        self.assertEqual(checkout_audio.sound_info()["path"], previous)

    def test_playback_error_is_contained_in_worker(self):
        checkout_audio.choose_sound(self.source)
        with patch.object(
            checkout_audio,
            "_play",
            side_effect=checkout_audio.AudioError("device gone"),
        ):
            worker = checkout_audio.play_checkout_sound()
            worker.join(timeout=5)
        self.assertFalse(worker.is_alive())


if __name__ == "__main__":
    unittest.main()
