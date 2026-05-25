import tkinter as tk
from tkinter import messagebox, ttk

from core import auth


class AccountFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, get_current_user, on_logout) -> None:
        super().__init__(master, padding=14)
        self.get_current_user = get_current_user
        self.on_logout = on_logout
        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X)
        ttk.Label(header, text="Account", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(header, text="View and manage your account.").pack(anchor="w", pady=(4, 8))

        info_card = ttk.Frame(self, padding=8)
        info_card.pack(fill=tk.X, pady=(8, 12))
        self.username_label = ttk.Label(info_card, text="Username: -")
        self.username_label.pack(anchor="w")
        self.role_label = ttk.Label(info_card, text="Role: -")
        self.role_label.pack(anchor="w", pady=(4, 0))
        self.created_label = ttk.Label(info_card, text="Created: -")
        self.created_label.pack(anchor="w", pady=(4, 0))

        ttk.Separator(self).pack(fill=tk.X, pady=(6, 12))

        cp_frame = ttk.LabelFrame(self, text="Change Password", padding=10)
        cp_frame.pack(fill=tk.X)

        self.old_var = tk.StringVar()
        self.new_var = tk.StringVar()
        self.confirm_var = tk.StringVar()

        ttk.Label(cp_frame, text="Old password:").grid(row=0, column=0, sticky="w")
        ttk.Entry(cp_frame, textvariable=self.old_var, show="*").grid(row=0, column=1, sticky="ew", pady=6)
        ttk.Label(cp_frame, text="New password:").grid(row=1, column=0, sticky="w")
        ttk.Entry(cp_frame, textvariable=self.new_var, show="*").grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Label(cp_frame, text="Confirm new:").grid(row=2, column=0, sticky="w")
        ttk.Entry(cp_frame, textvariable=self.confirm_var, show="*").grid(row=2, column=1, sticky="ew", pady=6)
        cp_frame.columnconfigure(1, weight=1)

        btn_row = ttk.Frame(cp_frame)
        btn_row.grid(row=3, column=1, sticky="e", pady=(6, 0))
        ttk.Button(btn_row, text="Change Password", command=self._change_password).pack(side=tk.RIGHT)

        ttk.Separator(self).pack(fill=tk.X, pady=(12, 12))
        actions = ttk.Frame(self)
        actions.pack(fill=tk.X)
        ttk.Button(actions, text="Logout", command=self._on_logout).pack(side=tk.RIGHT)

    def refresh(self) -> None:
        user = self.get_current_user()
        if not user:
            self.username_label.config(text="Username: -")
            self.role_label.config(text="Role: -")
            self.created_label.config(text="Created: -")
            return
        self.username_label.config(text=f"Username: {user.get('username')}")
        self.role_label.config(text=f"Role: {'Admin' if user.get('is_admin') else 'User'}")
        self.created_label.config(text=f"Created: {user.get('created_at')}")

    def _change_password(self) -> None:
        user = self.get_current_user()
        if not user:
            messagebox.showerror("Not signed in", "No user signed in.", parent=self)
            return
        old = self.old_var.get().strip()
        new = self.new_var.get().strip()
        conf = self.confirm_var.get().strip()
        if not old or not new or not conf:
            messagebox.showerror("Invalid", "All password fields are required.", parent=self)
            return
        if new != conf:
            messagebox.showerror("Mismatch", "New password and confirmation do not match.", parent=self)
            return
        ok = auth.change_password(user.get("username"), old, new)
        if not ok:
            messagebox.showerror("Failed", "Old password is incorrect or update failed.", parent=self)
            return
        messagebox.showinfo("Success", "Password changed successfully.", parent=self)
        self.old_var.set("")
        self.new_var.set("")
        self.confirm_var.set("")

    def _on_logout(self) -> None:
        if callable(self.on_logout):
            self.on_logout()
