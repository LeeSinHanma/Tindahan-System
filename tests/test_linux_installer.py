"""Install/update behavior, store imports, and recovery from setup failures."""

import os
import sqlite3
import sys
import tarfile
import tempfile
import tkinter as tk
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from core import linux_installer
from core.linux_installer import (
    InstallLocations,
    install_payload,
    uninstall_application,
)


@unittest.skipUnless(sys.platform == "linux", "Linux installer")
class LinuxInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="tindahan-setup-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.locations = InstallLocations(
            self.directory / "local opt/app",
            self.directory / "store data",
            self.directory / "menu",
            self.directory / "Desktop",
        )
        self.bundle = self.directory / "source/Tindahan-System"
        self.bundle.mkdir(parents=True)
        (self.bundle / "POS-System").write_text("#!/bin/sh\nexit 0\n")
        (self.bundle / "POS-System").chmod(0o755)
        (self.bundle / "Tindahan-Uninstall.run").write_text("#!/bin/sh\nexit 0\n")
        (self.bundle / "Tindahan-Uninstall.run").chmod(0o755)
        (self.bundle / "LICENSE").write_text("MIT License\n")
        (self.bundle / "_internal").mkdir()
        (self.bundle / "_internal/library.so.1").write_bytes(b"library")
        (self.bundle / "_internal/library.so").symlink_to("library.so.1")
        self.payload = self.directory / "payload.tar.gz"
        self.make_payload()

    def make_payload(self):
        with tarfile.open(self.payload, "w:gz") as archive:
            archive.add(self.bundle, arcname="Tindahan-System")

    def make_store(self, path, value="existing shop"):
        path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(path)
        self.addCleanup(connection.close)
        connection.execute("PRAGMA journal_mode=WAL")
        for table in ("products", "sales", "users", "settings"):
            connection.execute(f"CREATE TABLE {table} (value TEXT)")
        connection.execute("INSERT INTO products VALUES (?)", (value,))
        connection.commit()
        return connection

    def install(self, **kwargs):
        install_payload(self.payload, self.locations, version="0.1.0", **kwargs)

    def test_install_creates_launcher_and_preserves_bundle_symlinks(self):
        progress = []
        self.install(
            desktop_shortcut=True,
            progress=lambda percent, text: progress.append(percent),
        )
        self.assertTrue((self.locations.application / ".tindahan-install").is_file())
        self.assertTrue(os.access(self.locations.application / "POS-System", os.X_OK))
        self.assertTrue(
            (self.locations.application / "_internal/library.so").is_symlink()
        )
        menu = self.locations.applications_menu / "tindahan-system.desktop"
        self.assertIn(str(self.locations.application / "POS-System"), menu.read_text())
        self.assertEqual(
            menu.read_bytes(), (self.locations.desktop / menu.name).read_bytes()
        )
        self.assertEqual(
            (self.locations.application / ".tindahan-desktop-path").read_text().strip(),
            str(self.locations.desktop / menu.name),
        )
        self.assertEqual(progress[-1], 100)

    def test_import_copies_committed_wal_records_without_touching_source(self):
        source = self.directory / "old store/pos.db"
        self.make_store(source)
        self.install(import_database=source)
        with closing(sqlite3.connect(self.locations.data / "pos.db")) as connection:
            self.assertEqual(
                connection.execute("SELECT value FROM products").fetchone()[0],
                "existing shop",
            )
        self.assertTrue(source.exists())

    def test_update_preserves_database_audio_and_removes_obsolete_program_files(self):
        self.install()
        self.make_store(self.locations.data / "pos.db")
        sounds = self.locations.data / "sounds"
        sounds.mkdir()
        (sounds / "personal.wav").write_bytes(b"personal sound")
        (self.locations.application / "obsolete.txt").write_text("old version")
        (self.bundle / "version.txt").write_text("new version")
        self.make_payload()
        self.install()
        self.assertFalse((self.locations.application / "obsolete.txt").exists())
        self.assertEqual(
            (self.locations.application / "version.txt").read_text(), "new version"
        )
        self.assertEqual((sounds / "personal.wav").read_bytes(), b"personal sound")
        with closing(sqlite3.connect(self.locations.data / "pos.db")) as connection:
            self.assertEqual(
                connection.execute("SELECT value FROM products").fetchone()[0],
                "existing shop",
            )

    def test_import_never_overwrites_existing_store(self):
        self.make_store(self.locations.data / "pos.db", "keep this shop")
        source = self.directory / "other.db"
        self.make_store(source, "other shop")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.install(import_database=source)
        self.assertFalse(self.locations.application.exists())
        with closing(sqlite3.connect(self.locations.data / "pos.db")) as connection:
            self.assertEqual(
                connection.execute("SELECT value FROM products").fetchone()[0],
                "keep this shop",
            )

    def test_legacy_executable_adjacent_database_is_kept_and_migrated(self):
        self.install()
        self.make_store(self.locations.application / "pos.db")
        self.install()
        for path in (
            self.locations.application / "pos.db",
            self.locations.data / "pos.db",
        ):
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(
                    connection.execute("SELECT value FROM products").fetchone()[0],
                    "existing shop",
                )

    def test_unrecognized_installation_folder_is_untouched(self):
        self.locations.application.mkdir(parents=True)
        personal = self.locations.application / "personal.txt"
        personal.write_text("keep me")
        with self.assertRaisesRegex(ValueError, "other files"):
            self.install()
        self.assertEqual(personal.read_text(), "keep me")

    def test_invalid_database_does_not_replace_old_installation(self):
        self.install()
        marker = self.locations.application / "keep.txt"
        marker.write_text("previous version")
        source = self.directory / "not-a-store.db"
        with closing(sqlite3.connect(source)) as connection:
            connection.execute("CREATE TABLE unrelated (value TEXT)")
        with self.assertRaisesRegex(ValueError, "store database"):
            self.install(import_database=source)
        self.assertEqual(marker.read_text(), "previous version")
        self.assertFalse((self.locations.data / "pos.db").exists())

    def test_shortcut_failure_restores_previous_program_and_menu_entry(self):
        self.install()
        marker = self.locations.application / "keep.txt"
        marker.write_text("previous version")
        menu = self.locations.applications_menu / "tindahan-system.desktop"
        original = menu.read_bytes()
        with patch.object(
            linux_installer, "_atomic_write", side_effect=OSError("test disk failure")
        ):
            with self.assertRaises(OSError):
                self.install()
        self.assertEqual(marker.read_text(), "previous version")
        self.assertEqual(menu.read_bytes(), original)

    def test_archive_cannot_write_outside_staging_folder(self):
        import io

        with tarfile.open(self.payload, "w:gz") as archive:
            entry = tarfile.TarInfo("Tindahan-System/../../escaped.txt")
            entry.size = 4
            archive.addfile(entry, io.BytesIO(b"bad!"))
        with self.assertRaises(tarfile.FilterError):
            self.install()
        self.assertFalse((self.directory / "escaped.txt").exists())
        self.assertFalse(self.locations.application.exists())

    def test_uninstall_removes_program_and_shortcuts_but_keeps_store_and_sounds(self):
        self.install(desktop_shortcut=True)
        self.make_store(self.locations.data / "pos.db")
        sounds = self.locations.data / "sounds"
        sounds.mkdir()
        (sounds / "personal.wav").write_bytes(b"keep personal audio")
        uninstall_menu = (
            self.locations.applications_menu / "tindahan-system-uninstall.desktop"
        )
        self.assertIn("Tindahan-Uninstall.run", uninstall_menu.read_text())
        uninstall_application(self.locations)
        self.assertFalse(self.locations.application.exists())
        self.assertFalse(uninstall_menu.exists())
        self.assertFalse(
            (self.locations.applications_menu / "tindahan-system.desktop").exists()
        )
        self.assertFalse((self.locations.desktop / "tindahan-system.desktop").exists())
        self.assertEqual((sounds / "personal.wav").read_bytes(), b"keep personal audio")
        with closing(sqlite3.connect(self.locations.data / "pos.db")) as connection:
            self.assertEqual(
                connection.execute("SELECT value FROM products").fetchone()[0],
                "existing shop",
            )

    def test_uninstall_saves_legacy_records_before_removing_application(self):
        self.install()
        self.make_store(self.locations.application / "pos.db", "old shop")
        uninstall_application(self.locations)
        with closing(sqlite3.connect(self.locations.data / "pos.db")) as connection:
            self.assertEqual(
                connection.execute("SELECT value FROM products").fetchone()[0],
                "old shop",
            )

    def test_uninstall_keeps_both_legacy_and_current_store(self):
        self.install()
        self.make_store(self.locations.application / "pos.db", "old shop")
        self.make_store(self.locations.data / "pos.db", "current shop")
        uninstall_application(self.locations)
        backups = list((self.locations.data / "legacy-backups").glob("*.db"))
        self.assertEqual(len(backups), 1)
        for path, value in (
            (self.locations.data / "pos.db", "current shop"),
            (backups[0], "old shop"),
        ):
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(
                    connection.execute("SELECT value FROM products").fetchone()[0],
                    value,
                )

    def test_uninstall_refuses_unrecognized_folder_or_nested_data(self):
        self.locations.application.mkdir(parents=True)
        personal = self.locations.application / "personal.txt"
        personal.write_text("keep")
        with self.assertRaises(ValueError):
            uninstall_application(self.locations)
        self.assertTrue(personal.exists())
        (self.locations.application / ".tindahan-install").touch()
        nested = InstallLocations(
            self.locations.application,
            self.locations.application / "store",
            self.locations.applications_menu,
            self.locations.desktop,
        )
        with self.assertRaisesRegex(ValueError, "inside the application"):
            uninstall_application(nested)
        self.assertTrue(personal.exists())

    def test_setup_can_open_graphical_uninstall_and_finish(self):
        from ui.linux_setup_ui import SetupWizard

        self.install()
        try:
            root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        root.withdraw()
        setup = SetupWizard(root, self.payload, "0.1.0", locations=self.locations)
        setup.show_uninstaller()
        wizard = setup.uninstaller
        completed = []
        wizard.on_complete = lambda ok, message: (
            completed.append((ok, message)),
            root.quit(),
        )
        timeout = root.after(10000, root.quit)
        try:
            wizard.start_uninstall()
            root.mainloop()
            self.assertEqual(completed, [(True, "")])
            self.assertTrue(wizard.complete)
            self.assertEqual(wizard.remove_button.cget("text"), "Finish")
        finally:
            root.after_cancel(timeout)
            wizard.close()

    def test_child_launch_environment_does_not_depend_on_installer_runtime(self):
        with patch.dict(
            os.environ,
            {
                "LD_LIBRARY_PATH": "/tmp/installer",
                "LD_LIBRARY_PATH_ORIG": "/system/libraries",
            },
        ):
            environment = linux_installer.child_environment()
        self.assertEqual(environment["LD_LIBRARY_PATH"], "/system/libraries")
        self.assertEqual(environment["PYINSTALLER_RESET_ENVIRONMENT"], "1")
        self.assertNotIn("LD_LIBRARY_PATH_ORIG", environment)

    def test_wizard_installs_and_reaches_finish_without_terminal_commands(self):
        from ui.linux_setup_ui import SetupWizard

        try:
            root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        root.withdraw()
        completed = []

        def finished(ok, message):
            completed.append((ok, message))
            root.quit()

        wizard = SetupWizard(
            root, self.payload, "0.1.0", locations=self.locations, on_complete=finished
        )
        timeout = root.after(10000, root.quit)
        try:
            wizard.start_install()
            root.mainloop()
            self.assertEqual(completed, [(True, "")])
            self.assertTrue(wizard.complete)
            self.assertEqual(wizard.install_button.cget("text"), "Finish")
        finally:
            root.after_cancel(timeout)
            wizard.close()


if __name__ == "__main__":
    unittest.main()
