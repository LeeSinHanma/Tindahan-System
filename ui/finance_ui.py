import tkinter as tk
from tkinter import ttk

from db import database
from core import debt_tracker


class FinanceFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        top_level = master.winfo_toplevel()
        screen_w = top_level.winfo_screenwidth()
        screen_h = top_level.winfo_screenheight()
        self.compact_layout = screen_w < 1400 or screen_h < 820

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X)

        ttk.Label(header, text="Finance", font=("Segoe UI", 20 if self.compact_layout else 24, "bold")).pack(anchor="w")
        ttk.Label(header, text="Summary of monetary metrics.", font=("Segoe UI", 11 if self.compact_layout else 13)).pack(anchor="w", pady=(4, 8))

        cards = ttk.Frame(self)
        cards.pack(fill=tk.X, pady=(8, 12))

        self.metrics: dict[str, ttk.Label] = {}
        specs = [
            ("Today Sales", "today_sales"),
            ("Inventory Cost (tracked)", "inventory_cost"),
            ("Inventory Value (sell)", "inventory_value"),
            ("Total Debt", "total_debt"),
            ("Daily Profit", "daily_profit"),
            ("Pending Debt Count", "pending_debt_count"),
        ]

        for i, (title, key) in enumerate(specs):
            card = ttk.LabelFrame(cards, text=title, padding=8)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0))
            cards.columnconfigure(i, weight=1)
            lbl = ttk.Label(card, text="—", font=("Segoe UI", 14, "bold"))
            lbl.pack(anchor="w")
            self.metrics[key] = lbl

        # Details area
        details = ttk.LabelFrame(self, text="Details", padding=8)
        details.pack(fill=tk.BOTH, expand=True)

        self.details_table = ttk.Treeview(details, columns=("k", "v"), show="headings", height=8)
        self.details_table.heading("k", text="Metric")
        self.details_table.heading("v", text="Value")
        self.details_table.column("k", width=300)
        self.details_table.column("v", width=180, anchor=tk.E)
        self.details_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scroll = ttk.Scrollbar(details, orient=tk.VERTICAL, command=self.details_table.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_table.configure(yscrollcommand=scroll.set)

    def refresh(self) -> None:
        # Today sales
        summary = database.get_sales_summary(1)
        today_sales = summary.get("total_sales", 0.0)

        # Inventory value (sell price) is provided by get_sales_summary
        inventory_value = summary.get("inventory_value", 0.0)

        # Inventory cost for tracked items: sum(original_price * stock) where stock_tracked=1
        with database.get_connection() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(original_price * stock), 0) AS inventory_cost FROM products WHERE stock_tracked = 1"
            ).fetchone()
            inventory_cost = float(row["inventory_cost"] or 0)

            pending_row = conn.execute("SELECT COALESCE(SUM(amount),0) AS total_pending, COALESCE(COUNT(id),0) AS pending_count FROM debt_tracker WHERE is_paid = 0").fetchone()
            total_pending = float(pending_row["total_pending"] or 0)
            pending_count = int(pending_row["pending_count"] or 0)

        self.metrics["today_sales"].configure(text=f"PHP {today_sales:.2f}")
        self.metrics["inventory_cost"].configure(text=f"PHP {inventory_cost:.2f}")
        self.metrics["inventory_value"].configure(text=f"PHP {inventory_value:.2f}")
        self.metrics["total_debt"].configure(text=f"PHP {total_pending:.2f}")
        # compute daily profit = today_sales - cogs for today's sold items
        with database.get_connection() as conn:
            cogs_row = conn.execute(
                """
                SELECT COALESCE(SUM(si.quantity * p.original_price), 0) AS cogs
                FROM sale_items si
                INNER JOIN products p ON p.id = si.product_id
                INNER JOIN sales s ON s.id = si.sale_id
                WHERE date(s.date) = date('now')
                """,
            ).fetchone()
            today_cogs = float(cogs_row["cogs"] or 0)

        daily_profit = today_sales - today_cogs
        self.metrics["daily_profit"].configure(text=f"PHP {daily_profit:.2f}")
        self.metrics["pending_debt_count"].configure(text=str(pending_count))

        # Populate details table
        for r in self.details_table.get_children():
            self.details_table.delete(r)

        details = [
            ("Today Sales (PHP)", f"{today_sales:.2f}"),
            ("COGS Today (PHP)", f"{today_cogs:.2f}"),
            ("Daily Profit (PHP)", f"{daily_profit:.2f}"),
            ("Inventory Cost (tracked, PHP)", f"{inventory_cost:.2f}"),
            ("Inventory Value (sell, PHP)", f"{inventory_value:.2f}"),
            ("Total Pending Debt (PHP)", f"{total_pending:.2f}"),
            ("Pending Debt Items", str(pending_count)),
        ]

        for k, v in details:
            self.details_table.insert("", tk.END, values=(k, v))
