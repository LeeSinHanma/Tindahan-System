from datetime import datetime
import sys
import threading
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from core.cart import Cart
from core.inventory import get_product_by_barcode, get_quick_access_products, search_products
from core.sales import complete_sale, finalize_debt_checkout, validate_checkout_stock
from core import debt_tracker
from .theme_manager import ThemeManager


class POSFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        top_level = master.winfo_toplevel()
        screen_w = top_level.winfo_screenwidth()
        screen_h = top_level.winfo_screenheight()
        self.compact_layout = screen_w < 1400 or screen_h < 820
        self.theme = ThemeManager(self.compact_layout)
        self.cart = Cart()
        self.selected_product_id: int | None = None
        self.selected_search_product_id: int | None = None
        self.barcode_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.qty_var = tk.StringVar(value="1")
        self.total_var = tk.StringVar(value="Total: PHP 0.00")
        self.items_count_var = tk.StringVar(value="Items: 0")
        self.status_var = tk.StringVar(value="Ready: scan a barcode")
        self.quick_access_modal: tk.Toplevel | None = None

        self._configure_styles()
        self._build_ui()
        self.after(100, self.focus_barcode)
        top_level.bind("<F1>", self._on_quick_access_hotkey, add="+")
        top_level.bind("<Shift-Return>", self._on_checkout_hotkey, add="+")

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.configure("POSHeader.TLabel", font=("Segoe UI", self.theme.heading_large, "bold"))
        style.configure("POSSubhead.TLabel", font=("Segoe UI", self.theme.body_small))
        style.configure("POSMetricLabel.TLabel", font=("Segoe UI", self.theme.body_small, "bold"))
        style.configure("POSMetricValue.TLabel", font=("Segoe UI", self.theme.heading_huge, "bold"))
        style.configure("Treeview", rowheight=self.theme.table_row_height)
        style.configure("Treeview.Heading", font=("Segoe UI", self.theme.body_small, "bold"))

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X)

        ttk.Label(header, text="Point of Sale", style="POSHeader.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Scan barcode and press ENTER. Select a row for fast quantity actions.",
            style="POSSubhead.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        metrics = ttk.Frame(self)
        metrics.pack(fill=tk.X, pady=(self.theme.gap_medium, self.theme.gap_medium))

        card_padding = self.theme.padding_medium

        total_card = ttk.LabelFrame(metrics, text="Total Due", padding=card_padding)
        total_card.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(total_card, textvariable=self.total_var, style="POSMetricValue.TLabel").pack(anchor="w")

        items_card = ttk.LabelFrame(metrics, text="Cart", padding=card_padding)
        items_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        ttk.Label(items_card, textvariable=self.items_count_var, style="POSMetricValue.TLabel").pack(anchor="w")

        scan_box = ttk.LabelFrame(self, text="Barcode Scanner", padding=card_padding)
        scan_box.pack(fill=tk.X, pady=(0, self.theme.gap_medium))
        ttk.Label(scan_box, text="Barcode:", style="POSMetricLabel.TLabel").pack(side=tk.LEFT)

        self.barcode_entry = ttk.Entry(scan_box, textvariable=self.barcode_var, font=("Consolas", self.theme.monospace_medium))
        self.barcode_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        self.barcode_entry.bind("<Return>", self._on_scan_enter)
        self.barcode_entry.bind("<Shift-Return>", self._on_checkout_hotkey)

        search_box = ttk.LabelFrame(self, text="Search Products", padding=card_padding)
        search_box.pack(fill=tk.X, pady=(0, self.theme.gap_medium))

        search_row = ttk.Frame(search_box)
        search_row.pack(fill=tk.X)

        ttk.Label(search_row, text="Search:", style="POSMetricLabel.TLabel").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_row, textvariable=self.search_var, font=("Segoe UI", self.theme.body_medium))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 8))
        self.search_entry.bind("<Return>", self._on_search_enter)

        self._create_action_button(search_row, "Search", self._search_products, "#1d4ed8").pack(side=tk.LEFT)
        self._create_action_button(search_row, "Add Selected", self._add_selected_search_product, "#16a34a").pack(side=tk.LEFT, padx=(8, 0))

        results_box = ttk.Frame(search_box)
        results_box.pack(fill=tk.X, expand=True, pady=(self.theme.gap_medium, 0))

        search_columns = ("id", "name", "barcode", "price", "stock")
        self.search_table = ttk.Treeview(results_box, columns=search_columns, show="headings", height=self.theme.table_height_small)
        self.search_table.heading("id", text="ID")
        self.search_table.heading("name", text="Product")
        self.search_table.heading("barcode", text="Barcode")
        self.search_table.heading("price", text="Price")
        self.search_table.heading("stock", text="Stock")
        self.search_table.column("id", width=45, anchor=tk.CENTER)
        self.search_table.column("name", width=180, anchor=tk.W)
        self.search_table.column("barcode", width=120, anchor=tk.W)
        self.search_table.column("price", width=70, anchor=tk.E)
        self.search_table.column("stock", width=60, anchor=tk.CENTER)
        self.search_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        search_scroll = ttk.Scrollbar(results_box, orient=tk.VERTICAL, command=self.search_table.yview)
        search_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_table.configure(yscrollcommand=search_scroll.set)
        self.search_table.bind("<<TreeviewSelect>>", self._on_search_select)
        self.search_table.bind("<Double-1>", self._add_selected_search_product)

        table_box = ttk.LabelFrame(self, text="Current Cart", padding=card_padding)
        table_box.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "price", "qty", "subtotal", "stock")
        self.cart_table = ttk.Treeview(table_box, columns=columns, show="headings", height=self.theme.table_height_medium)
        self.cart_table.heading("id", text="ID")
        self.cart_table.heading("name", text="Product")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("qty", text="Qty")
        self.cart_table.heading("subtotal", text="Subtotal")
        self.cart_table.heading("stock", text="Stock")

        self.cart_table.column("id", width=45, anchor=tk.CENTER)
        self.cart_table.column("name", width=180, anchor=tk.W)
        self.cart_table.column("price", width=70, anchor=tk.E)
        self.cart_table.column("qty", width=50, anchor=tk.CENTER)
        self.cart_table.column("subtotal", width=85, anchor=tk.E)
        self.cart_table.column("stock", width=55, anchor=tk.CENTER)
        self.cart_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        cart_scroll = ttk.Scrollbar(table_box, orient=tk.VERTICAL, command=self.cart_table.yview)
        cart_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_table.configure(yscrollcommand=cart_scroll.set)
        self.cart_table.bind("<<TreeviewSelect>>", self._on_table_select)
        self.cart_table.bind("<Double-1>", self._double_click_add_qty)

        total_row = ttk.Frame(self)
        total_row.pack(fill=tk.X, pady=(self.theme.gap_medium, 0))
        ttk.Label(total_row, text="Current Total:", style="POSMetricLabel.TLabel").pack(side=tk.LEFT)
        ttk.Label(total_row, textvariable=self.total_var, style="POSMetricValue.TLabel").pack(side=tk.LEFT, padx=(8, 0))

        actions = ttk.Frame(self)
        actions.pack(fill=tk.X, pady=(self.theme.gap_small, self.theme.gap_small))

        qty_tools = ttk.Frame(actions)
        qty_tools.pack(side=tk.LEFT)

        ttk.Label(qty_tools, text="Quick Qty:").pack(side=tk.LEFT)
        qty_entry = ttk.Entry(qty_tools, textvariable=self.qty_var, width=5, justify=tk.CENTER, font=("Segoe UI", self.theme.body_medium))
        qty_entry.pack(side=tk.LEFT, padx=(6, 4))
        qty_entry.bind("<Return>", self._set_selected_quantity)

        self._create_action_button(qty_tools, "Set", self._set_selected_quantity, "#1d4ed8").pack(side=tk.LEFT)
        self._create_action_button(qty_tools, "+5", lambda: self._adjust_selected_quantity(5), "#16a34a").pack(side=tk.LEFT, padx=(4, 0))
        self._create_action_button(qty_tools, "-5", lambda: self._adjust_selected_quantity(-5), "#dc2626").pack(side=tk.LEFT, padx=(4, 8))

        self._create_action_button(actions, "- Qty", self._decrease_quantity, "#64748b").pack(side=tk.LEFT)
        self._create_action_button(actions, "+ Qty", self._increase_quantity, "#0ea5e9").pack(side=tk.LEFT, padx=(8, 0))
        self._create_action_button(actions, "Remove", self._remove_selected, "#b91c1c").pack(side=tk.LEFT, padx=(8, 0))
        self._create_action_button(actions, "Clear Cart", self._clear_cart, "#475569").pack(side=tk.RIGHT)
        self._create_action_button(actions, "Checkout Debt", self._checkout_debt, "#f59e0b").pack(side=tk.RIGHT, padx=(0, 8))
        self._create_action_button(actions, "Checkout", self._checkout, "#16a34a").pack(side=tk.RIGHT, padx=(0, 8))

        footer = ttk.Frame(self)
        footer.pack(fill=tk.X, pady=(self.theme.gap_small, 0))
        ttk.Label(footer, textvariable=self.status_var).pack(side=tk.LEFT)

    def _create_action_button(self, parent: tk.Widget, text: str, command, color: str) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief=tk.FLAT,
            padx=self.theme.button_padding_x,
            pady=self.theme.button_padding_y,
            font=("Segoe UI", self.theme.body_small, "bold"),
            cursor="hand2",
        )

    def focus_barcode(self) -> None:
        self.barcode_entry.focus_set()
        self.barcode_entry.icursor(tk.END)

    def _on_quick_access_hotkey(self, _event: tk.Event | None = None) -> str:
        focus_widget = self.focus_get()
        if focus_widget is None:
            return "break"

        focus_path = str(focus_widget)
        if not focus_path.startswith(str(self)):
            return "break"

        self._open_quick_access_modal()
        return "break"

    def _on_checkout_hotkey(self, _event: tk.Event | None = None) -> str:
        focus_widget = self.focus_get()
        if focus_widget is None:
            return "break"

        focus_path = str(focus_widget)
        if not focus_path.startswith(str(self)):
            return "break"

        self._checkout()
        return "break"

    def _open_quick_access_modal(self) -> None:
        if self.quick_access_modal is not None and self.quick_access_modal.winfo_exists():
            self.quick_access_modal.lift()
            self.quick_access_modal.focus_force()
            return

        modal = tk.Toplevel(self)
        self.quick_access_modal = modal
        modal.title("Quick Access Items")
        width, height = 560, 380
        modal.geometry(f"{width}x{height}")
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.update_idletasks()
        modal.lift()
        modal.focus_force()
        try:
            modal.attributes("-topmost", True)
            modal.after_idle(lambda: modal.attributes("-topmost", False))
        except tk.TclError:
            pass
        self._center_modal(modal, width, height)
        modal.lift()
        modal.wait_visibility()
        modal.grab_set()

        def close_modal() -> None:
            if self.quick_access_modal is modal:
                self.quick_access_modal = None
            modal.destroy()

        modal.protocol("WM_DELETE_WINDOW", close_modal)

        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Quick Access Items", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        ttk.Label(
            content,
            text="Pick an item, then use Add to Cart to send it into the cart.",
            wraplength=520,
        ).pack(anchor="w", pady=(4, 12))

        button_row = ttk.Frame(content)
        button_row.pack(fill=tk.X, pady=(0, 10))

        items_box = ttk.Frame(content)
        items_box.pack(fill=tk.BOTH, expand=True)

        quick_access_products = get_quick_access_products()
        quick_access_lookup = {item["id"]: item for item in quick_access_products}

        quick_columns = ("name", "price", "stock")
        quick_table = ttk.Treeview(items_box, columns=quick_columns, show="headings", height=10)
        quick_table.heading("name", text="Name")
        quick_table.heading("price", text="Price")
        quick_table.heading("stock", text="Stock")
        quick_table.column("name", width=280, anchor=tk.W)
        quick_table.column("price", width=100, anchor=tk.E)
        quick_table.column("stock", width=80, anchor=tk.CENTER)
        quick_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        quick_scroll = ttk.Scrollbar(items_box, orient=tk.VERTICAL, command=quick_table.yview)
        quick_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        quick_table.configure(yscrollcommand=quick_scroll.set)

        for product in quick_access_products:
            quick_table.insert(
                "",
                tk.END,
                iid=str(product["id"]),
                values=(
                    product["name"],
                    f"PHP {product['sell_price']:.2f}",
                    product["stock"],
                ),
            )

        if not quick_access_products:
            ttk.Label(items_box, text="No quick access items configured yet.").pack(side=tk.LEFT, padx=12, pady=12)

        def add_selected_item() -> None:
            selected = quick_table.selection()
            if not selected:
                messagebox.showerror("Invalid input", "Select a quick access item first", parent=modal)
                return

            product_id = int(selected[0])
            product = quick_access_lookup.get(product_id)
            if product is None:
                messagebox.showerror("Invalid input", "Selected quick access item not found", parent=modal)
                return

            if self._add_product_to_cart(product, restore_focus=False):
                quick_table.focus_set()

        ttk.Button(
            button_row,
            text="Add to Cart",
            command=add_selected_item,
            style="",
            width=16,
        ).pack(side=tk.LEFT)

        ttk.Label(content, text="Press Esc or close this window to return to POS.").pack(anchor="w", pady=(10, 0))

        modal.bind("<Escape>", lambda _event: close_modal())
        modal.wait_window()

    def _add_product_to_cart(self, product: dict, restore_focus: bool = True) -> bool:
        if product.get("stock_tracked", False) and product["stock"] <= 0:
            self.status_var.set(f"Out of stock: {product['name']}")
            return False

        added = self.cart.add_product(product)
        if not added:
            self.status_var.set(f"Stock limit reached: {product['name']}")
            return False

        if product["stock"] <= 10:
            self.status_var.set(f"Added: {product['name']} (low stock)")
        else:
            self.status_var.set(f"Added: {product['name']}")

        self._render_cart()
        if restore_focus:
            self.focus_barcode()
        return True

    def _on_search_enter(self, _event: tk.Event | None = None) -> str:
        self._search_products()
        return "break"

    def _search_products(self) -> None:
        search_term = self.search_var.get().strip()
        products = search_products(search_term) if search_term else []

        for row_id in self.search_table.get_children():
            self.search_table.delete(row_id)

        for product in products:
            self.search_table.insert(
                "",
                tk.END,
                iid=str(product["id"]),
                values=(
                    product["id"],
                    product["name"],
                    product["barcode"],
                    f"{product['sell_price']:.2f}",
                    product["stock"] if product.get("stock_tracked", False) else "N/A",
                ),
            )

        self.status_var.set(f"Search results: {len(products)}")

    def _on_search_select(self, _event: tk.Event) -> None:
        selected = self.search_table.selection()
        self.selected_search_product_id = int(selected[0]) if selected else None

    def _selected_search_product(self) -> dict | None:
        if self.selected_search_product_id is None:
            return None

        for row_id in self.search_table.get_children():
            if int(row_id) == self.selected_search_product_id:
                values = self.search_table.item(row_id, "values")
                return get_product_by_barcode(values[2])
        return None

    def _add_selected_search_product(self, _event: tk.Event | None = None) -> None:
        selected = self.search_table.selection()
        if not selected:
            messagebox.showerror("Invalid input", "Select a search result first", parent=self)
            return

        product_barcode = self.search_table.item(selected[0], "values")[2]
        product = get_product_by_barcode(product_barcode)
        if product is None:
            messagebox.showerror("Invalid input", "Selected product not found", parent=self)
            return

        self._add_product_to_cart(product)

    def _on_scan_enter(self, _event: tk.Event) -> str:
        barcode = self.barcode_var.get().strip()
        self.barcode_var.set("")

        if not barcode:
            self.status_var.set("Empty barcode ignored")
            self.focus_barcode()
            return "break"

        product = get_product_by_barcode(barcode)
        if product is None:
            self.status_var.set(f"Product not found: {barcode}")
            self.focus_barcode()
            return "break"

        if product.get("stock_tracked", False) and product["stock"] <= 0:
            self.status_var.set(f"Out of stock: {product['name']}")
            self.focus_barcode()
            return "break"

        added = self.cart.add_product(product)
        if not added:
            self.status_var.set(f"Stock limit reached: {product['name']}")
        else:
            if product["stock"] <= 10:
                self.status_var.set(f"Added: {product['name']} (low stock)")
            else:
                self.status_var.set(f"Added: {product['name']}")
            self._render_cart()

        self.focus_barcode()
        return "break"

    def _render_cart(self) -> None:
        for row_id in self.cart_table.get_children():
            self.cart_table.delete(row_id)

        item_count = 0
        for item in self.cart.get_items():
            item_count += item["quantity"]
            self.cart_table.insert(
                "",
                tk.END,
                iid=str(item["product_id"]),
                values=(
                    item["product_id"],
                    item["name"],
                    f"{item['price']:.2f}",
                    item["quantity"],
                    f"{item['subtotal']:.2f}",
                    item["stock"] if item.get("stock_tracked", False) else "N/A",
                ),
            )

        self.total_var.set(f"Total: PHP {self.cart.get_total():.2f}")
        self.items_count_var.set(f"Items: {item_count}")

    def _on_table_select(self, _event: tk.Event) -> None:
        selected = self.cart_table.selection()
        self.selected_product_id = int(selected[0]) if selected else None

    def _selected_cart_item(self) -> dict | None:
        if self.selected_product_id is None:
            return None

        for item in self.cart.get_items():
            if item["product_id"] == self.selected_product_id:
                return item
        return None

    def _parse_qty_input(self) -> int | None:
        raw_value = self.qty_var.get().strip()
        if not raw_value:
            messagebox.showerror("Invalid input", "Enter quantity first", parent=self)
            return None

        if not raw_value.isdigit():
            messagebox.showerror("Invalid input", "Quantity must be a whole number", parent=self)
            return None

        value = int(raw_value)
        if value <= 0:
            messagebox.showerror("Invalid input", "Quantity must be at least 1", parent=self)
            return None
        return value

    def _set_selected_quantity(self, _event: tk.Event | None = None) -> None:
        item = self._selected_cart_item()
        if item is None:
            messagebox.showerror("Invalid input", "Select an item first", parent=self)
            return

        qty_value = self._parse_qty_input()
        if qty_value is None:
            return

        self.cart.update_quantity(item["product_id"], qty_value)
        self._render_cart()
        self.status_var.set(f"Quantity updated: {item['name']}")
        self.qty_var.set("1")
        self.focus_barcode()

    def _adjust_selected_quantity(self, step: int) -> None:
        item = self._selected_cart_item()
        if item is None:
            messagebox.showerror("Invalid input", "Select an item first", parent=self)
            return

        new_qty = item["quantity"] + step
        self.cart.update_quantity(item["product_id"], new_qty)
        self._render_cart()
        self.qty_var.set("1")
        self.focus_barcode()

    def _double_click_add_qty(self, _event: tk.Event) -> None:
        self._adjust_selected_quantity(1)

    def _increase_quantity(self) -> None:
        self._adjust_selected_quantity(1)

    def _decrease_quantity(self) -> None:
        self._adjust_selected_quantity(-1)

    def _is_valid_money_text(self, new_text: str) -> bool:
        if new_text == "":
            return True
        if new_text.count(".") > 1:
            return False
        if any(ch not in "0123456789." for ch in new_text):
            return False
        return True

    def _open_payment_modal(self, total: float) -> tuple[float, float] | None:
        modal = tk.Toplevel(self)
        modal.title("Payment")
        width, height = 480, 300
        modal.geometry(f"{width}x{height}")
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.update_idletasks()
        modal.lift()
        modal.focus_force()
        try:
            modal.attributes("-topmost", True)
            modal.after_idle(lambda: modal.attributes("-topmost", False))
        except tk.TclError:
            pass
        self._center_modal(modal, width, height)
        modal.lift()
        modal.wait_visibility()
        modal.grab_set()

        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Checkout Payment", font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(content, text=f"Amount to pay: PHP {total:.2f}").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(6, 8)
        )

        amount_given_var = tk.StringVar()
        change_var = tk.StringVar(value="PHP 0.00")
        error_var = tk.StringVar(value="")
        payment_result: dict[str, float] = {}

        ttk.Label(content, text="Amount given:").grid(row=2, column=0, sticky="w", pady=4)
        validate_cmd = (modal.register(self._is_valid_money_text), "%P")
        amount_entry = ttk.Entry(
            content,
            textvariable=amount_given_var,
            validate="key",
            validatecommand=validate_cmd,
            font=("Segoe UI", 11),
        )
        amount_entry.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(content, text="Change:").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Label(content, textvariable=change_var, font=("Segoe UI", 10, "bold")).grid(
            row=3, column=1, sticky="w", pady=4
        )
        ttk.Label(content, textvariable=error_var, foreground="#b91c1c").grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(4, 8)
        )
        content.columnconfigure(1, weight=1)

        def update_change(*_args) -> None:
            value_text = amount_given_var.get().strip()
            if not value_text:
                change_var.set("PHP 0.00")
                error_var.set("")
                return

            try:
                amount_value = float(value_text)
            except ValueError:
                change_var.set("PHP 0.00")
                error_var.set("Amount given must be numeric")
                return

            change_amount = amount_value - total
            change_var.set(f"PHP {max(change_amount, 0):.2f}")
            if change_amount < 0:
                error_var.set("Amount given cannot be less than amount to pay")
            else:
                error_var.set("")

        amount_given_var.trace_add("write", update_change)

        button_row = ttk.Frame(content)
        button_row.grid(row=5, column=0, columnspan=2, sticky="e", pady=(10, 0))

        def submit_payment() -> None:
            value_text = amount_given_var.get().strip()
            if not value_text:
                error_var.set("Enter amount given")
                return

            try:
                amount_value = float(value_text)
            except ValueError:
                error_var.set("Amount given must be numeric")
                return

            if amount_value < total:
                error_var.set("Amount given cannot be less than amount to pay")
                return

            payment_result["amount_given"] = amount_value
            payment_result["change"] = amount_value - total
            modal.destroy()

        modal.bind("<Return>", lambda _event: submit_payment())

        tk.Button(
            button_row,
            text="Cancel",
            command=modal.destroy,
            bg="#64748b",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            font=("Segoe UI", 11, "bold"),
        ).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(
            button_row,
            text="Pay",
            command=submit_payment,
            bg="#16a34a",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            font=("Segoe UI", 11, "bold"),
        ).pack(side=tk.RIGHT)

        amount_entry.focus_set()
        modal.wait_window()

        if "amount_given" not in payment_result:
            return None
        return payment_result["amount_given"], payment_result["change"]

    def _center_modal(self, modal: tk.Toplevel, width: int, height: int) -> None:
        modal.update_idletasks()
        screen_w = modal.winfo_screenwidth()
        screen_h = modal.winfo_screenheight()
        pos_x = max((screen_w - width) // 2, 0)
        pos_y = max((screen_h - height) // 2, 0)
        modal.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def _remove_selected(self) -> None:
        if self.selected_product_id is None:
            self.status_var.set("Select an item first")
            return

        self.cart.remove_product(self.selected_product_id)
        self.selected_product_id = None
        self._render_cart()
        self.status_var.set("Item removed")
        self.focus_barcode()

    def _clear_cart(self) -> None:
        self.cart.clear()
        self.selected_product_id = None
        self._render_cart()
        self.status_var.set("Cart cleared")
        self.focus_barcode()

    def _checkout(self) -> None:
        items = self.cart.get_items()
        if not items:
            self.status_var.set("Cart is empty")
            self.focus_barcode()
            return

        total = self.cart.get_total()
        payment = self._open_payment_modal(total)
        if payment is None:
            self.status_var.set("Checkout cancelled")
            self.focus_barcode()
            return

        amount_given, change = payment
        try:
            sale_id = complete_sale(items, total, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except ValueError as exc:
            self.status_var.set(str(exc))
            self.focus_barcode()
            return

        self._play_checkout_sound()

        self.cart.clear()
        self.selected_product_id = None
        self._render_cart()
        self.status_var.set(
            f"Sale complete. ID: {sale_id} | Paid: PHP {amount_given:.2f} | Change: PHP {change:.2f}"
        )
        self.focus_barcode()

    def _play_checkout_sound(self) -> None:
        sound_path = self._resource_path("assets", "sounds", "checkout.mp3")
        if not sound_path.exists():
            return

        def play_sound() -> None:
            try:
                import pygame

                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                sound = pygame.mixer.Sound(str(sound_path))
                channel = sound.play()
                if channel is None:
                    return

                while channel.get_busy():
                    time.sleep(0.05)
            except Exception:
                return

        threading.Thread(target=play_sound, daemon=True).start()

    def _resource_path(self, *parts: str) -> Path:
        if getattr(sys, "frozen", False):
            base_dir = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
        else:
            base_dir = Path(__file__).resolve().parents[1]
        return base_dir.joinpath(*parts)

    def _checkout_debt(self) -> None:
        items = self.cart.get_items()
        if not items:
            self.status_var.set("Cart is empty")
            self.focus_barcode()
            return

        total = self.cart.get_total()

        modal = tk.Toplevel(self)
        modal.title("Checkout as Debt")
        width, height = 860, 560
        modal.geometry(f"{width}x{height}")
        modal.resizable(True, True)
        modal.transient(self.winfo_toplevel())
        modal.update_idletasks()
        modal.lift()
        modal.focus_force()
        try:
            modal.attributes("-topmost", True)
            modal.after_idle(lambda: modal.attributes("-topmost", False))
        except tk.TclError:
            pass
        self._center_modal(modal, width, height)
        modal.lift()
        modal.wait_visibility()
        modal.grab_set()

        content = ttk.Frame(modal, padding=12)
        content.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(content)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        right = ttk.Frame(content)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="Customers", font=("Segoe UI", 11, "bold")).pack(anchor="w")

        search_var = tk.StringVar()
        new_customer_var = tk.StringVar()

        search_entry = ttk.Entry(left, textvariable=search_var)
        search_entry.pack(fill=tk.X, pady=(6, 4))

        cust_columns = ("name", "total", "pending")
        cust_table = ttk.Treeview(left, columns=cust_columns, show="headings", height=8)
        cust_table.heading("name", text="Name")
        cust_table.heading("total", text="Total Due")
        cust_table.heading("pending", text="Pending")
        cust_table.column("name", width=160)
        cust_table.column("total", width=80, anchor=tk.E)
        cust_table.column("pending", width=60, anchor=tk.CENTER)
        cust_table.pack(fill=tk.BOTH, expand=True)

        ttk.Label(left, text="New / Search").pack(anchor="w", pady=(6, 0))
        new_entry = ttk.Entry(left, textvariable=new_customer_var)
        new_entry.pack(fill=tk.X, pady=(2, 4))

        def load_customers(filter_text: str = ""):
            for r in cust_table.get_children():
                cust_table.delete(r)
            customers = debt_tracker.get_customers_with_totals()
            for c in customers:
                name = c.get("person_name")
                if filter_text and filter_text.lower() not in name.lower():
                    continue
                total = c.get("total_debt") or 0.0
                pending = c.get("pending_count") or 0
                cust_table.insert("", tk.END, values=(name, f"{total:.2f}", pending))

        def on_search_change(*_args):
            load_customers(search_var.get().strip())

        search_var.trace_add("write", on_search_change)

        def add_customer_action() -> None:
            name = new_customer_var.get().strip()
            if not name:
                messagebox.showerror("Invalid input", "Enter a customer name", parent=modal)
                return
            if debt_tracker.add_customer(name):
                new_customer_var.set("")
                load_customers()
                self.status_var.set(f"Customer '{name}' added")
            else:
                messagebox.showerror("Invalid input", "Failed to add customer or already exists", parent=modal)
                return

        btn_row = ttk.Frame(left)
        btn_row.pack(fill=tk.X, pady=(6, 0))
        tk.Button(btn_row, text="Add", command=add_customer_action, bg="#059669", fg="white", relief=tk.FLAT, padx=10, pady=6).pack(side=tk.LEFT)
        tk.Button(btn_row, text="Close", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=10, pady=6).pack(side=tk.RIGHT)

        # Right: show cart summary and actions
        ttk.Label(right, text="Cart Items to Debt", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        cart_box = ttk.Frame(right)
        cart_box.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

        cart_columns = ("name", "qty", "subtotal")
        debt_items_table = ttk.Treeview(cart_box, columns=cart_columns, show="headings", height=8)
        debt_items_table.heading("name", text="Product")
        debt_items_table.heading("qty", text="Qty")
        debt_items_table.heading("subtotal", text="Amount")
        debt_items_table.column("name", width=360)
        debt_items_table.column("qty", width=60, anchor=tk.CENTER)
        debt_items_table.column("subtotal", width=100, anchor=tk.E)
        debt_items_table.pack(fill=tk.BOTH, expand=True)

        for it in items:
            debt_items_table.insert("", tk.END, values=(it["name"], it["quantity"], f"{it['subtotal']:.2f}"))

        action_row = ttk.Frame(right)
        action_row.pack(fill=tk.X, pady=(8, 0))

        selected_customer = {
            "name": None
        }

        def on_customer_select(_event: tk.Event | None = None):
            sel = cust_table.selection()
            if not sel:
                selected_customer["name"] = None
                return
            values = cust_table.item(sel[0], "values")
            selected_customer["name"] = values[0]

        cust_table.bind("<<TreeviewSelect>>", on_customer_select)

        def submit_debt() -> None:
            name = selected_customer.get("name") or new_customer_var.get().strip()
            if not name:
                messagebox.showerror("Invalid input", "Select or enter a customer name", parent=modal)
                return

            try:
                validate_checkout_stock(items)
            except ValueError as exc:
                messagebox.showerror("Invalid input", str(exc), parent=modal)
                return

            # ensure customer exists
            if not any(c.get("person_name") == name for c in debt_tracker.get_customers_with_totals()):
                debt_tracker.add_customer(name)

            for it in items:
                desc = f"{it['quantity']}x {it['name']}"
                amount = float(it["subtotal"])
                debt_tracker.add_debt(name, amount, desc, True)

            finalize_debt_checkout(items)

            self.cart.clear()
            self._render_cart()
            self.status_var.set(f"Added debt for {name}: PHP {sum(it['subtotal'] for it in items):.2f}")
            modal.destroy()

        tk.Button(action_row, text="Submit as Debt", command=submit_debt, bg="#f59e0b", fg="white", relief=tk.FLAT, padx=12, pady=8).pack(side=tk.RIGHT)

        load_customers()
        new_entry.focus_set()
        modal.wait_window()