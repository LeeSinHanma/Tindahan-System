import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

from ui.dashboard_ui import DashboardFrame
from ui.inventory_ui import InventoryFrame
from ui.pos_ui import POSFrame
from ui.shopping_list_ui import ShoppingListFrame
from ui.untracked_ui import UntrackedFrame


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tindahan POS + Inventory")
        self.root.geometry("1280x760")
        self.root.minsize(1100, 680)
        self._configure_global_typography()
        self._set_default_fullscreen()

        self.active_screen: str = "dashboard"
        self.nav_buttons: dict[str, tk.Button] = {}

        self.shell = ttk.Frame(self.root)
        self.shell.pack(fill=tk.BOTH, expand=True)
        self.shell.columnconfigure(1, weight=1)
        self.shell.rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()
        self._build_frames()
        self._show_screen("dashboard")

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

    def _set_default_fullscreen(self) -> None:
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-fullscreen", True)

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
        nav_container = tk.Frame(self.sidebar, bg="#0f172a")
        nav_container.pack(fill=tk.X, padx=16)

        self._add_nav_button(nav_container, "Dashboard", "dashboard")
        self._add_nav_button(nav_container, "Point of Sale", "pos")
        self._add_nav_button(nav_container, "Inventory", "inventory")
        self._add_nav_button(nav_container, "Untracked Items", "untracked")
        self._add_nav_button(nav_container, "Shopping List", "shopping_list")

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
        button = tk.Button(
            parent,
            text=text,
            command=lambda name=screen_name: self._show_screen(name),
            anchor="w",
            relief=tk.FLAT,
            padx=16,
            pady=14,
            bg="#1e293b",
            fg="#e2e8f0",
            activebackground="#334155",
            activeforeground="#ffffff",
            font=("Segoe UI", 11, "bold"),
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
            "dashboard": DashboardFrame(self.content, on_navigate=self._show_screen),
            "pos": POSFrame(self.content),
            "inventory": InventoryFrame(self.content),
            "untracked": UntrackedFrame(self.content),
            "shopping_list": ShoppingListFrame(self.content),
        }

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def _show_screen(self, screen_name: str) -> None:
        self.active_screen = screen_name
        frame = self.frames[screen_name]
        frame.tkraise()
        self._refresh_active_screen()
        self._update_nav_state()

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

    def _update_nav_state(self) -> None:
        for screen_name, button in self.nav_buttons.items():
            if screen_name == self.active_screen:
                button.configure(bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white")
            else:
                button.configure(bg="#1e293b", fg="#e2e8f0", activebackground="#334155", activeforeground="#ffffff")