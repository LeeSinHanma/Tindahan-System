from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk

from core import inventory
from db import database
from .theme_manager import ThemeManager


class DashboardFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, on_navigate=None) -> None:
        super().__init__(master, padding=16)
        self.on_navigate = on_navigate
        self.filter_days = 7
        self.filter_buttons: dict[int, tk.Button] = {}
        top_level = master.winfo_toplevel()
        screen_w = top_level.winfo_screenwidth()
        screen_h = top_level.winfo_screenheight()
        self.compact_layout = screen_w < 1400 or screen_h < 820
        self.theme = ThemeManager(self.compact_layout)

        self._configure_styles()
        self._build_ui()
        self.refresh()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.configure("DashboardTitle.TLabel", font=("Segoe UI", self.theme.heading_huge, "bold"))
        style.configure("DashboardSubhead.TLabel", font=("Segoe UI", self.theme.body_medium))
        style.configure("DashboardCardValue.TLabel", font=("Segoe UI", self.theme.heading_huge, "bold"))
        style.configure("DashboardQuick.TButton", font=("Segoe UI", self.theme.body_medium, "bold"))
        style.configure("Treeview", rowheight=self.theme.table_row_height)
        style.configure("Treeview.Heading", font=("Segoe UI", self.theme.body_medium, "bold"))

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, self.theme.gap_large))

        ttk.Label(header, text="Dashboard", style="DashboardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Live overview of sales, stock, and product health.",
            style="DashboardSubhead.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        controls = ttk.Frame(self)
        controls.pack(fill=tk.X, pady=(0, self.theme.gap_large))

        filters = ttk.Frame(controls)
        filters.pack(side=tk.LEFT)
        ttk.Label(filters, text="Sales Range:").pack(side=tk.LEFT, padx=(0, 8))
        self._add_filter_button(filters, "Today", 1)
        self._add_filter_button(filters, "7 Days", 7)
        self._add_filter_button(filters, "30 Days", 30)

        quick_actions = ttk.Frame(controls)
        quick_actions.pack(side=tk.RIGHT)
        ttk.Button(quick_actions, text="Open POS", style="DashboardQuick.TButton", command=lambda: self._navigate("pos")).pack(side=tk.LEFT)
        ttk.Button(
            quick_actions,
            text="Open Inventory",
            style="DashboardQuick.TButton",
            command=lambda: self._navigate("inventory"),
        ).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(
            quick_actions,
            text="Open Untracked",
            style="DashboardQuick.TButton",
            command=lambda: self._navigate("untracked"),
        ).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(
            quick_actions,
            text="Open Shopping List",
            style="DashboardQuick.TButton",
            command=lambda: self._navigate("shopping_list"),
        ).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(quick_actions, text="Refresh", style="DashboardQuick.TButton", command=self.refresh).pack(side=tk.LEFT, padx=(8, 0))

        self.cards = ttk.Frame(self)
        self.cards.pack(fill=tk.X, pady=(0, self.theme.gap_small))

        self._card_frames: dict[str, ttk.Label] = {}
        card_specs = [
            ("Products", "product_count"),
            ("Low Stock", "low_stock_count"),
            ("Untracked", "untracked_count"),
            ("Sales Total", "total_sales"),
            ("Transactions", "sale_count"),
            ("Inventory Value", "inventory_value"),
        ]

        for index, (title, key) in enumerate(card_specs):
            card = ttk.LabelFrame(self.cards, padding=self.theme.padding_medium, text=title)
            card.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 8, 0))
            self.cards.columnconfigure(index, weight=1)
            value = ttk.Label(card, text="0", style="DashboardCardValue.TLabel")
            value.pack(anchor="w")
            self._card_frames[key] = value

        status_row = ttk.Frame(self)
        status_row.pack(fill=tk.X, pady=(self.theme.gap_medium, 0))
        status_row.columnconfigure(0, weight=1)
        status_row.columnconfigure(1, weight=1)

        self.warning_card = tk.Frame(status_row, bg="#16a34a")
        self.warning_card.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self.warning_label = tk.Label(
            self.warning_card,
            text="Stock health is good",
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            padx=12,
            pady=10,
        )
        self.warning_label.pack(fill=tk.X)

        self.sales_card = tk.Frame(status_row, bg="#2563eb")
        self.sales_card.grid(row=0, column=1, sticky="ew", padx=(4, 0))
        self.sales_label = tk.Label(
            self.sales_card,
            text="Sales status",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            padx=12,
            pady=10,
        )
        self.sales_label.pack(fill=tk.X)

        content = ttk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True, pady=(self.theme.gap_large, 0))
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=2)
        content.rowconfigure(1, weight=1)

        inner_padding = self.theme.padding_medium
        gap = self.theme.gap_medium

        left_top = ttk.LabelFrame(content, text="Recent Sales", padding=inner_padding)
        left_top.grid(row=0, column=0, sticky="nsew", padx=(0, gap))

        self.sales_table = ttk.Treeview(left_top, columns=("id", "date", "time", "total"), show="headings", height=self.theme.table_height_medium)
        self.sales_table.heading("id", text="ID")
        self.sales_table.heading("date", text="Date")
        self.sales_table.heading("time", text="Time")
        self.sales_table.heading("total", text="Total")
        self.sales_table.column("id", width=60, anchor=tk.CENTER)
        self.sales_table.column("date", width=120)
        self.sales_table.column("time", width=100)
        self.sales_table.column("total", width=110, anchor=tk.E)
        self.sales_table.pack(fill=tk.BOTH, expand=True)
        self.sales_table.bind("<Double-1>", self._open_sale_details_modal)

        right_top = ttk.LabelFrame(content, text="Top Selling Products", padding=inner_padding)
        right_top.grid(row=0, column=1, sticky="nsew")

        self.top_table = ttk.Treeview(right_top, columns=("name", "qty", "revenue"), show="headings", height=self.theme.table_height_medium)
        self.top_table.heading("name", text="Product")
        self.top_table.heading("qty", text="Qty")
        self.top_table.heading("revenue", text="Revenue")
        self.top_table.column("name", width=180)
        self.top_table.column("qty", width=60, anchor=tk.CENTER)
        self.top_table.column("revenue", width=100, anchor=tk.E)
        self.top_table.pack(fill=tk.BOTH, expand=True)

        chart_box = ttk.LabelFrame(content, text="Sales Line Graph", padding=inner_padding)
        chart_box.grid(row=1, column=0, sticky="nsew", padx=(0, gap), pady=(gap, 0))
        self.sales_chart = tk.Canvas(chart_box, height=self.theme.chart_height, bg="white", highlightthickness=0)
        self.sales_chart.pack(fill=tk.BOTH, expand=True)

        low_stock_box = ttk.LabelFrame(content, text="Low Stock Alerts", padding=inner_padding)
        low_stock_box.grid(row=1, column=1, sticky="nsew", pady=(gap, 0))
        self.stock_table = ttk.Treeview(low_stock_box, columns=("name", "stock"), show="headings", height=self.theme.table_height_small)
        self.stock_table.heading("name", text="Product")
        self.stock_table.heading("stock", text="Stock")
        self.stock_table.column("name", width=180)
        self.stock_table.column("stock", width=60, anchor=tk.CENTER)
        self.stock_table.pack(fill=tk.BOTH, expand=True)

    def _add_filter_button(self, parent: ttk.Frame, text: str, days: int) -> None:
        button = tk.Button(
            parent,
            text=text,
            command=lambda d=days: self._set_filter(d),
            relief=tk.FLAT,
            padx=10,
            pady=5,
            bg="#e2e8f0",
            fg="#0f172a",
            activebackground="#cbd5e1",
            activeforeground="#0f172a",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        button.pack(side=tk.LEFT, padx=(0, 6))
        self.filter_buttons[days] = button

    def _set_filter(self, days: int) -> None:
        self.filter_days = days
        self.refresh()

    def _update_filter_buttons(self) -> None:
        for days, button in self.filter_buttons.items():
            if days == self.filter_days:
                button.configure(bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white")
            else:
                button.configure(bg="#e2e8f0", fg="#0f172a", activebackground="#cbd5e1", activeforeground="#0f172a")

    def _navigate(self, screen_name: str) -> None:
        if self.on_navigate is not None:
            self.on_navigate(screen_name)

    def _prepare_daily_points(self) -> list[dict]:
        raw_points = database.get_daily_sales(self.filter_days)
        raw_map = {row["day"]: row["total"] for row in raw_points}

        today = datetime.now().date()
        points = []
        for offset in range(self.filter_days - 1, -1, -1):
            day = today - timedelta(days=offset)
            key = day.strftime("%Y-%m-%d")
            points.append({"day": key, "total": raw_map.get(key, 0.0)})
        return points

    def _draw_line_chart(self, points: list[dict]) -> None:
        self.sales_chart.delete("all")
        self.sales_chart.update_idletasks()

        width = max(self.sales_chart.winfo_width(), 300)
        height = max(self.sales_chart.winfo_height(), 160)

        left = 40
        right = 20
        top = 14
        bottom = 30
        chart_w = width - left - right
        chart_h = height - top - bottom

        self.sales_chart.create_line(left, top, left, height - bottom, fill="#94a3b8")
        self.sales_chart.create_line(left, height - bottom, width - right, height - bottom, fill="#94a3b8")

        if not points:
            self.sales_chart.create_text(width // 2, height // 2, text="No sales data", fill="#64748b", font=("Segoe UI", 11))
            return

        max_total = max(point["total"] for point in points)
        if max_total <= 0:
            max_total = 1.0

        if len(points) == 1:
            step = chart_w
        else:
            step = chart_w / (len(points) - 1)

        coords = []
        for idx, point in enumerate(points):
            x = left + step * idx
            y = height - bottom - (point["total"] / max_total) * chart_h
            coords.extend((x, y))

            self.sales_chart.create_oval(x - 3, y - 3, x + 3, y + 3, fill="#2563eb", outline="")
            day_label = point["day"][5:] if len(point["day"]) >= 10 else point["day"]
            self.sales_chart.create_text(x, height - bottom + 12, text=day_label, fill="#334155", font=("Segoe UI", 8))

        if len(coords) >= 4:
            self.sales_chart.create_line(*coords, fill="#2563eb", width=2, smooth=True)

        self.sales_chart.create_text(left + 4, top + 8, text=f"PHP {max_total:.0f}", anchor="w", fill="#64748b", font=("Segoe UI", 9))

    def _open_sale_details_modal(self, _event: tk.Event | None = None) -> None:
        selected = self.sales_table.selection()
        if not selected:
            return

        values = self.sales_table.item(selected[0], "values")
        if not values:
            return

        try:
            sale_id = int(values[0])
        except (ValueError, TypeError):
            return

        sale = database.get_sale_details(sale_id)
        if sale is None:
            return

        modal = tk.Toplevel(self)
        modal.title(f"Sale #{sale_id} Details")
        width, height = 720, 500
        screen_w = modal.winfo_screenwidth()
        screen_h = modal.winfo_screenheight()
        pos_x = max((screen_w - width) // 2, 0)
        pos_y = max((screen_h - height) // 2, 0)
        modal.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        modal.resizable(True, True)
        modal.transient(self.winfo_toplevel())
        modal.update_idletasks()
        modal.lift()
        modal.focus_force()

        content = ttk.Frame(modal, padding=14)
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        header = ttk.Frame(content)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(header, text=f"Transaction #{sale['id']}", font=("Segoe UI", 13, "bold")).pack(anchor="w")

        date_text = sale["date"]
        sale_date = date_text[:10] if len(date_text) >= 10 else date_text
        sale_time = date_text[11:19] if len(date_text) >= 19 else "--:--:--"
        ttk.Label(header, text=f"Date: {sale_date} {sale_time}", font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 0))
        ttk.Label(header, text=f"Total: PHP {sale['total']:.2f}", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(2, 0))

        table_frame = ttk.Frame(content)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        item_columns = ("product", "qty", "unit_price", "subtotal")
        items_table = ttk.Treeview(table_frame, columns=item_columns, show="headings", height=12)
        items_table.heading("product", text="Product")
        items_table.heading("qty", text="Qty")
        items_table.heading("unit_price", text="Unit Price")
        items_table.heading("subtotal", text="Subtotal")
        items_table.column("product", width=280)
        items_table.column("qty", width=70, anchor=tk.CENTER)
        items_table.column("unit_price", width=120, anchor=tk.E)
        items_table.column("subtotal", width=120, anchor=tk.E)
        items_table.grid(row=0, column=0, sticky="nsew")

        items_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=items_table.yview)
        items_scroll.grid(row=0, column=1, sticky="ns")
        items_table.configure(yscrollcommand=items_scroll.set)

        items = sale.get("items", [])
        if not items:
            ttk.Label(
                content,
                text="No item breakdown recorded for this sale.",
                foreground="#64748b",
                font=("Segoe UI", 10, "bold"),
            ).grid(row=2, column=0, sticky="w", pady=(10, 0))
        else:
            for item in items:
                items_table.insert(
                    "",
                    tk.END,
                    values=(
                        item["product_name"],
                        item["quantity"],
                        f"PHP {item['price']:.2f}",
                        f"PHP {item['subtotal']:.2f}",
                    ),
                )

        button_row = ttk.Frame(content)
        button_row.grid(row=3, column=0, sticky="e", pady=(12, 0))
        tk.Button(
            button_row,
            text="Close",
            command=modal.destroy,
            bg="#64748b",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        ).pack(side=tk.RIGHT)

    def refresh(self) -> None:
        self._update_filter_buttons()
        summary = database.get_sales_summary(self.filter_days)

        self._card_frames["product_count"].configure(text=str(summary["product_count"]))
        self._card_frames["low_stock_count"].configure(text=str(summary["low_stock_count"]))
        self._card_frames["untracked_count"].configure(text=str(summary["untracked_count"]))
        self._card_frames["total_sales"].configure(text=f"PHP {summary['total_sales']:.2f}")
        self._card_frames["sale_count"].configure(text=str(summary["sale_count"]))
        self._card_frames["inventory_value"].configure(text=f"PHP {summary['inventory_value']:.2f}")

        low_stock_count = summary["low_stock_count"]
        if low_stock_count == 0:
            self.warning_card.configure(bg="#16a34a")
            self.warning_label.configure(bg="#16a34a", text="Stock health is good")
        elif low_stock_count <= 5:
            self.warning_card.configure(bg="#d97706")
            self.warning_label.configure(bg="#d97706", text=f"Warning: {low_stock_count} low-stock items")
        else:
            self.warning_card.configure(bg="#dc2626")
            self.warning_label.configure(bg="#dc2626", text=f"Critical: {low_stock_count} low-stock items")

        if summary["total_sales"] > 0:
            self.sales_card.configure(bg="#2563eb")
            self.sales_label.configure(
                bg="#2563eb",
                text=f"{summary['sale_count']} transactions | PHP {summary['total_sales']:.2f}",
            )
        else:
            self.sales_card.configure(bg="#475569")
            self.sales_label.configure(bg="#475569", text="No sales in selected range")

        for row_id in self.sales_table.get_children():
            self.sales_table.delete(row_id)
        for sale in database.get_recent_sales(limit=10, period_days=self.filter_days):
            date_text = sale["date"]
            sale_date = date_text[:10] if len(date_text) >= 10 else date_text
            sale_time = date_text[11:19] if len(date_text) >= 19 else "--:--:--"
            self.sales_table.insert(
                "",
                tk.END,
                values=(sale["id"], sale_date, sale_time, f"PHP {sale['total']:.2f}"),
            )

        for row_id in self.top_table.get_children():
            self.top_table.delete(row_id)
        for item in database.get_top_selling_products(limit=8, period_days=self.filter_days):
            self.top_table.insert(
                "",
                tk.END,
                values=(item["product_name"], item["total_qty"], f"PHP {item['revenue']:.2f}"),
            )

        for row_id in self.stock_table.get_children():
            self.stock_table.delete(row_id)
        for product in inventory.get_low_stock_products():
            self.stock_table.insert("", tk.END, values=(product["name"], product["stock"]))

        self._draw_line_chart(self._prepare_daily_points())