"""Source desktop installs work without the checkout and preserve store records."""

import json
import os
import shlex
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core import app_paths  # Load the real migration helper before using a fixture checkout.
from db import database
from scripts import install_linux


@unittest.skipUnless(sys.platform.startswith("linux"), "Linux desktop installer")
class SourceInstallerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.home = self.directory / 'Home with spaces $cash `tick` %rate "quote"'
        self.root = self.directory / "checkout"
        self.root.mkdir()
        for filename in ("requirements.txt", "LICENSE", "THIRD_PARTY_NOTICES.md"):
            (self.root / filename).write_text("test")
        (self.root / "main.py").write_text(
            "import json, os, sys\n"
            "print(json.dumps([os.environ['TINDAHAN_DATA_DIR'], os.environ['TINDAHAN_DB_FILE'], sys.argv[1:]]))\n"
        )
        for directory in ("core", "db", "ui", "scripts", "packaging/third_party"):
            (self.root / directory).mkdir(parents=True)
        (self.root / "scripts/install_linux.py").write_text("# installer")
        (self.root / "packaging/third_party/SOURCE_CODE.md").write_text("source")
        self.target = self.home / ".local/opt" / install_linux.INSTALL_NAME
        self.data = self.home / ".local/share/tindahan-system/pos.db"
        self.connections = []
        connect = sqlite3.connect

        def track_connection(*args, **kwargs):
            connection = connect(*args, **kwargs)
            self.connections.append(connection)
            return connection

        for context in (
            patch.object(Path, "home", return_value=self.home),
            patch.object(install_linux, "ROOT", self.root),
            patch.dict(os.environ, {}, clear=True),
            patch.object(sys, "path", sys.path.copy()),
            patch.object(install_linux.shutil, "which", return_value=None),
            patch.object(install_linux.subprocess, "run", side_effect=self.dependencies),
            patch.object(install_linux, "choose_database", return_value=(self.data, True)),
            patch.object(sqlite3, "connect", side_effect=track_connection),
        ):
            context.start()
            self.addCleanup(context.stop)
        self.addCleanup(self.close_connections)

    def close_connections(self):
        for connection in self.connections:
            connection.close()

    def dependencies(self, command, **kwargs):
        if command[1:3] == ["-m", "venv"]:
            python = Path(command[3]) / "bin/python"
            python.parent.mkdir(parents=True)
            python.write_text(f"#!/bin/sh\nexec {shlex.quote(sys.executable)} \"$@\"\n")
            python.chmod(0o755)
        else:
            self.assertEqual(command[1:4], ["-m", "pip", "install"])

    def test_launcher_runs_after_checkout_removed_with_special_paths(self):
        install_linux.install()
        self.root.rename(self.directory / "moved-checkout")
        # Bypass the dependency-install stub to execute the generated launcher.
        process = subprocess.Popen(
            [str(self.target / "Tindahan-System"), "argument with spaces"],
            cwd=self.directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        result, errors = process.communicate(timeout=10)
        self.assertEqual(process.returncode, 0, errors)
        self.assertEqual(json.loads(result), [str(self.data.parent), str(self.data), ["argument with spaces"]])
        entry = self.home / ".local/share/applications/tindahan-system-source.desktop"
        contents = entry.read_text()
        self.assertIn("Terminal=false\n", contents)
        self.assertIn("%%rate", contents)
        self.assertIn('\\\\"quote\\\\"', contents)
        self.assertTrue(os.access(self.target / "Tindahan-System", os.X_OK))

    def make_store(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with patch.object(database, "DB_FILE", path):
            database.init_database()

    def test_selected_database_keeps_wal_records_updates_and_uninstall_preserve_it(self):
        selected = self.directory / "Existing Store/my-store.sqlite3"
        self.make_store(selected)
        connection = sqlite3.connect(selected)
        self.addCleanup(connection.close)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("CREATE TABLE records (value TEXT)")
        connection.execute("INSERT INTO records VALUES ('original')")
        connection.commit()
        install_linux.install(database_file=selected)
        self.assertFalse(self.data.exists())
        with sqlite3.connect(selected) as installed:
            self.assertEqual(installed.execute("SELECT value FROM records").fetchone(), ("original",))
            installed.execute("UPDATE records SET value = 'new sale'")
        with patch.object(install_linux, "choose_database", return_value=(selected, False)) as chooser:
            install_linux.install()
        chooser.assert_called_once_with(selected)
        with sqlite3.connect(selected) as installed:
            self.assertEqual(installed.execute("SELECT value FROM records").fetchone(), ("new sale",))
        sound = self.data.parent / "sounds/checkout.wav"
        sound.parent.mkdir(parents=True)
        sound.write_bytes(b"selected audio")
        install_linux.uninstall()
        self.assertFalse(self.target.exists())
        self.assertTrue(selected.is_file())
        self.assertTrue(sound.is_file())
        self.assertFalse((self.home / ".local/share/applications/tindahan-system-source.desktop").exists())

    def test_unrecognized_installation_is_not_modified(self):
        self.target.mkdir(parents=True)
        existing = self.target / "keep.txt"
        existing.write_text("keep")
        with self.assertRaisesRegex(RuntimeError, "unrecognized"):
            install_linux.install()
        with self.assertRaisesRegex(RuntimeError, "No recognized"):
            install_linux.uninstall()
        self.assertEqual(existing.read_text(), "keep")

    def test_cancel_does_not_create_installation_or_database(self):
        with patch.object(install_linux, "choose_database", return_value=None):
            install_linux.install()
        self.assertFalse(self.target.exists())
        self.assertFalse(self.data.exists())

    def test_new_store_does_not_overwrite_existing_database(self):
        self.make_store(self.data)
        original = self.data.read_bytes()
        with self.assertRaisesRegex(ValueError, "already exists"):
            install_linux.install(database_file=self.data, create_new=True)
        self.assertEqual(self.data.read_bytes(), original)
        self.assertFalse(self.target.exists())

    def test_invalid_database_does_not_install_or_change_the_file(self):
        selected = self.directory / "invalid.db"
        selected.write_bytes(b"not a database")
        with self.assertRaisesRegex(ValueError, "not a readable"):
            install_linux.install(database_file=selected)
        self.assertEqual(selected.read_bytes(), b"not a database")
        self.assertFalse(self.target.exists())

    def test_switching_database_keeps_original_database_and_accounts(self):
        install_linux.install()
        selected = self.directory / "other-store.db"
        self.make_store(selected)
        with sqlite3.connect(selected) as connection:
            connection.execute("INSERT INTO settings (key, value) VALUES ('store_marker', 'other store')")
        original = self.data.read_bytes()
        install_linux.install(database_file=selected)
        self.assertEqual(self.data.read_bytes(), original)
        self.assertEqual(json.loads((self.target / "store-database.json").read_text())["database"], str(selected))
        self.assertIn(shlex.quote(str(selected)), (self.target / "Tindahan-System").read_text())
        with sqlite3.connect(selected) as connection:
            self.assertEqual(connection.execute("SELECT value FROM settings WHERE key='store_marker'").fetchone(), ("other store",))

    def test_database_inside_application_directory_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside the application folder"):
            install_linux.install(database_file=self.target / "records.db", create_new=True)
        self.assertFalse(self.target.exists())

    def test_absolute_xdg_data_directory_and_relative_fallback(self):
        os.environ["XDG_DATA_HOME"] = str(self.directory / "custom data")
        install_linux.install()
        self.assertTrue((self.directory / "custom data/applications/tindahan-system-source.desktop").is_file())
        self.assertTrue((self.directory / "custom data/tindahan-system").is_dir())
        os.environ["XDG_DATA_HOME"] = "relative"
        self.assertEqual(install_linux.data_root(), self.home / ".local/share")


if __name__ == "__main__":
    unittest.main()
