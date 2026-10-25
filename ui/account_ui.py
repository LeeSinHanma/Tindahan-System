import tkinter as tk
from tkinter import ttk

from core import auth
from ui import theme as visual
from ui.widgets import ActionButton, page_header


class AccountFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, get_current_user, on_logout) -> None:
        super().__init__(master, padding=14)
        self.get_current_user = get_current_user
        self.on_logout = on_logout
        self._build_ui()

    def _build_ui(self) -> None:
        self.configure(padding=0)
        page_header(
            self, "My account", "Manage your profile and sign-in details."
        ).pack(fill="x", pady=(0, 20))
        info = ttk.Frame(self, padding=20, style="Panel.TFrame")
        info.pack(anchor="w", fill="x", pady=(0, 16))
        self.username_label = ttk.Label(
            info, text="", style="Panel.TLabel", font=(visual.FONT, 16, "bold")
        )
        self.username_label.pack(anchor="w")
        self.role_label = ttk.Label(
            info, text="", style="Panel.TLabel", foreground=visual.MUTED
        )
        self.role_label.pack(anchor="w", pady=(6, 0))
        self.created_label = ttk.Label(
            info, text="", style="Panel.TLabel", foreground=visual.MUTED
        )
        self.created_label.pack(anchor="w", pady=(4, 0))
        form = ttk.Frame(self)
        form.pack(anchor="w")
        ttk.Label(form, text="Change password", style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
        )
        self.old_var, self.new_var, self.confirm_var = (
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
        )
        for row, (label, variable) in enumerate(
            [
                ("Current password", self.old_var),
                ("New password", self.new_var),
                ("Confirm password", self.confirm_var),
            ],
            start=1,
        ):
            ttk.Label(form, text=label).grid(
                row=row, column=0, sticky="w", padx=(0, 16), pady=6
            )
            ttk.Entry(form, textvariable=variable, show="•", width=34).grid(
                row=row, column=1, sticky="ew", pady=6
            )
        self.feedback_var = tk.StringVar()
        ttk.Label(
            form, textvariable=self.feedback_var, style="Muted.TLabel", wraplength=520
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ActionButton(
            form,
            text="Update password",
            variant="Primary",
            command=self._change_password,
        ).grid(row=5, column=1, sticky="e", pady=(12, 0))

    def refresh(self) -> None:
        self.old_var.set("")
        self.new_var.set("")
        self.confirm_var.set("")
        self.feedback_var.set("")
        user = self.get_current_user()
        if not user:
            self.username_label.config(text="Username: -")
            self.role_label.config(text="Role: -")
            self.created_label.config(text="Created: -")
            return
        self.username_label.config(text=f"Username: {user.get('username')}")
        self.role_label.config(
            text=f"Role: {'Admin' if user.get('is_admin') else 'User'}"
        )
        self.created_label.config(text=f"Created: {user.get('created_at')}")

    def _change_password(self) -> None:
        user = self.get_current_user()
        old, new, confirmation = (
            self.old_var.get(),
            self.new_var.get(),
            self.confirm_var.get(),
        )
        if not user:
            self.feedback_var.set("Sign in to update your password.")
        elif not old or not new or not confirmation:
            self.feedback_var.set("Complete all password fields.")
        elif new != confirmation:
            self.feedback_var.set("The new passwords do not match.")
        elif error := auth.password_error(new):
            self.feedback_var.set(error)
        elif not auth.change_password(user["username"], old, new):
            self.feedback_var.set("The current password is incorrect.")
        else:
            self.old_var.set("")
            self.new_var.set("")
            self.confirm_var.set("")
            self.feedback_var.set("Your password has been updated.")

    def _on_logout(self) -> None:
        if callable(self.on_logout):
            self.on_logout()
