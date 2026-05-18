import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox

from db import database
from db.database import record_user_audit
from ui.login_ui import LoginModal, LoginFrame
from ui.dashboard_ui import DashboardFrame
from ui.debt_tracker_ui import DebtTrackerFrame
from ui.finance_ui import FinanceFrame
from ui.inventory_ui import InventoryFrame
from ui.pos_ui import POSFrame
from ui.shopping_list_ui import ShoppingListFrame
from ui.untracked_ui import UntrackedFrame
from ui.users_ui import UsersFrame
from ui.account_ui import AccountFrame


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tindahan POS + Inventory")
        self._configure_global_typography()
        self._configure_window_geometry()

        # ensure database and default admin exist
        database.init_database()
        self.current_user = None

        self.active_screen: str = "login"
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
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=12)

        text_font = tkfont.nametofont("TkTextFont")
        text_font.configure(family="Segoe UI", size=12)

        fixed_font = tkfont.nametofont("TkFixedFont")
        fixed_font.configure(family="Consolas", size=13)

        heading_font = tkfont.nametofont("TkHeadingFont")
        heading_font.configure(family="Segoe UI", size=13, weight="bold")

        style = ttk.Style(self.root)
        style.configure("TLabel", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 11, "bold"))
        style.configure("TEntry", font=("Segoe UI", 12))
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    def _configure_window_geometry(self) -> None:
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.root.minsize(min(1024, screen_w), min(640, screen_h))

        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry(f"{screen_w}x{screen_h}+0+0")

    def _toggle_fullscreen(self, _event: tk.Event | None = None) -> None:
        try:
            if self.root.state() == "zoomed":
                self.root.state("normal")
            else:
                self.root.state("zoomed")
        except tk.TclError:
            current = bool(self.root.attributes("-fullscreen"))
            self.root.attributes("-fullscreen", not current)

    def _build_sidebar(self) -> None:
        self.sidebar = tk.Frame(self.shell, width=280, bg="#0f172a")
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        brand_card = tk.Frame(self.sidebar, bg="#111827", bd=0, highlightthickness=0)
        brand_card.pack(fill=tk.X, padx=16, pady=(16, 14))

        tk.Label(
            brand_card,
            text="Tindahan System",
            bg="#111827",
            fg="#f8fafc",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        ).pack(fill=tk.X, padx=14, pady=(14, 2))
        tk.Label(
            brand_card,
            text="Offline POS Dashboard",
            bg="#111827",
            fg="#cbd5e1",
            font=("Segoe UI", 10),
            anchor="w",
        ).pack(fill=tk.X, padx=14)
        tk.Label(
            brand_card,
            text="Fast navigation for cashier and inventory tasks.",
            bg="#111827",
            fg="#94a3b8",
            font=("Segoe UI", 9),
            wraplength=230,
            justify=tk.LEFT,
            anchor="w",
        ).pack(fill=tk.X, padx=14, pady=(4, 14))

        self._add_sidebar_section("MAIN MENU")
        self.nav_container = tk.Frame(self.sidebar, bg="#0f172a")
        self.nav_container.pack(fill=tk.X, padx=16)

        self._add_nav_button(self.nav_container, "Dashboard", "dashboard")
        self._add_nav_button(self.nav_container, "Point of Sale", "pos")
        self._add_nav_button(self.nav_container, "Inventory", "inventory")
        self._add_nav_button(self.nav_container, "Untracked Items", "untracked")
        self._add_nav_button(self.nav_container, "Shopping List", "shopping_list")
        self._add_nav_button(self.nav_container, "Debt Tracker", "debt_tracker")
        self._add_nav_button(self.nav_container, "Finance", "finance")
        self._add_nav_button(self.nav_container, "Account", "account")
        # show user management only for admins
        try:
            if (getattr(self, "current_user", None) or {}).get("is_admin"):
                self._add_nav_button(self.nav_container, "Users", "users")
        except Exception:
            pass

        self._add_sidebar_section("SHORTCUTS", pady=(18, 8))
        shortcut_card = tk.Frame(self.sidebar, bg="#111827")
        shortcut_card.pack(fill=tk.X, padx=16)

        tk.Label(
            shortcut_card,
            text="F11  Toggle fullscreen",
            bg="#111827",
            fg="#e2e8f0",
            font=("Segoe UI", 10),
            anchor="w",
        ).pack(fill=tk.X, padx=14, pady=(12, 4))
        tk.Label(
            shortcut_card,
            text="Use the menu buttons to switch between sections.",
            bg="#111827",
            fg="#94a3b8",
            font=("Segoe UI", 9),
            wraplength=220,
            justify=tk.LEFT,
            anchor="w",
        ).pack(fill=tk.X, padx=14, pady=(0, 12))

        ttk.Separator(self.sidebar).pack(fill=tk.X, padx=16, pady=14)
        tk.Label(
            self.sidebar,
            text="Ready for offline use",
            bg="#0f172a",
            fg="#94a3b8",
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill=tk.X, padx=16, pady=(0, 14))

        # Logout button
        try:
            signin_btn = tk.Button(
                self.sidebar,
                text="Sign In",
                command=self._handle_signin,
                anchor="w",
                relief=tk.FLAT,
                padx=12,
                pady=10,
                bg="#064e3b",
                fg="#fff",
                activebackground="#065f46",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
            )
            signin_btn.pack(fill=tk.X, padx=16, pady=(0, 8))

            logout_btn = tk.Button(
                self.sidebar,
                text="Logout",
                command=self._handle_logout,
                anchor="w",
                relief=tk.FLAT,
                padx=12,
                pady=10,
                bg="#dc2626",
                fg="#ffffff",
                activebackground="#b91c1c",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
            )
            logout_btn.pack(fill=tk.X, padx=16, pady=(0, 18))
        except Exception:
            pass

    def _add_sidebar_section(self, title: str, pady: tuple[int, int] = (0, 8)) -> None:
        tk.Label(
            self.sidebar,
            text=title,
            bg="#0f172a",
            fg="#64748b",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        ).pack(fill=tk.X, padx=16, pady=pady)

    def _add_nav_button(self, parent: ttk.Frame, text: str, screen_name: str) -> None:
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        compact_layout = screen_w < 1400 or screen_h < 820
        
        btn_padx = 12 if compact_layout else 16
        btn_pady = 10 if compact_layout else 14
        btn_font_size = 10 if compact_layout else 11
        
        button = tk.Button(
            parent,
            text=text,
            command=lambda name=screen_name: self._show_screen(name),
            anchor="w",
            relief=tk.FLAT,
            padx=btn_padx,
            pady=btn_pady,
            bg="#1e293b",
            fg="#e2e8f0",
            activebackground="#334155",
            activeforeground="#ffffff",
            font=("Segoe UI", btn_font_size, "bold"),
            cursor="hand2",
        )
        button.pack(fill=tk.X, pady=(0, 8))
        self.nav_buttons[screen_name] = button

    def _build_content_area(self) -> None:
        self.content = ttk.Frame(self.shell, padding=16)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)

    def _build_frames(self) -> None:
        self.frames = {
            "login": LoginFrame(self.content, on_success=self._on_login_success, on_cancel=self._on_login_cancel),
            "dashboard": DashboardFrame(self.content, on_navigate=self._show_screen),
            "pos": POSFrame(self.content),
            "inventory": InventoryFrame(self.content),
            "untracked": UntrackedFrame(self.content),
            "shopping_list": ShoppingListFrame(self.content),
            "debt_tracker": DebtTrackerFrame(self.content),
            "finance": FinanceFrame(self.content),
            "account": AccountFrame(self.content, get_current_user=lambda: getattr(self, "current_user", None), on_logout=self._handle_logout),
        }
        if (getattr(self, "current_user", None) or {}).get("is_admin"):
            self.frames["users"] = UsersFrame(self.content)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # show login screen first
        self._show_screen("login")

    def _show_screen(self, screen_name: str) -> None:
        # Allow login screen always; other screens require authentication
        if screen_name != "login" and self.current_user is None:
            # redirect to login if trying to access protected screen without auth
            messagebox.showwarning("Not authenticated", "Please log in first.", parent=self.root)
            self.active_screen = "login"
            self.frames["login"].tkraise()
            self._update_nav_state()
            return
        
        self.active_screen = screen_name
        frame = self.frames[screen_name]
        frame.tkraise()
        
        # Clear login form when returning to login screen
        if screen_name == "login" and hasattr(frame, "clear_fields"):
            frame.clear_fields()
        
        self._refresh_active_screen()
        self._update_nav_state()

    def _handle_logout(self) -> None:
        # Confirm logout action first
        if not messagebox.askyesno("Confirm logout", "Are you sure you want to log out?", parent=self.root):
            return
        # record audit for logout
        try:
            cu = getattr(self, "current_user", None) or {}
            record_user_audit(cu.get("username"), cu.get("id"), "logout", "user initiated logout")
        except Exception:
            pass

        # Clear persistent login settings
        try:
            database.set_setting("persistent_login_enabled", "0")
        except Exception:
            pass

        self.current_user = None
        self._sync_user_access()
        # show dedicated login screen (if login cancelled by user, close app)
        self._show_screen("login")

    def _handle_signin(self) -> None:
        # show login screen in content area to sign in/switch without modal
        self._show_screen("login")

    def _on_login_success(self, user: dict) -> None:
        # called by LoginFrame when login succeeds
        self.current_user = user
        try:
            record_user_audit(user.get("username"), user.get("id"), "login", "user signed in")
        except Exception:
            pass
        self._sync_user_access()
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
            persistent_enabled = database.get_setting("persistent_login_enabled", "0") == "1"
            if not persistent_enabled:
                return
            
            username = database.get_setting("persistent_login_username", "")
            if not username:
                return
            
            # Try to get the user without password verification
            from core import auth
            user = auth.get_user_by_username(username)
            if user:
                self.current_user = user
                try:
                    record_user_audit(user.get("username"), user.get("id"), "login", "persistent auto-login")
                except Exception:
                    pass
                self._sync_user_access()
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
            if "users" not in self.nav_buttons:
                self._add_nav_button(self.nav_container, "Users", "users")
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

    def _refresh_active_screen(self) -> None:
        if self.active_screen == "dashboard":
            self.frames["dashboard"].refresh()
        elif self.active_screen == "pos":
            self.frames["pos"].focus_barcode()
        elif self.active_screen == "inventory":
            self.frames["inventory"].refresh_products()
            self.frames["inventory"].focus_search()
        elif self.active_screen == "untracked":
            self.frames["untracked"].refresh()
        elif self.active_screen == "shopping_list":
            self.frames["shopping_list"].refresh()
        elif self.active_screen == "debt_tracker":
            self.frames["debt_tracker"].refresh()
        elif self.active_screen == "account":
            self.frames["account"].refresh()
        elif self.active_screen == "finance":
            self.frames["finance"].refresh()

    def _update_nav_state(self) -> None:
        is_authenticated = self.current_user is not None
        
        for screen_name, button in self.nav_buttons.items():
            if not is_authenticated:
                # disable all nav buttons when not logged in
                button.config(state="disabled", bg="#64748b", fg="#94a3b8", activebackground="#64748b", activeforeground="#94a3b8")
            elif screen_name == self.active_screen:
                button.configure(bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", state="normal")
            else:
                button.configure(bg="#1e293b", fg="#e2e8f0", activebackground="#334155", activeforeground="#ffffff", state="normal")