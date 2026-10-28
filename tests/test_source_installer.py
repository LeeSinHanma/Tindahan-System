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
            "print(json.dumps([os.environ['TINDAHAN_DATA_DIR'], sys.argv[1:]]))\n"
        )
        for directory in ("core", "db", "ui", "scripts", "packaging/third_party"):
            (self.root / directory).mkdir(parents=True)
        (self.root / "scripts/install_linux.py").write_text("# installer")
        (self.root / "packaging/third_party/SOURCE_CODE.md").write_text("source")
        self.target = self.home / ".local/opt" / install_linux.INSTALL_NAME
        self.data = self.home / ".local/share/tindahan-system/pos.db"
        for context in (
            patch.object(Path, "home", return_value=self.home),
            patch.object(install_linux, "ROOT", self.root),
            patch.dict(os.environ, {}, clear=True),
            patch.object(sys, "path", sys.path.copy()),
            patch.object(install_linux.shutil, "which", return_value=None),
            patch.object(install_linux.subprocess, "run", side_effect=self.dependencies),
        ):
            context.start()
            self.addCleanup(context.stop)

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
        self.assertEqual(json.loads(result), [str(self.data.parent), ["argument with spaces"]])
        entry = self.home / ".local/share/applications/tindahan-system-source.desktop"
        contents = entry.read_text()
        self.assertIn("Terminal=false\n", contents)
        self.assertIn("%%rate", contents)
        self.assertIn('\\\\"quote\\\\"', contents)
        self.assertTrue(os.access(self.target / "Tindahan-System", os.X_OK))

    def test_wal_import_update_and_uninstall_preserve_records(self):
        connection = sqlite3.connect(self.root / "pos.db")
        self.addCleanup(connection.close)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("CREATE TABLE records (value TEXT)")
        connection.execute("INSERT INTO records VALUES ('original')")
        connection.commit()
        install_linux.install()
        with sqlite3.connect(self.data) as installed:
            self.assertEqual(installed.execute("SELECT value FROM records").fetchone(), ("original",))
            installed.execute("UPDATE records SET value = 'new sale'")
        install_linux.install()
        with sqlite3.connect(self.data) as installed:
            self.assertEqual(installed.execute("SELECT value FROM records").fetchone(), ("new sale",))
        sound = self.data.parent / "sounds/checkout.wav"
        sound.parent.mkdir()
        sound.write_bytes(b"selected audio")
        install_linux.uninstall()
        self.assertFalse(self.target.exists())
        self.assertTrue(self.data.is_file())
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

    def test_absolute_xdg_data_directory_and_relative_fallback(self):
        os.environ["XDG_DATA_HOME"] = str(self.directory / "custom data")
        install_linux.install()
        self.assertTrue((self.directory / "custom data/applications/tindahan-system-source.desktop").is_file())
        self.assertTrue((self.directory / "custom data/tindahan-system").is_dir())
        os.environ["XDG_DATA_HOME"] = "relative"
        self.assertEqual(install_linux.data_root(), self.home / ".local/share")


if __name__ == "__main__":
    unittest.main()
