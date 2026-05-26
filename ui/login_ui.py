import tkinter as tk
from tkinter import messagebox, ttk

from core import auth


class LoginModal:
    def __init__(self, parent: tk.Tk) -> None:
        self.parent = parent
        self.user = None

    def show(self) -> dict | None:
        modal = tk.Toplevel(self.parent)
        modal.title("Login")
        modal.geometry("480x260")
        modal.resizable(False, False)
        modal.transient(self.parent)
        modal.grab_set()
        modal.lift()

        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Sign in", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(content, text="Enter credentials to continue.").pack(anchor="w", pady=(4, 10))

        username_var = tk.StringVar()
        password_var = tk.StringVar()

        ttk.Label(content, text="Username:").pack(anchor="w")
        username_entry = ttk.Entry(content, textvariable=username_var)
        username_entry.pack(fill=tk.X, pady=4)

        ttk.Label(content, text="Password:").pack(anchor="w")
        password_entry = ttk.Entry(content, textvariable=password_var, show="*")
        password_entry.pack(fill=tk.X, pady=4)

        def submit(event: tk.Event | None = None) -> None:
            username = username_var.get().strip()
            password = password_var.get().strip()
            user = auth.verify_user(username, password)
            if user is None:
                messagebox.showerror("Login failed", "Invalid username or password", parent=modal)
                return
            self.user = user
            modal.destroy()

        btn_row = ttk.Frame(content)
        btn_row.pack(fill=tk.X, pady=(12, 0))

        cancel_btn = tk.Button(
            btn_row,
            text="Cancel",
            command=modal.destroy,
            bg="#9ca3af",
            fg="#000",
            activebackground="#a3a3a3",
            font=("Segoe UI", 10),
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(8, 0))

        sign_btn = tk.Button(
            btn_row,
            text="Sign In",
            command=submit,
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            font=("Segoe UI", 10, "bold"),
        )
        sign_btn.pack(side=tk.RIGHT)

        # Keyboard shortcuts: Enter to submit, Esc to cancel
        modal.bind("<Return>", submit)
        modal.bind("<Escape>", lambda e: modal.destroy())

        username_entry.focus_set()
        modal.wait_window()
        return self.user


class LoginFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, on_success, on_cancel=None) -> None:
        super().__init__(master, padding=16)
        self.on_success = on_success
        self.on_cancel = on_cancel
        self._build_ui()

    def _build_ui(self) -> None:
        ttk.Label(self, text="Sign in", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(self, text="Enter credentials to continue.").pack(anchor="w", pady=(4, 12))

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar()
        self.keep_signed_in_var = tk.BooleanVar()

        ttk.Label(self, text="Username:").pack(anchor="w")
        self.username_entry = ttk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack(fill=tk.X, pady=4)

        ttk.Label(self, text="Password:").pack(anchor="w")
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*")
        self.password_entry.pack(fill=tk.X, pady=4)

        # Checkboxes row
        checkbox_row = ttk.Frame(self)
        checkbox_row.pack(fill=tk.X, pady=(8, 0))

        def toggle_password_visibility(*args):
            show = self.show_password_var.get()
            self.password_entry.config(show="" if show else "*")

        show_pwd_check = ttk.Checkbutton(
            checkbox_row,
            text="Show password",
            variable=self.show_password_var,
            command=toggle_password_visibility,
        )
        show_pwd_check.pack(side=tk.LEFT)

        keep_signed_check = ttk.Checkbutton(
            checkbox_row,
            text="Keep me signed in",
            variable=self.keep_signed_in_var,
            command=self._on_keep_signed_in_toggle,
        )
        keep_signed_check.pack(side=tk.LEFT, padx=(16, 0))

        btn_row = ttk.Frame(self)
        btn_row.pack(fill=tk.X, pady=(12, 0))
        cancel_btn = tk.Button(btn_row, text="Cancel", command=self._cancel, bg="#9ca3af")
        cancel_btn.pack(side=tk.RIGHT, padx=(8, 0))
        sign_btn = tk.Button(btn_row, text="Sign In", command=self._submit, bg="#2563eb", fg="#fff")
        sign_btn.pack(side=tk.RIGHT)

        self.username_entry.focus_set()

        # keyboard bindings scoped to the login form only
        self.username_entry.bind('<Return>', lambda e: self._submit())
        self.password_entry.bind('<Return>', lambda e: self._submit())
        self.bind('<Escape>', lambda e: self._cancel())

    def _on_keep_signed_in_toggle(self) -> None:
        """Show verification dialog when Keep Me Signed In is toggled on."""
        if self.keep_signed_in_var.get():
            result = messagebox.askyesno(
                "Keep Me Signed In",
                "If you enable this option, the app will automatically open with your account next time.\n\n"
                "⚠️  Only enable this on a personal or secure device.\n"
                "Make sure to log out before leaving the app unattended.\n\n"
                "Do you want to keep this device signed in?",
                parent=self,
            )
            if not result:
                self.keep_signed_in_var.set(False)

    def _submit(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        user = auth.verify_user(username, password)
        if user is None:
            messagebox.showerror("Login failed", "Invalid username or password", parent=self)
            return
        
        # Store persistent login if checkbox is enabled
        if self.keep_signed_in_var.get():
            from db import database
            database.set_setting("persistent_login_enabled", "1")
            database.set_setting("persistent_login_username", username)
        else:
            from db import database
            database.set_setting("persistent_login_enabled", "0")
        
        if callable(self.on_success):
            self.on_success(user)

    def _cancel(self) -> None:
        if callable(self.on_cancel):
            self.on_cancel()

    def clear_fields(self) -> None:
        """Clear the login form fields."""
        self.username_var.set("")
        self.password_var.set("")
        self.show_password_var.set(False)
        self.keep_signed_in_var.set(False)
        self.password_entry.config(show="*")
        self.username_entry.focus_set()
