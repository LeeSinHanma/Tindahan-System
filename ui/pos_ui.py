import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

from core import checkout_audio, debt_tracker
from core.cart import Cart
from core.inventory import (
    get_product_by_barcode,
    get_quick_access_products,
    search_products,
)
from core.sales import complete_sale, finalize_debt_checkout, validate_checkout_stock
from ui import theme as visual
from ui.widgets import (
    ActionButton,
    AdaptivePanels,
    DataTable,
    FlowFrame,
    center_dialog,
    page_header,
    table,
)


class POSFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        top_level = master.winfo_toplevel()
        self.theme = visual.get_theme()
        self.cart = Cart()
        self.selected_product_id: int | None = None
        self.selected_search_product_id: int | None = None
        self.barcode_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.qty_var = tk.StringVar(value="1")
        self.no_profit_var = tk.BooleanVar(value=False)
        self.total_var = tk.StringVar(value="PHP 0.00")
        self.items_count_var = tk.StringVar(value="Items: 0")
        self.status_var = tk.StringVar(value="Ready: scan a barcode")
        self.quick_access_modal: tk.Toplevel | None = None

        self._build_ui()
        self.after(100, self.focus_barcode)
        top_level.bind("<F1>", self._on_quick_access_hotkey, add="+")
        top_level.bind("<Shift-Return>", self._on_checkout_hotkey, add="+")

    def _build_ui(self) -> None:
        self.configure(padding=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        page_header(
            self, "Point of Sale", "Scan items, review the cart, and complete a sale."
        ).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        scanner = ttk.Frame(self)
        scanner.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        scanner.columnconfigure(1, weight=1)
        ttk.Label(scanner, text="Barcode", style="Section.TLabel").grid(
            row=0, column=0, padx=(0, 12)
        )
        self.barcode_entry = ttk.Entry(
            scanner, textvariable=self.barcode_var, font=(visual.FONT, 12)
        )
        self.barcode_entry.grid(row=0, column=1, sticky="ew")
        self.barcode_entry.bind("<Return>", self._on_scan_enter)
        self.barcode_entry.bind("<Shift-Return>", self._on_checkout_hotkey)
        ActionButton(scanner, text="Find products", command=self._toggle_catalog).grid(
            row=0, column=2, padx=(8, 0)
        )
        ActionButton(
            scanner, text="Quick access · F1", command=self._open_quick_access_modal
        ).grid(row=0, column=3, padx=(8, 0))

        self.workspace = AdaptivePanels(self, breakpoint=1080)
        self.workspace.grid(row=2, column=0, sticky="nsew")
        self.catalog = ttk.LabelFrame(self.workspace, text="Find a product", padding=12)
        self.catalog.columnconfigure(0, weight=1)
        self.catalog.rowconfigure(1, weight=1)
        search_row = ttk.Frame(self.catalog)
        search_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        search_row.columnconfigure(0, weight=1)
        self.search_entry = ttk.Entry(
            search_row, textvariable=self.search_var, width=12
        )
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<Return>", self._on_search_enter)
        ActionButton(search_row, text="Search", command=self._search_products).grid(
            row=0, column=1, padx=(6, 0)
        )
        box, self.search_table = table(
            self.catalog,
            ("id", "name", "barcode", "price", "stock"),
            ("ID", "Product", "Barcode", "Price", "Stock"),
            (40, 165, 140, 80, 60),
            empty_text="Search by product name or barcode.",
            displaycolumns=("name", "price", "stock"),
            height=3,
        )
        box.grid(row=1, column=0, sticky="nsew")
        self.search_table.bind("<<TreeviewSelect>>", self._on_search_select)
        self.search_table.bind("<Double-1>", self._add_selected_search_product)
        self.add_search_button = ActionButton(
            self.catalog,
            text="Add selected item",
            command=self._add_selected_search_product,
            state="disabled",
        )
        self.add_search_button.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        self.cart_panel = ttk.LabelFrame(
            self.workspace, text="Current cart", padding=12
        )
        self.cart_panel.columnconfigure(0, weight=1)
        self.cart_panel.rowconfigure(1, weight=1)
        ttk.Label(
            self.cart_panel, textvariable=self.items_count_var, foreground=visual.MUTED
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        box, self.cart_table = table(
            self.cart_panel,
            ("id", "name", "price", "qty", "subtotal", "stock"),
            ("ID", "Product", "Price", "Qty", "Subtotal", "Stock"),
            (40, 180, 80, 50, 95, 60),
            empty_text="Your cart is empty. Scan a barcode to get started.",
            displaycolumns=("name", "price", "qty", "subtotal"),
            height=4,
        )
        box.grid(row=1, column=0, sticky="nsew")
        self.cart_table.bind("<<TreeviewSelect>>", self._on_table_select)
        self.cart_table.bind("<Double-1>", self._double_click_add_qty)
        tools = FlowFrame(self.cart_panel)
        tools.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        tools.add(ttk.Label(tools, text="Quantity"))
        self.qty_entry = tools.add(
            ttk.Entry(tools, textvariable=self.qty_var, width=4, justify="center")
        )
        self.qty_entry.bind("<Return>", self._set_selected_quantity)
        self.quantity_buttons = []
        for label, command in [
            ("Set", self._set_selected_quantity),
            ("−", self._decrease_quantity),
            ("+", self._increase_quantity),
            ("Remove", self._remove_selected),
        ]:
            self.quantity_buttons.append(
                tools.add(
                    ActionButton(tools, text=label, command=command, state="disabled")
                )
            )

        payment = ttk.Frame(self, style="Panel.TFrame", padding=16)
        payment.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        payment.columnconfigure(0, weight=1)
        ttk.Label(
            payment,
            textvariable=self.total_var,
            style="Panel.TLabel",
            font=(visual.FONT, 24, "bold"),
        ).grid(row=0, column=0, sticky="w")
        self.checkout_button = ActionButton(
            payment,
            text="Checkout  ·  Shift+Enter",
            variant="Primary",
            command=self._checkout,
            state="disabled",
        )
        self.checkout_button.grid(row=0, column=1, sticky="e")
        options = FlowFrame(payment)
        options.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        options.add(
            ttk.Checkbutton(
                options,
                text="Sell at cost",
                variable=self.no_profit_var,
                command=self._toggle_no_profit_pricing,
            )
        )
        self.debt_checkout_button = options.add(
            ActionButton(
                options,
                text="Charge to customer",
                command=self._checkout_debt,
                state="disabled",
            )
        )
        self.clear_button = options.add(
            ActionButton(
                options,
                text="Clear cart",
                variant="Quiet",
                command=self._clear_cart,
                state="disabled",
            )
        )
        options.add(
            ActionButton(
                options, text="Checkout sound", command=self._open_sound_settings
            )
        )
        status = ttk.Label(
            self, textvariable=self.status_var, style="Muted.TLabel", wraplength=700
        )
        status.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        self.bind(
            "<Configure>",
            lambda e: status.configure(wraplength=max(200, e.width)),
            add="+",
        )
        self.workspace.panels = [
            ("Find products", self.catalog),
            ("Current cart", self.cart_panel),
        ]
        self.workspace.show(self.cart_panel)
        self._render_cart()

    def _toggle_catalog(self):
        self.workspace.show(self.catalog)
        self.search_entry.focus_set()

    def _update_cart_actions(self):
        selected = bool(self.cart_table.selection())
        for button in self.quantity_buttons:
            button.configure(state="normal" if selected else "disabled")
        state = "normal" if self.cart.get_items() else "disabled"
        for button in (
            self.checkout_button,
            self.debt_checkout_button,
            self.clear_button,
        ):
            button.configure(state=state)

    def focus_barcode(self) -> None:
        self.barcode_entry.focus_set()
        self.barcode_entry.icursor(tk.END)

    def _on_quick_access_hotkey(self, _event: tk.Event | None = None) -> str:
        if getattr(self.winfo_toplevel(), "active_screen", None) != "pos":
            return ""

        focus_widget = self.focus_get()
        if focus_widget is None:
            return ""

        focus_path = str(focus_widget)
        if not focus_path.startswith(str(self)):
            return ""

        self._open_quick_access_modal()
        return "break"

    def _on_checkout_hotkey(self, _event: tk.Event | None = None) -> str:
        if getattr(self.winfo_toplevel(), "active_screen", None) != "pos":
            return ""

        focus_widget = self.focus_get()
        if focus_widget is None:
            return ""

        focus_path = str(focus_widget)
        if not focus_path.startswith(str(self)):
            return ""

        self._checkout()
        return "break"

    def _open_quick_access_modal(self) -> None:
        if (
            self.quick_access_modal is not None
            and self.quick_access_modal.winfo_exists()
        ):
            self.quick_access_modal.lift()
            return
        modal = tk.Toplevel(self)
        self.quick_access_modal = modal
        modal.title("Quick access")
        modal.transient(self.winfo_toplevel())
        center_dialog(modal, 620, 460)
        modal.columnconfigure(0, weight=1)
        modal.rowconfigure(1, weight=1)
        page_header(
            modal, "Quick access", "Choose an item to add to the current cart."
        ).grid(row=0, column=0, sticky="ew", padx=20, pady=16)
        box, quick_table = table(
            modal,
            ("name", "price", "stock"),
            ("Product", "Price", "Stock"),
            (260, 110, 80),
            empty_text="No quick access items yet. Configure them in Inventory settings.",
        )
        box.grid(row=1, column=0, sticky="nsew", padx=20)
        products = {p["id"]: p for p in get_quick_access_products()}
        for product in products.values():
            quick_table.insert(
                "",
                "end",
                iid=str(product["id"]),
                values=(
                    product["name"],
                    f"PHP {product['sell_price']:,.2f}",
                    product["stock"] if product.get("stock_tracked") else "—",
                ),
            )
        footer = ttk.Frame(modal, padding=20)
        footer.grid(row=2, column=0, sticky="ew")

        def close():
            self.quick_access_modal = None
            modal.destroy()
            self.focus_barcode()

        def add():
            selected = quick_table.selection()
            if selected:
                self._add_product_to_cart(
                    products[int(selected[0])], restore_focus=False
                )

        add_button = ActionButton(
            footer, text="Add to cart", variant="Primary", command=add, state="disabled"
        )
        add_button.pack(side="right")
        ActionButton(footer, text="Done", command=close).pack(side="right", padx=(0, 8))
        quick_table.bind(
            "<<TreeviewSelect>>",
            lambda e: add_button.configure(
                state="normal" if quick_table.selection() else "disabled"
            ),
        )
        quick_table.bind("<Double-1>", lambda e: add())
        quick_table.bind("<Return>", lambda e: add())
        modal.protocol("WM_DELETE_WINDOW", close)
        modal.bind("<Escape>", lambda e: close())
        modal.grab_set()
        quick_table.focus_set()
        modal.wait_window()

    def _add_product_to_cart(self, product: dict, restore_focus: bool = True) -> bool:
        available_stock = int(product.get("sellable_stock", product.get("stock", 0)))
        if product.get("stock_tracked", False) and available_stock <= 0:
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
            self.workspace.show(self.cart_panel)
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

        self.search_table.empty_text = (
            "No products found. Try another name or barcode."
            if search_term
            else "Search by product name or barcode."
        )
        self.search_table._refresh_empty()
        self.status_var.set(f"Search results: {len(products)}")

    def _on_search_select(self, _event: tk.Event) -> None:
        selected = self.search_table.selection()
        self.selected_search_product_id = int(selected[0]) if selected else None
        self.add_search_button.configure(state="normal" if selected else "disabled")

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
            messagebox.showerror(
                "Invalid input", "Select a search result first", parent=self
            )
            return

        product_barcode = self.search_table.item(selected[0], "values")[2]
        product = get_product_by_barcode(product_barcode)
        if product is None:
            messagebox.showerror(
                "Invalid input", "Selected product not found", parent=self
            )
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

        available_stock = int(product.get("sellable_stock", product.get("stock", 0)))
        if product.get("stock_tracked", False) and available_stock <= 0:
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
            self.workspace.show(self.cart_panel)

        self.focus_barcode()
        return "break"

    def _render_cart(self) -> None:
        selected = (
            str(self.selected_product_id)
            if self.selected_product_id is not None
            else None
        )
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

        self.total_var.set(f"PHP {self.cart.get_total():,.2f}")
        if selected and self.cart_table.exists(selected):
            self.cart_table.selection_set(selected)
        else:
            self.selected_product_id = None
        self._update_cart_actions()
        self.items_count_var.set(f"Items: {item_count}")

    def _on_table_select(self, _event: tk.Event) -> None:
        selected = self.cart_table.selection()
        self.selected_product_id = int(selected[0]) if selected else None
        self._update_cart_actions()

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
            messagebox.showerror(
                "Invalid input", "Quantity must be a whole number", parent=self
            )
            return None

        value = int(raw_value)
        if value <= 0:
            messagebox.showerror(
                "Invalid input", "Quantity must be at least 1", parent=self
            )
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

    def _toggle_no_profit_pricing(self) -> None:
        enabled = self.no_profit_var.get()
        self.cart.set_no_profit_pricing(enabled)
        self._render_cart()
        if enabled:
            self.status_var.set("Selling at cost: original prices applied")
        else:
            self.status_var.set("Regular selling prices restored")

    def _reset_no_profit_pricing(self) -> None:
        self.no_profit_var.set(False)
        self.cart.set_no_profit_pricing(False)

    def _is_valid_money_text(self, new_text: str) -> bool:
        if new_text == "":
            return True
        if new_text.count(".") > 1:
            return False
        if any(ch not in "0123456789." for ch in new_text):
            return False
        return True

    def _open_payment_modal(self) -> tuple[float, float, float] | None:
        total = self.cart.get_total()
        modal = tk.Toplevel(self)
        modal.title("Payment")
        width, height = 520, 400
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

        ttk.Label(
            content, text="Checkout Payment", font=(visual.FONT, 13, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        total_text_var = tk.StringVar(value=f"Amount to pay: PHP {total:.2f}")
        ttk.Label(
            content, textvariable=total_text_var, font=(visual.FONT, 18, "bold")
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 8))

        no_profit_checkout_var = tk.BooleanVar(value=self.no_profit_var.get())
        ttk.Checkbutton(
            content,
            text="Sell at cost",
            variable=no_profit_checkout_var,
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 6))

        misc_var = tk.StringVar(value="0")
        amount_given_var = tk.StringVar()
        change_var = tk.StringVar(value="PHP 0.00")
        error_var = tk.StringVar(value="")
        payment_result: dict[str, float] = {}
        validate_cmd = (modal.register(self._is_valid_money_text), "%P")

        ttk.Label(content, text="Additional charge:").grid(
            row=3, column=0, sticky="w", pady=4
        )
        misc_entry = ttk.Entry(
            content,
            textvariable=misc_var,
            validate="key",
            validatecommand=validate_cmd,
            font=(visual.FONT, 11),
        )
        misc_entry.grid(row=3, column=1, sticky="ew", pady=4)

        ttk.Label(content, text="Amount received:").grid(
            row=4, column=0, sticky="w", pady=4
        )
        amount_entry = ttk.Entry(
            content,
            textvariable=amount_given_var,
            validate="key",
            validatecommand=validate_cmd,
            font=(visual.FONT, 11),
        )
        amount_entry.grid(row=4, column=1, sticky="ew", pady=4)

        ttk.Label(content, text="Change:").grid(row=5, column=0, sticky="w", pady=4)
        ttk.Label(
            content, textvariable=change_var, font=(visual.FONT, 10, "bold")
        ).grid(row=5, column=1, sticky="w", pady=4)
        ttk.Label(content, textvariable=error_var, foreground="#b91c1c").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(4, 8)
        )
        content.columnconfigure(1, weight=1)

        def current_total_due() -> float | None:
            misc_text = misc_var.get().strip() or "0"
            try:
                misc_value = float(misc_text)
            except ValueError:
                return None
            if misc_value < 0:
                return None
            return self.cart.get_total() + misc_value

        def update_change(*_args) -> None:
            total_due = current_total_due()
            if total_due is None:
                total_text_var.set("Amount to pay: PHP --")
                change_var.set("PHP 0.00")
                error_var.set("Additional charge must be zero or more")
                return

            total_text_var.set(f"Amount to pay: PHP {total_due:.2f}")
            value_text = amount_given_var.get().strip()
            if not value_text:
                change_var.set("PHP 0.00")
                error_var.set("")
                return

            try:
                amount_value = float(value_text)
            except ValueError:
                change_var.set("PHP 0.00")
                error_var.set("Enter a valid amount received")
                return

            change_amount = amount_value - total_due
            change_var.set(f"PHP {max(change_amount, 0):.2f}")
            if change_amount < 0:
                error_var.set("Amount received is below the amount due")
            else:
                error_var.set("")

        def on_toggle_no_profit() -> None:
            enabled = no_profit_checkout_var.get()
            self.no_profit_var.set(enabled)
            self.cart.set_no_profit_pricing(enabled)
            self._render_cart()
            update_change()

        no_profit_checkout_var.trace_add("write", lambda *_args: on_toggle_no_profit())

        misc_var.trace_add("write", update_change)
        amount_given_var.trace_add("write", update_change)

        button_row = ttk.Frame(content)
        button_row.grid(row=7, column=0, columnspan=2, sticky="e", pady=(10, 0))

        def submit_payment() -> None:
            value_text = amount_given_var.get().strip()
            if not value_text:
                error_var.set("Enter the amount received")
                return

            try:
                amount_value = float(value_text)
            except ValueError:
                error_var.set("Enter a valid amount received")
                return

            total_due = current_total_due()
            if total_due is None:
                error_var.set("Additional charge must be zero or more")
                return

            if amount_value < total_due:
                error_var.set("Amount received is below the amount due")
                return

            payment_result["amount_given"] = amount_value
            payment_result["change"] = amount_value - total_due
            payment_result["total_due"] = total_due
            modal.destroy()

        modal.bind("<Return>", lambda _event: submit_payment())

        ActionButton(
            button_row,
            text="Cancel",
            command=modal.destroy,
            bg="#64748b",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            font=(visual.FONT, 11, "bold"),
        ).pack(side=tk.RIGHT, padx=(8, 0))
        ActionButton(
            button_row,
            text="Complete sale",
            command=submit_payment,
            bg="#16a34a",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            font=(visual.FONT, 11, "bold"),
        ).pack(side=tk.RIGHT)

        amount_entry.focus_set()
        modal.wait_window()

        if "amount_given" not in payment_result:
            return None
        return (
            payment_result["amount_given"],
            payment_result["change"],
            payment_result["total_due"],
        )

    def _center_modal(self, modal, width, height):
        center_dialog(modal, width, height)

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
        self._reset_no_profit_pricing()
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

        payment = self._open_payment_modal()
        if payment is None:
            self.status_var.set("Checkout cancelled")
            self.focus_barcode()
            return

        amount_given, change, total_due = payment
        items = self.cart.get_items()
        try:
            sale_id = complete_sale(
                items, total_due, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        except ValueError as exc:
            self.status_var.set(str(exc))
            self.focus_barcode()
            return

        self._play_checkout_sound()

        self.cart.clear()
        self._reset_no_profit_pricing()
        self.selected_product_id = None
        self._render_cart()
        self.status_var.set(
            f"Sale complete. ID: {sale_id} | Paid: PHP {amount_given:.2f} | Change: PHP {change:.2f}"
        )
        self.focus_barcode()

    def _play_checkout_sound(self) -> None:
        checkout_audio.play_checkout_sound()

    def _open_sound_settings(self) -> None:
        modal = tk.Toplevel(self)
        modal.title("Checkout sound")
        modal.transient(self.winfo_toplevel())
        modal.resizable(False, False)
        modal.grab_set()
        content = ttk.Frame(modal, padding=24)
        content.pack(fill="both", expand=True)
        ttk.Label(content, text="Checkout sound", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            content,
            text="Choose your own sound to play after a completed cash sale.",
            style="Muted.TLabel",
            wraplength=450,
        ).pack(anchor="w", pady=(6, 18))
        name_var = tk.StringVar()
        enabled_var = tk.BooleanVar()
        feedback_var = tk.StringVar()
        ttk.Label(content, textvariable=name_var, wraplength=450).pack(
            anchor="w", pady=(0, 12)
        )

        def refresh():
            info = checkout_audio.sound_info()
            filename = info["name"]
            if len(filename) > 80:
                filename = filename[:77] + "…"
            name_var.set(
                filename
                if info["available"]
                else (
                    "Saved sound is missing. Choose a file again."
                    if info["name"]
                    else "No sound selected. Checkout is silent."
                )
            )
            enabled_var.set(info["enabled"])
            enabled.configure(state="normal" if info["available"] else "disabled")
            preview.configure(state="normal" if info["available"] else "disabled")
            remove.configure(state="normal" if info["path"] is not None else "disabled")

        def toggle():
            try:
                checkout_audio.set_enabled(enabled_var.get())
                feedback_var.set(
                    "Sound enabled." if enabled_var.get() else "Checkout sound muted."
                )
            except checkout_audio.AudioError as exc:
                feedback_var.set(str(exc))
            refresh()

        enabled = ttk.Checkbutton(
            content,
            text="Play sound after checkout",
            variable=enabled_var,
            command=toggle,
        )
        enabled.pack(anchor="w")
        controls = FlowFrame(content)
        controls.pack(fill="x", pady=(16, 10))

        def choose():
            filename = filedialog.askopenfilename(
                parent=modal,
                title="Choose checkout sound",
                filetypes=[("Audio files", "*.wav *.ogg *.mp3"), ("All files", "*.*")],
            )
            if not filename:
                return
            try:
                checkout_audio.choose_sound(filename)
                feedback_var.set("Sound saved. Use Preview to listen.")
            except (checkout_audio.AudioError, OSError) as exc:
                feedback_var.set(str(exc))
            refresh()

        def listen():
            try:
                checkout_audio.preview_sound()
                feedback_var.set("Playing preview.")
            except (checkout_audio.AudioError, OSError) as exc:
                feedback_var.set(str(exc))

        def clear():
            checkout_audio.remove_sound()
            feedback_var.set("Sound removed. Checkout is silent.")
            refresh()

        controls.add(
            ActionButton(
                controls, text="Choose file", variant="Primary", command=choose
            )
        )
        preview = controls.add(ActionButton(controls, text="Preview", command=listen))
        controls.add(
            ActionButton(controls, text="Stop", command=checkout_audio.stop_playback)
        )
        remove = controls.add(
            ActionButton(controls, text="Remove", variant="Quiet", command=clear)
        )
        ttk.Label(
            content,
            text="WAV, OGG, or MP3 · up to 10 MB. Your file is copied locally, so it keeps working if the original moves.",
            style="Muted.TLabel",
            wraplength=450,
        ).pack(anchor="w", pady=(4, 12))
        ttk.Label(content, textvariable=feedback_var, wraplength=450).pack(
            anchor="w", fill="x"
        )

        def close():
            checkout_audio.stop_playback()
            modal.destroy()

        ActionButton(content, text="Done", command=close).pack(anchor="e", pady=(14, 0))
        refresh()
        center_dialog(modal, 520, 440)
        modal.bind("<Escape>", lambda event: close())
        modal.protocol("WM_DELETE_WINDOW", close)

    def _checkout_debt(self) -> None:
        items = self.cart.get_items()
        if not items:
            self.status_var.set("Cart is empty")
            self.focus_barcode()
            return

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

        ttk.Label(left, text="Customers", font=(visual.FONT, 11, "bold")).pack(
            anchor="w"
        )

        search_var = tk.StringVar()
        new_customer_var = tk.StringVar()

        search_entry = ttk.Entry(left, textvariable=search_var)
        search_entry.pack(fill=tk.X, pady=(6, 4))

        cust_columns = ("name", "total", "pending")
        cust_table = DataTable(left, columns=cust_columns, show="headings", height=8)
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
                messagebox.showerror(
                    "Invalid input", "Enter a customer name", parent=modal
                )
                return
            if debt_tracker.add_customer(name):
                new_customer_var.set("")
                load_customers()
                self.status_var.set(f"Customer '{name}' added")
            else:
                messagebox.showerror(
                    "Invalid input",
                    "Failed to add customer or already exists",
                    parent=modal,
                )
                return

        btn_row = ttk.Frame(left)
        btn_row.pack(fill=tk.X, pady=(6, 0))
        ActionButton(
            btn_row,
            text="Add",
            command=add_customer_action,
            bg="#059669",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=6,
        ).pack(side=tk.LEFT)
        ActionButton(
            btn_row,
            text="Close",
            command=modal.destroy,
            bg="#64748b",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=6,
        ).pack(side=tk.RIGHT)

        # Right: show cart summary and actions
        ttk.Label(
            right, text="Cart Items to Debt", font=(visual.FONT, 11, "bold")
        ).pack(anchor="w")
        cart_box = ttk.Frame(right)
        cart_box.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

        cart_columns = ("name", "qty", "subtotal")
        debt_items_table = DataTable(
            cart_box, columns=cart_columns, show="headings", height=8
        )
        debt_items_table.heading("name", text="Product")
        debt_items_table.heading("qty", text="Qty")
        debt_items_table.heading("subtotal", text="Amount")
        debt_items_table.column("name", width=360)
        debt_items_table.column("qty", width=60, anchor=tk.CENTER)
        debt_items_table.column("subtotal", width=100, anchor=tk.E)
        debt_items_table.pack(fill=tk.BOTH, expand=True)

        for it in items:
            debt_items_table.insert(
                "", tk.END, values=(it["name"], it["quantity"], f"{it['subtotal']:.2f}")
            )

        action_row = ttk.Frame(right)
        action_row.pack(fill=tk.X, pady=(8, 0))

        selected_customer = {"name": None}

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
                messagebox.showerror(
                    "Invalid input", "Select or enter a customer name", parent=modal
                )
                return

            try:
                validate_checkout_stock(items)
            except ValueError as exc:
                messagebox.showerror("Invalid input", str(exc), parent=modal)
                return

            # ensure customer exists
            if not any(
                c.get("person_name") == name
                for c in debt_tracker.get_customers_with_totals()
            ):
                debt_tracker.add_customer(name)

            try:
                finalize_debt_checkout(items)
            except ValueError as exc:
                messagebox.showerror("Invalid input", str(exc), parent=modal)
                return

            for it in items:
                desc = f"{it['quantity']}x {it['name']}"
                amount = float(it["subtotal"])
                debt_tracker.add_debt(name, amount, desc, True)

            self.cart.clear()
            self._reset_no_profit_pricing()
            self._render_cart()
            self.status_var.set(
                f"Added debt for {name}: PHP {sum(it['subtotal'] for it in items):.2f}"
            )
            modal.destroy()

        ActionButton(
            action_row,
            text="Submit as Debt",
            command=submit_debt,
            bg="#f59e0b",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=8,
        ).pack(side=tk.RIGHT)

        load_customers()
        new_entry.focus_set()
        modal.wait_window()
