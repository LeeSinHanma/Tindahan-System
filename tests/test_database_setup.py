"""The database chooser selects real files and never overwrites another store."""

import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from db import database
from ui.database_setup_ui import DatabaseSelectionDialog


class DatabaseSelectionTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"A Tk display is required: {exc}")
        self.root.withdraw()
        self.addCleanup(self.close_root)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.store = self.directory / "my-store.sqlite3"
        connection = database.get_connection
        self.connections = []

        def tracked_connection():
            result = connection()
            self.connections.append(result)
            return result

        with patch.object(database, "DB_FILE", self.store), patch.object(database, "get_connection", side_effect=tracked_connection):
            database.init_database()
        for result in self.connections:
            result.close()
        self.dialog = DatabaseSelectionDialog(self.root, self.store)

    def close_root(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def test_keep_current_database(self):
        self.dialog.accept(self.store, False)
        self.assertEqual(self.dialog.selection, (self.store, False))

    def test_choose_existing_database_keeps_exact_filename_and_contents(self):
        original = self.store.read_bytes()
        with patch("ui.database_setup_ui.filedialog.askopenfilename", return_value=str(self.store)):
            self.dialog.choose_existing()
        self.assertEqual(self.dialog.selection, (self.store, False))
        self.assertEqual(self.store.read_bytes(), original)

    def test_new_store_selects_a_new_filename(self):
        destination = self.directory / "new-shop.db"
        with patch("ui.database_setup_ui.filedialog.asksaveasfilename", return_value=str(destination)):
            self.dialog.choose_new()
        self.assertEqual(self.dialog.selection, (destination, True))
        self.assertFalse(destination.exists())

    def test_new_store_rejects_existing_file(self):
        original = self.store.read_bytes()
        with patch("ui.database_setup_ui.messagebox.showerror") as error:
            self.dialog.accept(self.store, True)
        error.assert_called_once()
        self.assertIsNone(self.dialog.selection)
        self.assertEqual(self.store.read_bytes(), original)
        self.assertTrue(self.root.winfo_exists())

    def test_invalid_or_unrelated_database_can_be_reselected(self):
        invalid = self.directory / "bad.db"
        invalid.write_text("not SQLite")
        empty = self.directory / "empty.db"
        empty.touch()
        for selected in (invalid, empty, self.directory / "missing.db"):
            with self.subTest(selected=selected), patch("ui.database_setup_ui.messagebox.showerror") as error:
                self.dialog.accept(selected, False)
                error.assert_called_once()
                self.assertIsNone(self.dialog.selection)
                self.assertTrue(self.root.winfo_exists())

    def test_cancel_file_picker_keeps_selection_open(self):
        with patch("ui.database_setup_ui.filedialog.askopenfilename", return_value=""):
            self.dialog.choose_existing()
        with patch("ui.database_setup_ui.filedialog.asksaveasfilename", return_value=""):
            self.dialog.choose_new()
        self.assertIsNone(self.dialog.selection)
        self.assertTrue(self.root.winfo_exists())


if __name__ == "__main__":
    unittest.main()
