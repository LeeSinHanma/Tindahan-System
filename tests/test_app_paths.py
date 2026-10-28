"""Installed database locations and lossless migration of existing shop records."""

import os
import sqlite3
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from core import app_paths


class AppPathTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_source_keeps_existing_project_database(self):
        with patch.object(sys, "frozen", False, create=True):
            self.assertEqual(
                app_paths.database_path(), app_paths.PROJECT_DIR / "pos.db"
            )
            self.assertIsNone(app_paths.legacy_database_path())

    def test_windows_installed_location(self):
        with (
            patch.object(sys, "frozen", True, create=True),
            patch.object(sys, "platform", "win32"),
        ):
            os.environ["LOCALAPPDATA"] = str(self.directory / "Local")
            self.assertEqual(
                app_paths.database_path(),
                self.directory / "Local/TindahanSystem/pos.db",
            )

    def test_linux_installed_location(self):
        with (
            patch.object(sys, "frozen", True, create=True),
            patch.object(sys, "platform", "linux"),
        ):
            os.environ["XDG_DATA_HOME"] = str(self.directory / "data")
            self.assertEqual(
                app_paths.database_path(),
                self.directory / "data/tindahan-system/pos.db",
            )

    def test_linux_falls_back_for_missing_or_relative_xdg_directory(self):
        with (
            patch.object(sys, "frozen", True, create=True),
            patch.object(sys, "platform", "linux"),
            patch.object(Path, "home", return_value=self.directory),
        ):
            for value in ("", "relative-folder"):
                os.environ["XDG_DATA_HOME"] = value
                self.assertEqual(
                    app_paths.database_path(),
                    self.directory / ".local/share/tindahan-system/pos.db",
                )

    def test_explicit_directory_disables_automatic_migration(self):
        with patch.object(sys, "frozen", True, create=True):
            os.environ["TINDAHAN_DATA_DIR"] = str(self.directory)
            self.assertEqual(app_paths.database_path(), self.directory / "pos.db")
            self.assertIsNone(app_paths.legacy_database_path())

    def test_selected_database_file_overrides_directory_for_source_and_installed_apps(self):
        selected = self.directory / "My Store/custom-name.sqlite3"
        os.environ["TINDAHAN_DB_FILE"] = str(selected)
        os.environ["TINDAHAN_DATA_DIR"] = str(self.directory / "sounds-data")
        for frozen in (False, True):
            with self.subTest(frozen=frozen), patch.object(sys, "frozen", frozen, create=True):
                self.assertEqual(app_paths.database_path(), selected)
                self.assertIsNone(app_paths.legacy_database_path())
                self.assertEqual(app_paths.user_data_directory(), self.directory / "sounds-data")

    def test_legacy_path_uses_executable_directory(self):
        with (
            patch.object(sys, "frozen", True, create=True),
            patch.object(sys, "executable", str(self.directory / "POS-System")),
        ):
            self.assertEqual(
                app_paths.legacy_database_path(), self.directory / "pos.db"
            )

    def test_new_install_prepares_directory_without_creating_database(self):
        destination = self.directory / "data/pos.db"
        app_paths.prepare_database(destination)
        self.assertTrue(destination.parent.is_dir())
        self.assertFalse(destination.exists())

    def make_legacy(self):
        legacy = self.directory / "old.db"
        connection = sqlite3.connect(legacy)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("CREATE TABLE records (value TEXT)")
        connection.execute("INSERT INTO records VALUES ('shop data')")
        connection.commit()
        self.addCleanup(connection.close)
        return legacy

    def test_migration_includes_wal_and_preserves_original(self):
        legacy = self.make_legacy()
        self.assertTrue(Path(str(legacy) + "-wal").exists())
        destination = self.directory / "new/pos.db"
        app_paths.prepare_database(destination, legacy)
        with closing(sqlite3.connect(destination)) as connection:
            self.assertEqual(
                connection.execute("SELECT value FROM records").fetchone(),
                ("shop data",),
            )
        self.assertTrue(legacy.exists())
        self.assertEqual(list(destination.parent.glob(".pos-migration-*")), [])

    def test_existing_destination_is_never_replaced(self):
        destination = self.directory / "pos.db"
        destination.write_bytes(b"existing records")
        app_paths.prepare_database(destination, self.make_legacy())
        self.assertEqual(destination.read_bytes(), b"existing records")

    def test_corrupt_legacy_leaves_no_partial_destination(self):
        legacy = self.directory / "old.db"
        legacy.write_bytes(b"not a sqlite database")
        destination = self.directory / "new/pos.db"
        with self.assertRaises(sqlite3.DatabaseError):
            app_paths.prepare_database(destination, legacy)
        self.assertFalse(destination.exists())
        self.assertEqual(list(destination.parent.iterdir()), [])

    def test_concurrent_migrations_publish_one_complete_database(self):
        legacy = self.make_legacy()
        destination = self.directory / "new/pos.db"
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(
                pool.map(
                    lambda _: app_paths.prepare_database(destination, legacy), range(2)
                )
            )
        with closing(sqlite3.connect(destination)) as connection:
            self.assertEqual(
                connection.execute("PRAGMA quick_check").fetchone(), ("ok",)
            )
            self.assertEqual(
                connection.execute("SELECT COUNT(*) FROM records").fetchone(), (1,)
            )
        self.assertEqual(list(destination.parent.glob(".pos-migration-*")), [])


if __name__ == "__main__":
    unittest.main()
