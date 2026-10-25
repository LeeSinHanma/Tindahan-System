"""A short graphical setup flow for the self-contained Linux installer."""

import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from core.linux_installer import (
    InstallLocations,
    install_payload,
    launch_application,
    uninstall_application,
)
from ui.license_ui import show_licenses
from ui.theme import configure_styles


class SetupWizard:
    def __init__(
        self,
        root: tk.Tk,
        payload: Path,
        version: str,
        *,
        locations=None,
        on_complete=None,
    ):
        self.root = root
        self.payload = payload
        self.version = version
        self.locations = locations or InstallLocations.for_current_user()
        self.on_complete = on_complete
        self.events = queue.Queue()
        self.running = False
        self.complete = False
        self.import_database = None
        self._timer = None
        root.title("Tindahan System Setup")
        root.geometry("700x580")
        root.resizable(False, False)
        configure_styles(root)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.content = ttk.Frame(root, padding=28)
        self.content.pack(fill="both", expand=True)
        self.title = tk.StringVar(value="Welcome to Tindahan System")
        self.subtitle = tk.StringVar(
            value=f"Version {version} · Install for your user account"
        )
        ttk.Label(
            self.content,
            text="TINDAHAN",
            foreground="#2563eb",
            font=("sans-serif", 10, "bold"),
        ).pack(anchor="w")
        ttk.Label(self.content, textvariable=self.title, style="Title.TLabel").pack(
            anchor="w", pady=(14, 6)
        )
        ttk.Label(
            self.content,
            textvariable=self.subtitle,
            style="Muted.TLabel",
            wraplength=640,
        ).pack(anchor="w")
        self.body = ttk.Frame(self.content)
        self.body.pack(fill="both", expand=True, pady=(22, 0))
        ttk.Label(
            self.body,
            text="Close Tindahan System before continuing. Setup will keep your existing store records.",
            wraplength=640,
        ).pack(anchor="w")
        ttk.Label(self.body, text="Installation folder", style="Section.TLabel").pack(
            anchor="w", pady=(20, 6)
        )
        ttk.Label(
            self.body,
            text=str(self.locations.application),
            style="Muted.TLabel",
            wraplength=640,
        ).pack(anchor="w")
        self.desktop_var = tk.BooleanVar(value=False)
        self.desktop_checkbox = ttk.Checkbutton(
            self.body, text="Add a desktop shortcut", variable=self.desktop_var
        )
        self.desktop_checkbox.pack(anchor="w", pady=(16, 16))
        ttk.Label(self.body, text="Store records", style="Section.TLabel").pack(
            anchor="w"
        )
        self.records_text = tk.StringVar(
            value=(
                "Your existing store database will be kept."
                if (self.locations.data / "pos.db").exists()
                else "Start a new store, or bring records from an older installation."
            )
        )
        ttk.Label(
            self.body,
            textvariable=self.records_text,
            wraplength=640,
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(6, 10))
        self.import_button = ttk.Button(
            self.body, text="Choose existing database…", command=self.choose_database
        )
        self.import_button.pack(anchor="w")
        self.clear_import_button = ttk.Button(
            self.body, text="Use a new store", command=self.clear_import
        )
        if (self.locations.data / "pos.db").exists():
            self.import_button.configure(state="disabled")
        self.status = tk.StringVar()
        ttk.Label(
            self.content, textvariable=self.status, wraplength=640, style="Muted.TLabel"
        ).pack(anchor="w", pady=(10, 8))
        self.progress = ttk.Progressbar(self.content, mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=(0, 14))
        controls = ttk.Frame(self.content)
        controls.pack(fill="x")
        self.cancel_button = ttk.Button(controls, text="Cancel", command=self.close)
        self.cancel_button.pack(side="left")
        ttk.Button(controls, text="Licenses", command=lambda: show_licenses(root)).pack(
            side="left", padx=8
        )
        self.uninstall_button = ttk.Button(
            controls, text="Uninstall…", command=self.show_uninstaller
        )
        if (self.locations.application / ".tindahan-install").is_file():
            self.uninstall_button.pack(side="left", padx=(12, 0))
        self.install_button = ttk.Button(
            controls,
            text="Update"
            if (self.locations.application / ".tindahan-install").is_file()
            else "Install",
            style="Primary.TButton",
            command=self.start_install,
        )
        self.install_button.pack(side="right")
        self.launch_var = tk.BooleanVar(value=True)

    def choose_database(self):
        filename = filedialog.askopenfilename(
            parent=self.root,
            title="Choose your existing store database",
            filetypes=[
                ("Store database", "*.db *.sqlite *.sqlite3"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.import_database = Path(filename)
            name = self.import_database.name
            if len(name) > 80:
                name = name[:77] + "…"
            self.records_text.set(
                f"Import records from {name}. Your original file stays intact."
            )
            self.clear_import_button.pack(anchor="w", pady=(6, 0))

    def clear_import(self):
        self.import_database = None
        self.records_text.set(
            "Start a new store, or bring records from an older installation."
        )
        self.clear_import_button.pack_forget()

    def start_install(self):
        if self.running or self.complete:
            return
        self.running = True
        self.install_button.configure(state="disabled")
        self.cancel_button.configure(state="disabled")
        self.uninstall_button.configure(state="disabled")
        self.import_button.configure(state="disabled")
        self.desktop_checkbox.configure(state="disabled")
        self.clear_import_button.configure(state="disabled")
        self.status.set("Preparing installation…")
        import_database, desktop_shortcut = self.import_database, self.desktop_var.get()

        def work():
            try:
                install_payload(
                    self.payload,
                    self.locations,
                    version=self.version,
                    import_database=import_database,
                    desktop_shortcut=desktop_shortcut,
                    progress=lambda value, message: self.events.put(
                        ("progress", value, message)
                    ),
                )
                self.events.put(("done",))
            except Exception as exc:
                self.events.put(("error", str(exc)))

        threading.Thread(target=work, daemon=True, name="tindahan-setup").start()
        self._timer = self.root.after(50, self._poll)

    def _poll(self):
        self._timer = None
        while not self.events.empty():
            event = self.events.get()
            if event[0] == "progress":
                self.progress.configure(value=event[1])
                self.status.set(event[2])
            elif event[0] == "error":
                self.running = False
                self.status.set(event[1])
                self.install_button.configure(state="normal", text="Try again")
                self.cancel_button.configure(state="normal")
                self.uninstall_button.configure(state="normal")
                self.desktop_checkbox.configure(state="normal")
                self.clear_import_button.configure(state="normal")
                if not (self.locations.data / "pos.db").exists():
                    self.import_button.configure(state="normal")
                else:
                    self.import_database = None
                    self.records_text.set("Your existing store database will be kept.")
                    self.clear_import_button.pack_forget()
                if self.on_complete:
                    self.on_complete(False, event[1])
                return
            elif event[0] == "done":
                self.running = False
                self.complete = True
                self.title.set("Tindahan System is ready")
                self.subtitle.set(
                    "Open it from your application menu whenever you need it."
                )
                for child in self.body.winfo_children():
                    child.destroy()
                ttk.Label(
                    self.body,
                    text="Installation complete. Your store records are kept separately from the application.",
                    wraplength=640,
                ).pack(anchor="w", pady=(0, 16))
                ttk.Checkbutton(
                    self.body, text="Launch Tindahan System", variable=self.launch_var
                ).pack(anchor="w")
                self.cancel_button.pack_forget()
                self.uninstall_button.pack_forget()
                self.install_button.configure(
                    text="Finish", state="normal", command=self.finish
                )
                if self.on_complete:
                    self.on_complete(True, "")
                return
        self._timer = self.root.after(50, self._poll)

    def finish(self):
        if self.launch_var.get():
            try:
                launch_application(self.locations)
            except OSError as exc:
                messagebox.showerror("Could not launch", str(exc), parent=self.root)
                return
        self.close()

    def show_uninstaller(self):
        if self.running:
            return
        self.content.destroy()
        self.uninstaller = UninstallWizard(self.root, locations=self.locations)

    def close(self):
        if self.running:
            return
        if self._timer:
            self.root.after_cancel(self._timer)
            self._timer = None
        self.root.destroy()


class UninstallWizard:
    def __init__(self, root: tk.Tk, *, locations=None, on_complete=None):
        self.root = root
        self.locations = locations or InstallLocations.for_current_user()
        self.on_complete = on_complete
        self.events = queue.Queue()
        self.running = False
        self.complete = False
        self._timer = None
        root.title("Uninstall Tindahan System")
        root.geometry("700x480")
        root.resizable(False, False)
        configure_styles(root)
        root.protocol("WM_DELETE_WINDOW", self.close)
        content = ttk.Frame(root, padding=28)
        content.pack(fill="both", expand=True)
        ttk.Label(
            content,
            text="TINDAHAN",
            foreground="#2563eb",
            font=("sans-serif", 10, "bold"),
        ).pack(anchor="w")
        self.title = tk.StringVar(value="Uninstall Tindahan System")
        ttk.Label(content, textvariable=self.title, style="Title.TLabel").pack(
            anchor="w", pady=(14, 16)
        )
        self.description = tk.StringVar(
            value="Close Tindahan System before continuing. This removes the application and its shortcuts."
        )
        ttk.Label(content, textvariable=self.description, wraplength=640).pack(
            anchor="w"
        )
        ttk.Label(
            content,
            text="Your store records and selected checkout sounds will be kept for future reinstallation.",
            wraplength=640,
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(18, 8))
        ttk.Label(
            content, text=str(self.locations.data), wraplength=640, style="Muted.TLabel"
        ).pack(anchor="w")
        spacer = ttk.Frame(content)
        spacer.pack(fill="both", expand=True)
        self.status = tk.StringVar()
        ttk.Label(
            content, textvariable=self.status, wraplength=640, style="Muted.TLabel"
        ).pack(anchor="w", pady=(12, 8))
        self.progress = ttk.Progressbar(content, maximum=100)
        self.progress.pack(fill="x", pady=(0, 14))
        controls = ttk.Frame(content)
        controls.pack(fill="x")
        self.cancel_button = ttk.Button(controls, text="Cancel", command=self.close)
        self.cancel_button.pack(side="left")
        ttk.Button(controls, text="Licenses", command=lambda: show_licenses(root)).pack(
            side="left", padx=8
        )
        self.remove_button = ttk.Button(
            controls,
            text="Uninstall",
            style="Primary.TButton",
            command=self.start_uninstall,
        )
        self.remove_button.pack(side="right")
        if not (self.locations.application / ".tindahan-install").is_file():
            self.title.set("Tindahan System is not installed")
            self.description.set(
                "No installation was found for this user. No files have been removed."
            )
            self.remove_button.configure(text="Close", command=self.close)
            self.cancel_button.pack_forget()

    def start_uninstall(self):
        if self.running or self.complete:
            return
        self.running = True
        self.cancel_button.configure(state="disabled")
        self.remove_button.configure(state="disabled")
        self.status.set("Preparing to uninstall…")

        def work():
            try:
                uninstall_application(
                    self.locations,
                    progress=lambda value, message: self.events.put(
                        ("progress", value, message)
                    ),
                )
                self.events.put(("done",))
            except Exception as exc:
                self.events.put(("error", str(exc)))

        threading.Thread(target=work, daemon=True, name="tindahan-uninstall").start()
        self._timer = self.root.after(50, self._poll)

    def _poll(self):
        self._timer = None
        while not self.events.empty():
            event = self.events.get()
            if event[0] == "progress":
                self.progress.configure(value=event[1])
                self.status.set(event[2])
            elif event[0] == "error":
                self.running = False
                self.status.set(event[1])
                self.cancel_button.configure(state="normal")
                self.remove_button.configure(text="Try again", state="normal")
                if self.on_complete:
                    self.on_complete(False, event[1])
                return
            elif event[0] == "done":
                self.running = False
                self.complete = True
                self.title.set("Tindahan System was removed")
                self.description.set(
                    "You can reinstall it later and continue using your saved store records."
                )
                self.cancel_button.pack_forget()
                self.remove_button.configure(
                    text="Finish", state="normal", command=self.close
                )
                if self.on_complete:
                    self.on_complete(True, "")
                return
        self._timer = self.root.after(50, self._poll)

    def close(self):
        if self.running:
            return
        if self._timer:
            self.root.after_cancel(self._timer)
            self._timer = None
        self.root.destroy()
