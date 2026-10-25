import tkinter as tk
from tkinter import ttk

from core import auth
from ui.widgets import ActionButton, page_header, table


class UsersFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        self.configure(padding=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        page_header(
            self,
            "Team members",
            "Create staff accounts and assign administrator access.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        form = ttk.Frame(self)
        form.grid(row=1, column=0, sticky="nw", pady=(0, 20))
        self.username_var, self.password_var = tk.StringVar(), tk.StringVar()
        self.is_admin_var = tk.BooleanVar(value=False)
        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", padx=(0, 16))
        ttk.Entry(form, textvariable=self.username_var, width=34).grid(
            row=0, column=1, sticky="ew"
        )
        ttk.Label(form, text="Password").grid(
            row=1, column=0, sticky="w", padx=(0, 16), pady=(8, 0)
        )
        ttk.Entry(form, textvariable=self.password_var, show="•", width=34).grid(
            row=1, column=1, sticky="ew", pady=(8, 0)
        )
        ttk.Checkbutton(
            form, text="Administrator access", variable=self.is_admin_var
        ).grid(row=2, column=1, sticky="w", pady=(6, 0))
        self.feedback_var = tk.StringVar()
        ttk.Label(
            form, textvariable=self.feedback_var, style="Muted.TLabel", wraplength=500
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(4, 0))
        ActionButton(
            form, text="Create account", variant="Primary", command=self._create_user
        ).grid(row=4, column=1, sticky="e", pady=(8, 0))
        box, self.table = table(
            self,
            ("username", "admin", "created"),
            ("Username", "Administrator", "Created"),
            (240, 160, 200),
            empty_text="No team members to display.",
        )
        box.grid(row=2, column=0, sticky="nsew")

    def refresh(self) -> None:
        for r in self.table.get_children():
            self.table.delete(r)
        for u in auth.get_users():
            self.table.insert(
                "",
                tk.END,
                values=(
                    u["username"],
                    "Yes" if u["is_admin"] else "No",
                    u["created_at"],
                ),
            )

    def _create_user(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username or not password:
            self.feedback_var.set("Enter a username and password.")
        elif error := auth.password_error(password):
            self.feedback_var.set(error)
        elif auth.add_user(username, password, self.is_admin_var.get()):
            self.username_var.set("")
            self.password_var.set("")
            self.is_admin_var.set(False)
            self.feedback_var.set(f"Account created for {username}.")
            self.refresh()
        else:
            self.feedback_var.set("Could not create the account. Try another username.")
