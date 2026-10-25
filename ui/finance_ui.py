"""Sales-period reporting with separate current inventory and debt balances."""

import tkinter as tk
from contextlib import closing
from datetime import datetime, timedelta
from tkinter import ttk

from db import database
from ui.widgets import ActionButton, FlowFrame, MetricGrid, page_header, table


class FinanceFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.period_var = tk.StringVar(value="Today")
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
        page_header(
            self, "Finance", "Review sales performance and current store balances."
        ).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        controls = FlowFrame(self)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        controls.add(ttk.Label(controls, text="Sales period"))
        period = controls.add(
            ttk.Combobox(
                controls,
                textvariable=self.period_var,
                values=("Today", "Last 7 days", "Last 30 days"),
                state="readonly",
                width=16,
            )
        )
        period.bind("<<ComboboxSelected>>", lambda e: self.refresh())
        controls.add(ActionButton(controls, text="Refresh", command=self.refresh))
        cards = MetricGrid(
            self,
            [
                ("Period sales", "sales"),
                ("Gross profit", "profit"),
                ("Outstanding debt · current", "debt"),
                ("Stock cost · current", "inventory_cost"),
            ],
        )
        cards.grid(row=2, column=0, sticky="ew")
        self.metrics = cards.values
        note = ttk.Label(
            self,
            text="Gross profit = sales minus product cost, before other expenses. Cost uses current product prices. Inventory and debt are current balances.",
            style="Muted.TLabel",
            wraplength=760,
        )
        note.grid(row=3, column=0, sticky="ew", pady=(4, 12))
        self.bind(
            "<Configure>",
            lambda e: note.configure(wraplength=max(240, e.width)),
            add="+",
        )
        ttk.Label(self, text="Sales by day", style="Section.TLabel").grid(
            row=4, column=0, sticky="w", pady=(0, 8)
        )
        box, self.details_table = table(
            self,
            ("date", "count", "sales", "cost", "profit"),
            ("Date", "Transactions", "Sales (PHP)", "Cost (PHP)", "Gross profit (PHP)"),
            (140, 120, 140, 140, 160),
            empty_text="No sales in this period.",
        )
        for column in ("sales", "cost", "profit"):
            self.details_table.column(column, anchor="e")
        box.grid(row=5, column=0, sticky="nsew")
        self.status_var = tk.StringVar()
        ttk.Label(
            self, textvariable=self.status_var, style="Muted.TLabel", wraplength=760
        ).grid(row=6, column=0, sticky="w", pady=(8, 0))

    def refresh(self):
        days = {"Today": 1, "Last 7 days": 7, "Last 30 days": 30}[self.period_var.get()]
        start = (datetime.now().date() - timedelta(days=days - 1)).isoformat()
        end = datetime.now().date().isoformat()
        with closing(database.get_connection()) as conn:
            # Aggregate item costs before joining sales so multi-item carts do not duplicate revenue.
            rows = conn.execute(
                """
                SELECT date(s.date) AS day, COUNT(*) AS transactions,
                       SUM(s.total) AS revenue, SUM(COALESCE(c.cost, 0)) AS cost
                FROM sales s
                LEFT JOIN (
                    SELECT si.sale_id, SUM(si.quantity * p.original_price) AS cost
                    FROM sale_items si JOIN products p ON p.id = si.product_id
                    GROUP BY si.sale_id
                ) c ON c.sale_id = s.id
                WHERE date(s.date) BETWEEN ? AND ?
                GROUP BY date(s.date) ORDER BY day DESC
            """,
                (start, end),
            ).fetchall()
            stock = conn.execute(
                "SELECT COALESCE(SUM(original_price * stock), 0) AS cost, COALESCE(SUM(sell_price * stock), 0) AS value FROM products WHERE stock_tracked = 1"
            ).fetchone()
            debt = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) AS amount, COUNT(*) AS count FROM debt_tracker WHERE is_paid = 0"
            ).fetchone()
        sales = sum(row["revenue"] for row in rows)
        costs = sum(row["cost"] for row in rows)
        for key, amount in [
            ("sales", sales),
            ("profit", sales - costs),
            ("debt", debt["amount"]),
            ("inventory_cost", stock["cost"]),
        ]:
            self.metrics[key].configure(text=f"PHP {amount:,.2f}")
        self.details_table.delete(*self.details_table.get_children())
        for row in rows:
            self.details_table.insert(
                "",
                "end",
                values=(
                    row["day"],
                    row["transactions"],
                    f"{row['revenue']:,.2f}",
                    f"{row['cost']:,.2f}",
                    f"{row['revenue'] - row['cost']:,.2f}",
                ),
            )
        self.status_var.set(
            f"{sum(r['transactions'] for r in rows)} transactions  ·  {debt['count']} unpaid debt entries  ·  Stock sell value: PHP {stock['value']:,.2f}"
        )
