import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

from core import inventory
from db import database
from ui import theme as visual
from ui.widgets import (
    ActionButton,
    DataTable,
    FlowFrame,
    MetricGrid,
    page_header,
    table,
)


class DashboardFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, on_navigate=None) -> None:
        super().__init__(master, padding=16)
        self.on_navigate = on_navigate
        self.filter_days = 7
        self.filter_buttons: dict[int, tk.Button] = {}
        self.theme = visual.get_theme()

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        self.configure(padding=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        page_header(
            self,
            "Overview",
            "Your store at a glance. Track sales and see what needs attention.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        controls = FlowFrame(self)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for label, days in [("Today", 1), ("7 days", 7), ("30 days", 30)]:
            button = controls.add(
                ActionButton(
                    controls, text=label, command=lambda d=days: self._set_filter(d)
                )
            )
            self.filter_buttons[days] = button
        controls.add(
            ActionButton(
                controls,
                text="New sale",
                variant="Primary",
                command=lambda: self._navigate("pos"),
            )
        )
        controls.add(
            ActionButton(
                controls,
                text="Review stock",
                command=lambda: self._navigate("inventory"),
            )
        )
        controls.add(
            ActionButton(
                controls, text="Refresh", variant="Quiet", command=self.refresh
            )
        )
        self.cards = MetricGrid(
            self,
            [
                ("Sales in selected period", "total_sales"),
                ("Transactions", "sale_count"),
                ("Products needing stock", "low_stock_count"),
                ("Inventory sell value", "inventory_value"),
            ],
        )
        self.cards.grid(row=2, column=0, sticky="ew")
        self._card_frames = self.cards.values
        status = ttk.Frame(self)
        status.grid(row=3, column=0, sticky="ew", pady=(4, 12))
        status.columnconfigure(0, weight=1)
        self.warning_label = ttk.Label(
            status, text="", style="Muted.TLabel", wraplength=650
        )
        self.warning_label.grid(row=0, column=0, sticky="w")
        self.sales_label = ttk.Label(status, text="", style="Muted.TLabel")
        self.sales_label.grid(row=1, column=0, sticky="w", pady=(4, 0))
        notebook = ttk.Notebook(self)
        notebook.grid(row=4, column=0, sticky="nsew")
        for title, attribute, columns, headings, widths, empty in [
            (
                "Recent sales",
                "sales_table",
                ("id", "date", "time", "total"),
                ("Sale", "Date", "Time", "Total"),
                (60, 140, 120, 140),
                "No sales in this period. Start a sale from Point of Sale.",
            ),
            (
                "Top products",
                "top_table",
                ("name", "qty", "revenue"),
                ("Product", "Quantity", "Revenue"),
                (240, 100, 140),
                "Top products will appear after your first sale.",
            ),
            (
                "Stock alerts",
                "stock_table",
                ("name", "stock"),
                ("Product", "Remaining stock"),
                (260, 140),
                "No low-stock products to review.",
            ),
        ]:
            panel = ttk.Frame(notebook, padding=12)
            panel.columnconfigure(0, weight=1)
            panel.rowconfigure(0, weight=1)
            box, tree = table(panel, columns, headings, widths, empty_text=empty)
            box.grid(row=0, column=0, sticky="nsew")
            notebook.add(panel, text=title)
            setattr(self, attribute, tree)
        self.sales_table.bind("<Double-1>", self._open_sale_details_modal)
        self.sales_table.bind("<Return>", self._open_sale_details_modal)
        chart_panel = ttk.Frame(notebook, padding=12)
        self.sales_chart = tk.Canvas(
            chart_panel, bg=visual.SURFACE, highlightthickness=0, height=155
        )
        self.sales_chart.pack(fill="both", expand=True)
        notebook.add(chart_panel, text="Sales trend")
        self.sales_chart.bind(
            "<Configure>", lambda e: self._draw_line_chart(self._prepare_daily_points())
        )

    def _set_filter(self, days: int) -> None:
        self.filter_days = days
        self.refresh()

    def _update_filter_buttons(self) -> None:
        for days, button in self.filter_buttons.items():
            button.configure(
                style="Primary.TButton" if days == self.filter_days else "TButton"
            )

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

        width = max(self.sales_chart.winfo_width(), 300)
        height = max(self.sales_chart.winfo_height(), 160)

        left = 40
        right = 20
        top = 14
        bottom = 30
        chart_w = width - left - right
        chart_h = height - top - bottom

        self.sales_chart.create_line(left, top, left, height - bottom, fill="#94a3b8")
        self.sales_chart.create_line(
            left, height - bottom, width - right, height - bottom, fill="#94a3b8"
        )

        if not points or not any(point["total"] for point in points):
            self.sales_chart.create_text(
                width // 2,
                height // 2,
                text="No sales recorded in this period",
                fill="#64748b",
                font=(visual.FONT, 11),
            )
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

            self.sales_chart.create_oval(
                x - 3, y - 3, x + 3, y + 3, fill="#2563eb", outline=""
            )
            day_label = point["day"][5:] if len(point["day"]) >= 10 else point["day"]
            if idx % max(1, len(points) // 7) == 0 or idx == len(points) - 1:
                self.sales_chart.create_text(
                    x,
                    height - bottom + 12,
                    text=day_label,
                    fill="#334155",
                    font=(visual.FONT, 8),
                )

        if len(coords) >= 4:
            self.sales_chart.create_line(*coords, fill="#2563eb", width=2, smooth=True)

        self.sales_chart.create_text(
            left + 4,
            top + 8,
            text=f"PHP {max_total:.0f}",
            anchor="w",
            fill="#64748b",
            font=(visual.FONT, 9),
        )

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
        ttk.Label(
            header, text=f"Transaction #{sale['id']}", font=(visual.FONT, 13, "bold")
        ).pack(anchor="w")

        date_text = sale["date"]
        sale_date = date_text[:10] if len(date_text) >= 10 else date_text
        sale_time = date_text[11:19] if len(date_text) >= 19 else "--:--:--"
        ttk.Label(
            header, text=f"Date: {sale_date} {sale_time}", font=(visual.FONT, 10)
        ).pack(anchor="w", pady=(2, 0))
        ttk.Label(
            header,
            text=f"Total: PHP {sale['total']:.2f}",
            font=(visual.FONT, 10, "bold"),
        ).pack(anchor="w", pady=(2, 0))

        table_frame = ttk.Frame(content)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        item_columns = ("product", "qty", "unit_price", "subtotal")
        items_table = DataTable(
            table_frame, columns=item_columns, show="headings", height=12
        )
        items_table.heading("product", text="Product")
        items_table.heading("qty", text="Qty")
        items_table.heading("unit_price", text="Unit Price")
        items_table.heading("subtotal", text="Subtotal")
        items_table.column("product", width=280)
        items_table.column("qty", width=70, anchor=tk.CENTER)
        items_table.column("unit_price", width=120, anchor=tk.E)
        items_table.column("subtotal", width=120, anchor=tk.E)
        items_table.grid(row=0, column=0, sticky="nsew")

        items_scroll = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=items_table.yview
        )
        items_scroll.grid(row=0, column=1, sticky="ns")
        items_table.configure(yscrollcommand=items_scroll.set)

        items = sale.get("items", [])
        if not items:
            ttk.Label(
                content,
                text="No item breakdown recorded for this sale.",
                foreground="#64748b",
                font=(visual.FONT, 10, "bold"),
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
        ActionButton(
            button_row,
            text="Close",
            command=modal.destroy,
            bg="#64748b",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            font=(visual.FONT, 10, "bold"),
        ).pack(side=tk.RIGHT)

    def refresh(self) -> None:
        self._update_filter_buttons()
        summary = database.get_sales_summary(self.filter_days)
        for key, value in self._card_frames.items():
            amount = summary[key]
            value.configure(
                text=f"PHP {amount:,.2f}"
                if key in ("total_sales", "inventory_value")
                else str(amount)
            )
        count = summary["low_stock_count"]
        self.warning_label.configure(
            text=f"{count} products need restocking. Review Inventory for details."
            if count
            else "No low-stock alerts.",
            foreground="#b45309" if count else "#047857",
        )
        self.sales_label.configure(
            text=f"{summary['product_count']} products  ·  {summary['untracked_count']} without stock tracking"
        )
        self.sales_table.delete(*self.sales_table.get_children())
        for sale in database.get_recent_sales(limit=50, period_days=self.filter_days):
            self.sales_table.insert(
                "",
                "end",
                values=(
                    sale["id"],
                    sale["date"][:10],
                    sale["date"][11:19],
                    f"PHP {sale['total']:,.2f}",
                ),
            )
        self.top_table.delete(*self.top_table.get_children())
        for item in database.get_top_selling_products(
            limit=20, period_days=self.filter_days
        ):
            self.top_table.insert(
                "",
                "end",
                values=(
                    item["product_name"],
                    item["total_qty"],
                    f"PHP {item['revenue']:,.2f}",
                ),
            )
        self.stock_table.delete(*self.stock_table.get_children())
        for product in inventory.get_low_stock_products():
            self.stock_table.insert(
                "", "end", values=(product["name"], product["stock"])
            )
        self._draw_line_chart(self._prepare_daily_points())
