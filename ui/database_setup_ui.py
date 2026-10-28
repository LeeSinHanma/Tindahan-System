"""Choose an existing store file or a location for a new store before installation."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from core.app_paths import validate_store_database


class DatabaseSelectionDialog:
    def __init__(self, root: tk.Tk, current: Path):
        self.root = root
        self.current = current
        self.selection: tuple[Path, bool] | None = None
        root.title("Tindahan System · Choose store database")
        root.resizable(False, False)
        panel = ttk.Frame(root, padding=24)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="Choose your store database", font=("TkDefaultFont", 16, "bold")).pack(anchor="w")
        ttk.Label(
            panel,
            text="Open an existing store or create a new one before setting up your account. "
            "The app will use the file you select. Close other copies of the app first.",
            wraplength=520,
        ).pack(anchor="w", pady=(12, 16))
        if current.is_file():
            ttk.Label(panel, text=f"Current database:\n{current}", wraplength=520).pack(anchor="w", pady=(0, 8))
            ttk.Button(panel, text="Keep current database", command=lambda: self.accept(current, False)).pack(fill="x", pady=4)
        ttk.Button(panel, text="Choose existing database…", command=self.choose_existing).pack(fill="x", pady=4)
        ttk.Button(panel, text="Create a new store…", command=self.choose_new).pack(fill="x", pady=4)
        ttk.Label(
            panel,
            text="Existing stores keep their records and accounts. Creating a new store leaves your other databases intact.",
            wraplength=520,
        ).pack(anchor="w", pady=(12, 16))
        ttk.Button(panel, text="Cancel", command=root.destroy).pack(anchor="e")
        root.bind("<Escape>", lambda _event: root.destroy())

    def accept(self, path: Path, create_new: bool) -> None:
        path = path.expanduser().resolve()
        try:
            if create_new:
                if path.exists():
                    raise ValueError("That file already exists. Choose a new filename to create a store.")
            else:
                validate_store_database(path)
        except ValueError as exc:
            messagebox.showerror("Choose store database", str(exc), parent=self.root)
            return
        self.selection = (path, create_new)
        self.root.destroy()

    def choose_existing(self) -> None:
        filename = filedialog.askopenfilename(
            parent=self.root,
            title="Choose your existing store database",
            initialdir=str(self.current.parent) if self.current.parent.is_dir() else str(Path.home()),
            filetypes=[("Store database", "*.db *.sqlite *.sqlite3"), ("All files", "*.*")],
        )
        if filename:
            self.accept(Path(filename), False)

    def choose_new(self) -> None:
        filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Choose where to save your new store database",
            initialdir=str(self.current.parent) if self.current.parent.is_dir() else str(Path.home()),
            initialfile="pos.db",
            defaultextension=".db",
            filetypes=[("Store database", "*.db"), ("All files", "*.*")],
        )
        if filename:
            self.accept(Path(filename), True)


def choose_store_database(current: Path) -> tuple[Path, bool] | None:
    root = tk.Tk()
    dialog = DatabaseSelectionDialog(root, current)
    root.mainloop()
    return dialog.selection
