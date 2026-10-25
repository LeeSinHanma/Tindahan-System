"""Writable storage for installed apps, separate from bundled resources."""

import os
import sqlite3
import sys
import tempfile
from contextlib import closing
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]


def database_path() -> Path:
    override = os.environ.get("TINDAHAN_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve() / "pos.db"
    if not getattr(sys, "frozen", False):
        return PROJECT_DIR / "pos.db"
    return user_data_directory() / "pos.db"


def user_data_directory() -> Path:
    """Local app files stay outside the source checkout and installed program."""
    override = os.environ.get("TINDAHAN_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData/Local")
        return base / "TindahanSystem"
    base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    if not base.is_absolute():
        base = Path.home() / ".local/share"
    return base / "tindahan-system"


def legacy_database_path() -> Path | None:
    if getattr(sys, "frozen", False) and not os.environ.get("TINDAHAN_DATA_DIR"):
        return Path(sys.executable).resolve().parent / "pos.db"
    return None


def prepare_database(destination: Path, legacy: Path | None = None) -> None:
    """Copy an old executable-adjacent database once, including committed WAL data.

    Leave the original intact. Publish a complete backup without overwriting an
    existing destination, including when two app instances start together.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or legacy is None or not legacy.is_file():
        return
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".pos-migration-", suffix=".db", dir=destination.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with closing(
            sqlite3.connect(legacy.resolve().as_uri() + "?mode=ro", uri=True)
        ) as source:
            with closing(sqlite3.connect(temporary)) as target:
                source.backup(target)
                if target.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                    raise sqlite3.DatabaseError(
                        "The old database failed its integrity check"
                    )
        try:
            os.link(temporary, destination)
        except FileExistsError:
            pass
    finally:
        temporary.unlink(missing_ok=True)
