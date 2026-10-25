import tkinter as tk
from tkinter import messagebox, ttk

from db import database
from db.database import record_user_audit
from ui import theme as visual
from ui.account_ui import AccountFrame
from ui.cash_out_ui import CashOutFrame
from ui.dashboard_ui import DashboardFrame
from ui.debt_tracker_ui import DebtTrackerFrame
from ui.finance_ui import FinanceFrame
from ui.inventory_ui import InventoryFrame
from ui.license_ui import show_licenses
from ui.login_ui import LoginFrame
from ui.pos_ui import POSFrame
from ui.shopping_list_ui import ShoppingListFrame
from ui.theme import Theme, configure_styles, set_theme
from ui.users_ui import UsersFrame
from ui.widgets import Tooltip


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tindahan POS + Inventory")
        self._configure_global_typography()
        self._configure_window_geometry()

        # Initialize centralized theme
        theme = Theme(self.root)
        set_theme(theme)

        # Initialize tables; an empty database uses first-run account setup.
        database.init_database()
        self.current_user = None

        self.active_screen: str = "login"
        self.root.active_screen = self.active_screen
        self.nav_buttons: dict[str, tk.Button] = {}

        self.shell = ttk.Frame(self.root)
        self.shell.pack(fill=tk.BOTH, expand=True)
        self.shell.columnconfigure(1, weight=1)
        self.shell.rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()
        self._build_frames()
        # login screen is shown in _build_frames(), no override here
        # Attempt auto-login with persistent session
        self._attempt_persistent_login()
        self.root.bind("<F11>", self._toggle_fullscreen)

    def _configure_global_typography(self) -> None:
        configure_styles(self.root)

    def _configure_window_geometry(self) -> None:
        width = min(1440, self.root.winfo_screenwidth())
        height = min(900, self.root.winfo_screenheight() - 80)
        self.root.minsize(960, 640)
        self.root.geometry(f"{width}x{height}+0+0")

    def _toggle_fullscreen(self, _event=None) -> None:
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def _build_sidebar(self) -> None:
        self.sidebar = tk.Frame(self.shell, width=220, bg=visual.NAV)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.columnconfigure(0, weight=1)
        self.sidebar.rowconfigure(1, weight=1)
        self._nav_collapsed = False
        self._nav_labels = {}

        brand = tk.Frame(self.sidebar, bg=visual.NAV)
        brand.grid(row=0, column=0, sticky="ew", padx=12, pady=(20, 16))
        self.brand_label = tk.Label(
            brand,
            text="Tindahan",
            bg=visual.NAV,
            fg="white",
            font=(visual.FONT, 20, "bold"),
            anchor="w",
        )
        self.brand_label.pack(side="left")
        self.collapse_btn = tk.Button(
            brand,
            text="≡",
            command=self._toggle_sidebar,
            bg=visual.NAV,
            fg="#cbd5e1",
            activebackground="#253653",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=(visual.FONT, 16),
            cursor="hand2",
            takefocus=True,
        )
        self.collapse_btn.pack(side="right")

        nav_canvas = tk.Canvas(
            self.sidebar, bg=visual.NAV, highlightthickness=0, width=220
        )
        self._nav_canvas = nav_canvas
        nav_canvas.grid(row=1, column=0, sticky="nsew")
        self._nav_scroll = ttk.Scrollbar(
            self.sidebar, orient="vertical", command=nav_canvas.yview
        )
        nav_canvas.configure(yscrollcommand=self._nav_scroll.set)
        self.nav_container = tk.Frame(nav_canvas, bg=visual.NAV)
        nav_window = nav_canvas.create_window(
            (0, 0), window=self.nav_container, anchor="nw"
        )
        nav_canvas.bind(
            "<Configure>",
            lambda e: (
                nav_canvas.itemconfigure(nav_window, width=e.width),
                self._update_nav_scroll(),
            ),
        )
        self.nav_container.bind("<Configure>", lambda e: self._update_nav_scroll())
        nav_canvas.bind("<Button-4>", lambda e: nav_canvas.yview_scroll(-1, "units"))
        nav_canvas.bind("<Button-5>", lambda e: nav_canvas.yview_scroll(1, "units"))
        nav_canvas.bind(
            "<MouseWheel>",
            lambda e: nav_canvas.yview_scroll(-1 if e.delta > 0 else 1, "units"),
        )
        self.nav_section = tk.Label(
            self.nav_container,
            text="WORKSPACE",
            bg=visual.NAV,
            fg="#8494af",
            anchor="w",
            font=(visual.FONT, 8, "bold"),
        )
        self.nav_section.pack(fill="x", padx=20, pady=(0, 12))
        for label, key in [
            ("Overview", "dashboard"),
            ("Point of Sale", "pos"),
            ("Cash In / Out", "cash_out"),
            ("Inventory", "inventory"),
            ("Shopping List", "shopping_list"),
            ("Customers & Debt", "debt_tracker"),
            ("Finance", "finance"),
        ]:
            self._add_nav_button(self.nav_container, label, key)

        footer = tk.Frame(self.sidebar, bg=visual.NAV)
        footer.grid(row=2, column=0, sticky="ew", padx=12, pady=16)
        self.user_label = tk.Label(
            footer,
            text="",
            bg=visual.NAV,
            fg="#cbd5e1",
            anchor="w",
            font=(visual.FONT, 9),
            wraplength=190,
        )
        self.user_label.pack(fill="x", padx=8, pady=(0, 12))
        self._add_nav_button(footer, "My account", "account")
        self.licenses_btn = tk.Button(
            footer,
            text="Licenses",
            command=lambda: show_licenses(self.root),
            bg=visual.NAV,
            fg="#cbd5e1",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            anchor="w",
            font=(visual.FONT, 9),
            cursor="hand2",
        )
        self.licenses_btn.pack(fill="x", padx=8)
        self.logout_btn = tk.Button(
            footer,
            text="Sign out",
            command=self._handle_logout,
            bg="#1d2b43",
            fg="#e2e8f0",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=10,
            anchor="w",
            font=(visual.FONT, 9),
            cursor="hand2",
            takefocus=True,
        )
        self.logout_btn.pack(fill="x", padx=8, pady=(6, 0))

    def _toggle_sidebar(self):
        self._nav_collapsed = not self._nav_collapsed
        self._apply_sidebar_size()

    def _update_nav_scroll(self):
        self._nav_canvas.configure(scrollregion=self._nav_canvas.bbox("all"))
        if self.nav_container.winfo_reqheight() > self._nav_canvas.winfo_height():
            self._nav_scroll.grid(row=1, column=1, sticky="ns")
        else:
            self._nav_scroll.grid_remove()

    def _scroll_navigation(self, event):
        step = -1 if event.num == 4 or getattr(event, "delta", 0) > 0 else 1
        self._nav_canvas.yview_scroll(step, "units")
        return "break"

    def _apply_sidebar_size(self):
        collapsed = self._nav_collapsed
        self.sidebar.configure(width=76 if collapsed else 220)
        self.brand_label.configure(text="" if collapsed else "Tindahan")
        self.nav_section.configure(text="" if collapsed else "WORKSPACE")
        for key, button in self.nav_buttons.items():
            label = self._nav_labels[key]
            button.configure(
                text=label[:2].upper() if collapsed else label,
                anchor="center" if collapsed else "w",
            )
        self.user_label.configure(text="" if collapsed else self._user_caption())
        self.logout_btn.configure(
            text="Out" if collapsed else "Sign out",
            anchor="center" if collapsed else "w",
        )
        self.licenses_btn.configure(
            text="Lic" if collapsed else "Licenses",
            anchor="center" if collapsed else "w",
        )

    def _user_caption(self):
        user = self.current_user or {}
        return f"{user.get('username', '')}  ·  {'Admin' if user.get('is_admin') else 'Staff'}"

    def _add_nav_button(self, parent, text, screen_name):
        button = tk.Button(
            parent,
            text=text,
            command=lambda name=screen_name: self._show_screen(name),
            anchor="w",
            relief="flat",
            bd=0,
            padx=12,
            pady=11,
            bg=visual.NAV,
            fg="#cbd5e1",
            activebackground="#253653",
            activeforeground="white",
            font=(visual.FONT, 10),
            cursor="hand2",
            takefocus=True,
            highlightthickness=1,
            highlightbackground=visual.NAV,
            highlightcolor="#60a5fa",
        )
        button.pack(fill="x", padx=8, pady=(0, 4))
        self._nav_labels[screen_name] = text
        self.nav_buttons[screen_name] = button
        Tooltip(button, text)
        for event in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            button.bind(event, self._scroll_navigation)

    def _build_content_area(self) -> None:
        self.content = ttk.Frame(self.shell, padding=20)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)

    def _build_frames(self) -> None:
        self.frames = {
            "login": LoginFrame(
                self.content,
                on_success=self._on_login_success,
                on_cancel=self._on_login_cancel,
            ),
            "dashboard": DashboardFrame(self.content, on_navigate=self._show_screen),
            "pos": POSFrame(self.content),
            "cash_out": CashOutFrame(self.content),
            "inventory": InventoryFrame(self.content),
            "shopping_list": ShoppingListFrame(self.content),
            "debt_tracker": DebtTrackerFrame(self.content),
            "finance": FinanceFrame(self.content),
            "account": AccountFrame(
                self.content,
                get_current_user=lambda: getattr(self, "current_user", None),
                on_logout=self._handle_logout,
            ),
        }
        if (getattr(self, "current_user", None) or {}).get("is_admin"):
            self.frames["users"] = UsersFrame(self.content)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove()

        # show login screen first
        self._show_screen("login")

    def _show_screen(self, screen_name: str) -> None:
        if screen_name == "untracked":
            self.frames["inventory"]._show_untracked()
            screen_name = "inventory"
        # Allow login screen always; other screens require authentication
        if screen_name != "login" and self.current_user is None:
            # redirect to login if trying to access protected screen without auth
            messagebox.showwarning(
                "Not authenticated", "Please log in first.", parent=self.root
            )
            self.active_screen = "login"
            self.root.active_screen = self.active_screen
            self.frames["login"].grid(row=0, column=0, sticky="nsew")
            self.frames["login"].tkraise()
            self._update_nav_state()
            return

        self.active_screen = screen_name
        self.root.active_screen = self.active_screen
        for candidate in self.frames.values():
            candidate.grid_remove()
        frame = self.frames[screen_name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

        # Drop focus from any nav button or stale widget before restoring screen-specific focus.
        self.root.focus_set()

        # Clear login form when returning to login screen
        if screen_name == "login" and hasattr(frame, "clear_fields"):
            frame.clear_fields()

        self._refresh_active_screen()
        self._update_nav_state()

    def _handle_logout(self) -> None:
        # Confirm logout action first
        if not messagebox.askyesno(
            "Confirm logout", "Are you sure you want to log out?", parent=self.root
        ):
            return
        # record audit for logout
        try:
            cu = getattr(self, "current_user", None) or {}
            record_user_audit(
                cu.get("username"), cu.get("id"), "logout", "user initiated logout"
            )
        except Exception:
            pass

        # Clear persistent login settings
        try:
            database.set_setting("persistent_login_enabled", "0")
        except Exception:
            pass

        self.current_user = None
        self._sync_user_access()
        self._update_nav_state()
        # show dedicated login screen (if login cancelled by user, close app)
        self._show_screen("login")

    def _on_login_success(self, user: dict) -> None:
        # called by LoginFrame when login succeeds
        if user.get("must_change_password"):
            return
        self.current_user = user
        try:
            record_user_audit(
                user.get("username"), user.get("id"), "login", "user signed in"
            )
        except Exception:
            pass
        self._sync_user_access()
        self._update_nav_state()
        self._show_screen("dashboard")

    def _on_login_cancel(self) -> None:
        # if user cancels login from initial screen, exit app
        try:
            if self.current_user is None:
                self.root.destroy()
        except Exception:
            pass

    def _attempt_persistent_login(self) -> None:
        """Attempt to auto-login with persistent session if enabled."""
        try:
            persistent_enabled = (
                str(database.get_setting("persistent_login_enabled", "0")) == "1"
            )
            if not persistent_enabled:
                return

            username = database.get_setting("persistent_login_username", "")
            if not username:
                return

            # Try to get the user without password verification
            from core import auth

            user = auth.get_user_by_username(username)
            if user and not user.get("must_change_password"):
                self.current_user = user
                try:
                    record_user_audit(
                        user.get("username"),
                        user.get("id"),
                        "login",
                        "persistent auto-login",
                    )
                except Exception:
                    pass
                self._sync_user_access()
                self._update_nav_state()
                self._show_screen("dashboard")
        except Exception:
            pass

    def _sync_user_access(self) -> None:
        # ensure the Users nav and frame exist only for admins
        is_admin = (getattr(self, "current_user", None) or {}).get("is_admin")
        if is_admin:
            if "users" not in self.frames:
                self.frames["users"] = UsersFrame(self.content)
                self.frames["users"].grid(row=0, column=0, sticky="nsew")
                self.frames["users"].grid_remove()
            if "users" not in self.nav_buttons:
                self._add_nav_button(self.nav_container, "Team members", "users")
        else:
            # remove users nav/button/frame if present
            if "users" in self.nav_buttons:
                try:
                    self.nav_buttons["users"].destroy()
                except Exception:
                    pass
                del self.nav_buttons["users"]
            if "users" in self.frames:
                try:
                    self.frames["users"].destroy()
                except Exception:
                    pass
                del self.frames["users"]

    def _update_auth_controls(self) -> None:
        if self.current_user is None:
            self.sidebar.grid_remove()
        else:
            self.sidebar.grid()
            self._apply_sidebar_size()

    def _refresh_active_screen(self) -> None:
        if self.active_screen == "cash_out":
            self.frames["cash_out"].refresh()
        elif self.active_screen == "dashboard":
            self.frames["dashboard"].refresh()
        elif self.active_screen == "pos":
            self.frames["pos"].focus_barcode()
        elif self.active_screen == "inventory":
            self.frames["inventory"].refresh_products()
            self.frames["inventory"].focus_search()
        elif self.active_screen == "shopping_list":
            self.frames["shopping_list"].refresh()
        elif self.active_screen == "debt_tracker":
            self.frames["debt_tracker"].refresh()
        elif self.active_screen == "account":
            self.frames["account"].refresh()
        elif self.active_screen == "finance":
            self.frames["finance"].refresh()

    def _update_nav_state(self) -> None:
        self._update_auth_controls()
        for screen_name, button in self.nav_buttons.items():
            active = screen_name == self.active_screen or (
                screen_name == "inventory" and self.active_screen == "untracked"
            )
            button.configure(
                bg="#243d66" if active else visual.NAV,
                fg="white" if active else "#aebed6",
                font=(visual.FONT, 10, "bold" if active else "normal"),
            )
