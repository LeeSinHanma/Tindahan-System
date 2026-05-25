import tkinter as tk
from tkinter import messagebox, ttk

from core import auth


class UsersFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X)
        ttk.Label(header, text="User Management", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(header, text="Create and view user accounts.").pack(anchor="w", pady=(4, 8))

        form = ttk.Frame(self)
        form.pack(fill=tk.X, pady=(8, 8))
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.is_admin_var = tk.BooleanVar(value=False)

        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.username_var).grid(row=0, column=1, sticky="ew")
        ttk.Label(form, text="Password:").grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Entry(form, textvariable=self.password_var, show="*").grid(row=1, column=1, sticky="ew", pady=(6, 0))
        ttk.Checkbutton(form, text="Admin", variable=self.is_admin_var).grid(row=2, column=1, sticky="w", pady=(6, 0))
        form.columnconfigure(1, weight=1)

        ttk.Button(form, text="Create User", command=self._create_user).grid(row=3, column=1, sticky="e", pady=(8, 0))

        self.table = ttk.Treeview(self, columns=("username", "admin", "created"), show="headings", height=8)
        self.table.heading("username", text="Username")
        self.table.heading("admin", text="Admin")
        self.table.heading("created", text="Created At")
        self.table.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

    def refresh(self) -> None:
        for r in self.table.get_children():
            self.table.delete(r)
        for u in auth.get_users():
            self.table.insert("", tk.END, values=(u["username"], "Yes" if u["is_admin"] else "No", u["created_at"]))

    def _create_user(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        is_admin = self.is_admin_var.get()
        if not username or not password:
            messagebox.showerror("Invalid input", "Username and password required", parent=self)
            return
        if auth.add_user(username, password, is_admin):
            self.username_var.set("")
            self.password_var.set("")
            self.is_admin_var.set(False)
            messagebox.showinfo("User created", f"User '{username}' created", parent=self)
            self.refresh()
        else:
            messagebox.showerror("Create failed", "User could not be created (duplicate?)", parent=self)
