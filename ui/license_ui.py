"""Read the notices shipped with the app or a standalone setup runtime."""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


def material_path(filename: str) -> Path:
    if getattr(sys, "frozen", False):
        candidates = (
            Path(sys._MEIPASS) / filename,
            Path(sys.executable).parent / filename,
        )
    else:
        root = Path(__file__).resolve().parents[1]
        candidates = (root / filename, root / "packaging/third_party" / filename)
    return next((path for path in candidates if path.is_file()), candidates[0])


def show_licenses(parent, filename="THIRD_PARTY_NOTICES.md"):
    try:
        contents = material_path(filename).read_text(encoding="utf-8")
    except OSError as exc:
        messagebox.showerror("Open-source licenses", str(exc), parent=parent)
        return
    dialog = tk.Toplevel(parent)
    dialog.title(
        "Open-source licenses"
        if filename.endswith("NOTICES.md")
        else "Library source and rebuilding"
    )
    dialog.geometry("820x600")
    dialog.minsize(560, 360)
    dialog.transient(parent)
    panel = ttk.Frame(dialog, padding=16)
    panel.pack(fill="both", expand=True)
    panel.rowconfigure(0, weight=1)
    panel.columnconfigure(0, weight=1)
    text = tk.Text(panel, wrap="word", padx=12, pady=12)
    scrollbar = ttk.Scrollbar(panel, orient="vertical", command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)
    text.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    text.insert("1.0", contents)
    text.configure(state="disabled")
    controls = ttk.Frame(panel)
    controls.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(12, 0))

    def save_copy():
        selected = filedialog.asksaveasfilename(
            parent=dialog,
            title="Save a copy",
            initialfile=filename,
            defaultextension=".md",
            filetypes=[("Text documents", "*.md *.txt")],
        )
        if selected:
            try:
                Path(selected).write_text(contents, encoding="utf-8")
            except OSError as exc:
                messagebox.showerror("Save a copy", str(exc), parent=dialog)

    ttk.Button(controls, text="Save a copy…", command=save_copy).pack(side="left")
    if filename == "THIRD_PARTY_NOTICES.md":
        ttk.Button(
            controls,
            text="Library source and rebuilding",
            command=lambda: show_licenses(dialog, "SOURCE_CODE.md"),
        ).pack(side="left", padx=8)
    ttk.Button(controls, text="Close", command=dialog.destroy).pack(side="right")
    dialog.bind("<Escape>", lambda event: dialog.destroy())
    text.focus_set()
