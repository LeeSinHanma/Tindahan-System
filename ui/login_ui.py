import tkinter as tk
from tkinter import ttk

from core import auth
from core.passwords import MIN_PASSWORD_LENGTH
from db import database
from ui import theme as visual
from ui.widgets import ActionButton


class LoginFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, on_success, on_cancel=None) -> None:
        super().__init__(master, padding=16)
        self.on_success = on_success
        self.on_cancel = on_cancel
        self._pending_credentials = None
        self._build_ui()
        self.clear_fields()

    def _build_ui(self) -> None:
        self.configure(padding=0)
        card = ttk.Frame(self, padding=24, style="Panel.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center", width=440)
        ttk.Label(
            card,
            text="TINDAHAN",
            style="Panel.TLabel",
            foreground=visual.PRIMARY,
            font=(visual.FONT, 10, "bold"),
        ).pack(anchor="w")
        self.title_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.help_var = tk.StringVar()
        ttk.Label(
            card,
            textvariable=self.title_var,
            style="Panel.TLabel",
            font=(visual.FONT, 24, "bold"),
        ).pack(anchor="w", pady=(8, 4))
        ttk.Label(
            card,
            textvariable=self.description_var,
            style="Panel.TLabel",
            foreground=visual.MUTED,
            wraplength=360,
        ).pack(anchor="w", pady=(0, 16))
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar()
        self.keep_signed_in_var = tk.BooleanVar()
        self.error_var = tk.StringVar()
        ttk.Label(card, text="Username", style="Panel.TLabel").pack(anchor="w")
        self.username_entry = ttk.Entry(card, textvariable=self.username_var)
        self.username_entry.pack(fill="x", pady=(6, 12))
        self.password_label = ttk.Label(card, text="Password", style="Panel.TLabel")
        self.password_label.pack(anchor="w")
        self.password_entry = ttk.Entry(card, textvariable=self.password_var, show="•")
        self.password_entry.pack(fill="x", pady=(6, 10))
        self.confirm_frame = ttk.Frame(card, style="Panel.TFrame")
        ttk.Label(
            self.confirm_frame, text="Confirm password", style="Panel.TLabel"
        ).pack(anchor="w")
        self.confirm_entry = ttk.Entry(
            self.confirm_frame, textvariable=self.confirm_var, show="•"
        )
        self.confirm_entry.pack(fill="x", pady=(6, 10))
        self.options = ttk.Frame(card, style="Panel.TFrame")
        self.options.pack(fill="x")
        ttk.Checkbutton(
            self.options,
            text="Show password",
            variable=self.show_password_var,
            command=self._toggle_password,
        ).pack(side="left")
        self.remember_checkbox = ttk.Checkbutton(
            self.options, text="Remember me", variable=self.keep_signed_in_var
        )
        ttk.Label(
            card,
            textvariable=self.help_var,
            style="Panel.TLabel",
            foreground=visual.MUTED,
            font=(visual.FONT, 9),
            wraplength=360,
        ).pack(anchor="w", pady=(6, 6))
        ttk.Label(
            card,
            textvariable=self.error_var,
            style="Panel.TLabel",
            foreground="#be123c",
            wraplength=360,
        ).pack(fill="x")
        self.signin_button = ActionButton(
            card, text="Sign in", variant="Primary", command=self._submit
        )
        self.signin_button.pack(fill="x", pady=(8, 0))
        ActionButton(
            card, text="Close application", variant="Quiet", command=self._cancel
        ).pack(fill="x", pady=(8, 0))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", self._password_return)
        self.confirm_entry.bind("<Return>", lambda e: self._submit())

    def _toggle_password(self) -> None:
        for entry in (self.password_entry, self.confirm_entry):
            entry.configure(show="" if self.show_password_var.get() else "•")

    def _password_return(self, _event=None) -> None:
        if self.mode == "login":
            self._submit()
        else:
            self.confirm_entry.focus_set()

    def _set_mode(self, mode: str) -> None:
        self.mode = mode
        self.username_entry.configure(
            state="readonly" if mode == "password_change" else "normal"
        )
        self.password_label.configure(
            text="New password" if mode == "password_change" else "Password"
        )
        if mode == "login":
            self.confirm_frame.pack_forget()
            self.remember_checkbox.pack(side="right")
            self.title_var.set("Welcome back")
            self.description_var.set("Sign in to your store workspace.")
            self.help_var.set("Use Remember me only on a trusted device.")
            self.signin_button.configure(text="Sign in")
        else:
            self.confirm_frame.pack(fill="x", before=self.options)
            self.remember_checkbox.pack_forget()
            self.keep_signed_in_var.set(False)
            self.help_var.set(
                f"Use at least {MIN_PASSWORD_LENGTH} characters. A longer passphrase is easier to remember."
            )
            if mode == "setup":
                self.title_var.set("Set up your store")
                self.description_var.set(
                    "Create your owner account. This account can manage users and store settings."
                )
                self.signin_button.configure(text="Create owner account")
            else:
                self.title_var.set("Update password")
                self.description_var.set(
                    "This account uses the old shared default. Choose your own password to continue."
                )
                self.signin_button.configure(text="Save password and sign in")

    def _submit(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get()
        self.error_var.set("")
        if self.mode in {"setup", "password_change"}:
            if password != self.confirm_var.get():
                self.error_var.set("The passwords do not match.")
                return
            if error := auth.password_error(password):
                self.error_var.set(error)
                return
            if self.mode == "setup":
                try:
                    user = auth.create_initial_admin(username, password)
                except ValueError as exc:
                    if not auth.needs_initial_setup():
                        self.clear_fields()
                    self.error_var.set(str(exc))
                    return
            else:
                username, old_password = self._pending_credentials
                if not auth.change_password(username, old_password, password):
                    self.error_var.set(
                        "The account changed. Close and reopen the app, then sign in again."
                    )
                    return
                user = auth.verify_user(username, password)
            self._finish_sign_in(user)
            return

        user = auth.verify_user(username, password)
        if user is None:
            self.error_var.set("The username or password is incorrect.")
            self.password_entry.focus_set()
            return
        if user["must_change_password"]:
            self._pending_credentials = (username, password)
            self.password_var.set("")
            self.confirm_var.set("")
            self.show_password_var.set(False)
            self._toggle_password()
            self._set_mode("password_change")
            database.set_setting("persistent_login_enabled", "0")
            self.password_entry.focus_set()
            return
        self._finish_sign_in(user)

    def _finish_sign_in(self, user: dict | None) -> None:
        if user is None or user.get("must_change_password"):
            self.error_var.set("Sign in again to continue.")
            return
        remember = self.keep_signed_in_var.get()
        database.set_setting("persistent_login_enabled", "1" if remember else "0")
        database.set_setting(
            "persistent_login_username", user["username"] if remember else ""
        )
        self.password_var.set("")
        self.confirm_var.set("")
        self._pending_credentials = None
        if callable(self.on_success):
            self.on_success(user)

    def _cancel(self) -> None:
        if callable(self.on_cancel):
            self.on_cancel()

    def clear_fields(self) -> None:
        """Reset the form and select account setup only for an empty user table."""
        self._pending_credentials = None
        self.error_var.set("")
        self.username_var.set("")
        self.password_var.set("")
        self.confirm_var.set("")
        self.show_password_var.set(False)
        self.keep_signed_in_var.set(False)
        self._toggle_password()
        self._set_mode("setup" if auth.needs_initial_setup() else "login")
        self.username_entry.focus_set()
