import tkinter as tk
from tkinter import messagebox, ttk

from core import inventory
from .theme_manager import ThemeManager


class InventoryFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        top_level = master.winfo_toplevel()
        screen_w = top_level.winfo_screenwidth()
        screen_h = top_level.winfo_screenheight()
        self.compact_layout = screen_w < 1400 or screen_h < 820
        self.theme = ThemeManager(self.compact_layout)
        self.selected_product_id: int | None = None
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Select a product, then use Create / Update / Delete")
        self.show_only_untracked_var = tk.BooleanVar(value=False)
        self.search_entry: ttk.Entry | None = None

        self._build_ui()
        self.refresh_products()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X)

        ttk.Label(header, text="Inventory CRUD", font=("Segoe UI", self.theme.heading_huge, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="Create products from a modal form, update stock with buttons, or delete with confirmation.",
            font=("Segoe UI", self.theme.body_medium),
        ).pack(anchor="w", pady=(4, 0))

        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=(12, 10))

        search_row = ttk.Frame(toolbar)
        search_row.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(search_row, text="Search name / barcode:", font=("Segoe UI", 13, "bold")).pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_row, textvariable=self.search_var, font=("Segoe UI", 13))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 8))
        self.search_entry.bind("<Return>", self._on_search)

        self._create_toolbar_button(toolbar, "Search", self._on_search, "#1d4ed8").pack(side=tk.LEFT, padx=(0, 8))
        self._create_toolbar_button(toolbar, "Show All", self._show_all, "#64748b").pack(side=tk.LEFT)
        self._create_toolbar_button(toolbar, "Untracked Items", self._show_untracked, "#4f46e5").pack(side=tk.LEFT, padx=(8, 0))
        self._create_toolbar_button(toolbar, "Settings", self._open_settings_modal, "#a855f7").pack(side=tk.LEFT, padx=(8, 0))
        self._create_toolbar_button(toolbar, "Restock", self._open_restock_modal, "#0ea5e9").pack(side=tk.LEFT, padx=(8, 0))
        self._create_toolbar_button(toolbar, "Create", self._open_create_modal, "#16a34a").pack(side=tk.RIGHT, padx=(8, 0))
        self._create_toolbar_button(toolbar, "Delete", self._open_delete_modal, "#dc2626").pack(side=tk.RIGHT, padx=(8, 0))
        self._create_toolbar_button(toolbar, "Update", self._open_update_modal, "#f59e0b").pack(side=tk.RIGHT, padx=(8, 0))

        table_box = ttk.Frame(self)
        table_box.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "barcode", "original_price", "sell_price", "stock", "tracked")
        self.product_table = ttk.Treeview(table_box, columns=columns, show="headings", height=20)
        self.product_table.heading("id", text="ID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("barcode", text="Barcode")
        self.product_table.heading("original_price", text="Orig. Price")
        self.product_table.heading("sell_price", text="Sell Price")
        self.product_table.heading("stock", text="Stock")
        self.product_table.heading("tracked", text="Tracked")

        self.product_table.column("id", width=45, anchor=tk.CENTER)
        self.product_table.column("name", width=160, anchor=tk.W)
        self.product_table.column("barcode", width=100, anchor=tk.W)
        self.product_table.column("original_price", width=75, anchor=tk.E)
        self.product_table.column("sell_price", width=75, anchor=tk.E)
        self.product_table.column("stock", width=60, anchor=tk.CENTER)
        self.product_table.column("tracked", width=60, anchor=tk.CENTER)
        self.product_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(table_box, orient=tk.VERTICAL, command=self.product_table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_table.configure(yscrollcommand=scrollbar.set)

        self.product_table.tag_configure("low_stock", background="#fff2cc")
        self.product_table.tag_configure("untracked", background="#e0e7ff")
        self.product_table.bind("<<TreeviewSelect>>", self._on_row_select)
        self.product_table.bind("<Double-1>", self._open_update_modal)

        footer = ttk.Frame(self)
        footer.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(footer, textvariable=self.status_var).pack(side=tk.LEFT)

    def _create_toolbar_button(self, parent: tk.Widget, text: str, command, color: str) -> tk.Button:
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
            font=("Segoe UI", self.theme.body_medium, "bold"),
            cursor="hand2",
        )

    def _open_modal_shell(self, title: str, width: int = 520, height: int = 420) -> tk.Toplevel:
        modal = tk.Toplevel(self)
        modal.title(title)
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
        return modal

    def _center_modal(self, modal: tk.Toplevel, width: int, height: int) -> None:
        modal.update_idletasks()
        screen_w = modal.winfo_screenwidth()
        screen_h = modal.winfo_screenheight()
        pos_x = max((screen_w - width) // 2, 0)
        pos_y = max((screen_h - height) // 2, 0)
        modal.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def _field_row(self, parent: tk.Widget, label_text: str, variable: tk.StringVar, row: int) -> ttk.Entry:
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=6, padx=(0, 10))
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky="ew", pady=6)
        return entry

    def _product_payload(self) -> dict:
        return {
            "name": self._create_vars["name"].get(),
            "description": self._create_vars["description"].get(),
            "barcode": self._create_vars["barcode"].get(),
            "original_price": self._create_vars["original_price"].get(),
            "sell_price": self._create_vars["sell_price"].get(),
            "stock": self._create_vars["stock"].get(),
            "stock_tracked": self._create_vars["stock_tracked"].get(),
        }

    def _resolve_parent_link(self, current_product_id: int | None, current_barcode: str, vars_map: dict[str, tk.Variable]) -> dict:
        if not bool(vars_map["parent_linked"].get()):
            return {"parent_product_id": None, "parent_units": 1}

        parent_barcode = str(vars_map["parent_barcode"].get()).strip()
        if not parent_barcode:
            raise ValueError("Enter the parent item barcode")

        parent_product = inventory.get_product_by_barcode(parent_barcode)
        if parent_product is None:
            raise ValueError("Parent product not found")

        if current_product_id is not None and parent_product["id"] == current_product_id:
            raise ValueError("A product cannot be its own parent")

        if current_barcode and parent_product["barcode"] == current_barcode:
            raise ValueError("A product cannot be its own parent")

        try:
            parent_units = int(str(vars_map["parent_units"].get()).strip() or "1")
        except ValueError:
            raise ValueError("Parent units must be a whole number")

        if parent_units <= 0:
            raise ValueError("Parent units must be at least 1")

        return {"parent_product_id": parent_product["id"], "parent_units": parent_units}

    def _selected_product(self) -> dict | None:
        if self.selected_product_id is None:
            return None
        return inventory.get_product_by_id(self.selected_product_id)

    def _show_all(self) -> None:
        self.show_only_untracked_var.set(False)
        self.search_var.set("")
        self.refresh_products()

    def _show_untracked(self) -> None:
        self.show_only_untracked_var.set(True)
        self.refresh_products(self.search_var.get())

    def _on_search(self, _event: tk.Event | None = None) -> None:
        self.refresh_products(self.search_var.get())

    def focus_search(self) -> None:
        if self.search_entry:
            self.search_entry.focus()

    def _on_row_select(self, _event: tk.Event) -> None:
        selected = self.product_table.selection()
        self.selected_product_id = int(selected[0]) if selected else None

    def refresh_products(self, search_term: str | None = None) -> None:
        term = self.search_var.get() if search_term is None else search_term
        if self.show_only_untracked_var.get():
            products = inventory.get_untracked_products(term)
        else:
            products = inventory.search_products(term) if term.strip() else inventory.list_products()

        for row_id in self.product_table.get_children():
            self.product_table.delete(row_id)

        for product in products:
            if not product.get("stock_tracked", False):
                tags = ("untracked",)
            else:
                tags = ("low_stock",) if product["stock"] <= inventory.get_low_stock_threshold() else ()
            self.product_table.insert(
                "",
                tk.END,
                iid=str(product["id"]),
                values=(
                    product["id"],
                    product["name"],
                    product["barcode"],
                    f"{product['original_price']:.2f}",
                    f"{product['sell_price']:.2f}",
                    product["stock"],
                    "Yes" if product.get("stock_tracked", False) else "No",
                ),
                tags=tags,
            )

        low_stock_count = len(inventory.get_low_stock_products())
        self.status_var.set(f"Loaded {len(products)} products. Low stock: {low_stock_count}")

    def _open_create_modal(self) -> None:
        modal = self._open_modal_shell("Create Product", 540, 640)

        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Create Product", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(content, text="Enter the product information below.", font=("Segoe UI", 12)).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 12))

        self._create_vars = {
            "name": tk.StringVar(),
            "description": tk.StringVar(),
            "barcode": tk.StringVar(),
            "original_price": tk.StringVar(),
            "sell_price": tk.StringVar(),
            "stock": tk.StringVar(),
            "stock_tracked": tk.BooleanVar(value=False),
            "parent_linked": tk.BooleanVar(value=False),
            "parent_barcode": tk.StringVar(),
            "parent_units": tk.StringVar(value="1"),
        }

        content.columnconfigure(1, weight=1)
        self._field_row(content, "Name", self._create_vars["name"], 2)
        self._field_row(content, "Description", self._create_vars["description"], 3)
        self._field_row(content, "Barcode", self._create_vars["barcode"], 4)

        # Original Price field + suggested hint
        ttk.Label(content, text="Original Price").grid(row=5, column=0, sticky="w", pady=6, padx=(0, 10))
        orig_entry = ttk.Entry(content, textvariable=self._create_vars["original_price"])
        orig_entry.grid(row=5, column=1, sticky="ew", pady=6)
        self._create_suggest_orig = ttk.Label(content, text="", font=("Segoe UI", 9, "italic"))
        self._create_suggest_orig.grid(row=6, column=0, columnspan=2, sticky="w")

        # Sell Price field + suggested hint
        ttk.Label(content, text="Sell Price").grid(row=7, column=0, sticky="w", pady=6, padx=(0, 10))
        sell_entry = ttk.Entry(content, textvariable=self._create_vars["sell_price"])
        sell_entry.grid(row=7, column=1, sticky="ew", pady=6)
        self._create_suggest_sell = ttk.Label(content, text="", font=("Segoe UI", 9, "italic"))
        self._create_suggest_sell.grid(row=8, column=0, columnspan=2, sticky="w")

        # Stock field moved down
        self._field_row(content, "Stock", self._create_vars["stock"], 9)

        tracking_row = ttk.Frame(content)
        tracking_row.grid(row=10, column=0, columnspan=2, sticky="w", pady=(4, 8))
        ttk.Checkbutton(
            tracking_row,
            text="Track stock for this product",
            variable=self._create_vars["stock_tracked"],
        ).pack(anchor="w")
        ttk.Label(
            tracking_row,
            text="Unchecked means the item can be sold without stock counting.",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 0))

        parent_row = ttk.Frame(content)
        parent_row.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        ttk.Checkbutton(
            parent_row,
            text="Link stock to a parent item",
            variable=self._create_vars["parent_linked"],
        ).pack(anchor="w")

        self._field_row(content, "Parent Barcode", self._create_vars["parent_barcode"], 12)
        self._field_row(content, "Units per Parent", self._create_vars["parent_units"], 13)

        button_row = ttk.Frame(content)
        button_row.grid(row=14, column=0, columnspan=2, sticky="e", pady=(18, 0))

        def submit() -> None:
            try:
                payload = self._product_payload()
                payload.update(self._resolve_parent_link(None, payload["barcode"], self._create_vars))
                product_id = inventory.create_product(payload)
            except ValueError as exc:
                messagebox.showerror("Validation error", str(exc), parent=modal)
                return

            modal.destroy()
            self.refresh_products()
            self.status_var.set(f"Product created: {product_id}")

        tk.Button(button_row, text="Cancel", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(button_row, text="Add", command=submit, bg="#16a34a", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)

        # Suggestion logic: 20% markup (sell = orig * 1.2); vice versa orig = sell / 1.2
        def _safe_float(val: str) -> float | None:
            try:
                return float(val)
            except (ValueError, TypeError):
                return None

        def _update_create_suggestions(*_args) -> None:
            orig = _safe_float(self._create_vars["original_price"].get())
            sell = _safe_float(self._create_vars["sell_price"].get())

            if orig is not None and (sell is None or sell == 0):
                suggested = orig * 1.2
                self._create_suggest_sell.config(text=f"Suggested sell price: {suggested:.2f} (20% markup)")
            else:
                self._create_suggest_sell.config(text="")

            if sell is not None and (orig is None or orig == 0):
                suggested_orig = sell / 1.2
                self._create_suggest_orig.config(text=f"Suggested original price: {suggested_orig:.2f} (≈ sell/1.2)")
            else:
                self._create_suggest_orig.config(text="")

        self._create_vars["original_price"].trace_add("write", _update_create_suggestions)
        self._create_vars["sell_price"].trace_add("write", _update_create_suggestions)

    def _open_update_modal(self, _event: tk.Event | None = None) -> None:
        product = self._selected_product()
        if product is None:
            messagebox.showinfo("Update product", "Select a product first.", parent=self)
            return

        modal = self._open_modal_shell("Update Product", 560, 680)
        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Update Product", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(content, text=f"Selected: {product['name']} (ID {product['id']})", font=("Segoe UI", 12)).grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 12))

        vars_map = {
            "name": tk.StringVar(value=product["name"]),
            "description": tk.StringVar(value=product["description"]),
            "barcode": tk.StringVar(value=product["barcode"]),
            "original_price": tk.StringVar(value=f"{product['original_price']:.2f}"),
            "sell_price": tk.StringVar(value=f"{product['sell_price']:.2f}"),
            "stock": tk.StringVar(value=str(product["stock"])),
            "stock_tracked": tk.BooleanVar(value=bool(product.get("stock_tracked", False))),
            "parent_linked": tk.BooleanVar(value=bool(product.get("parent_product_id") is not None)),
            "parent_barcode": tk.StringVar(),
            "parent_units": tk.StringVar(value=str(product.get("parent_units", 1))),
        }

        if product.get("parent_product_id") is not None:
            parent_product = inventory.get_product_by_id(int(product["parent_product_id"]))
            if parent_product is not None:
                vars_map["parent_barcode"].set(parent_product["barcode"])

        self._update_vars = vars_map

        content.columnconfigure(1, weight=1)
        self._field_row(content, "Name", vars_map["name"], 2)
        self._field_row(content, "Description", vars_map["description"], 3)
        self._field_row(content, "Barcode", vars_map["barcode"], 4)

        # Original Price + suggestion
        ttk.Label(content, text="Original Price").grid(row=5, column=0, sticky="w", pady=6, padx=(0, 10))
        orig_entry = ttk.Entry(content, textvariable=vars_map["original_price"])
        orig_entry.grid(row=5, column=1, sticky="ew", pady=6)
        self._update_suggest_orig = ttk.Label(content, text="", font=("Segoe UI", 9, "italic"))
        self._update_suggest_orig.grid(row=6, column=0, columnspan=2, sticky="w")

        # Sell Price + suggestion
        ttk.Label(content, text="Sell Price").grid(row=7, column=0, sticky="w", pady=6, padx=(0, 10))
        sell_entry = ttk.Entry(content, textvariable=vars_map["sell_price"])
        sell_entry.grid(row=7, column=1, sticky="ew", pady=6)
        self._update_suggest_sell = ttk.Label(content, text="", font=("Segoe UI", 9, "italic"))
        self._update_suggest_sell.grid(row=8, column=0, columnspan=2, sticky="w")

        # Stock field moved down
        self._field_row(content, "Stock", vars_map["stock"], 9)

        tracking_row = ttk.Frame(content)
        tracking_row.grid(row=10, column=0, columnspan=2, sticky="w", pady=(4, 8))
        ttk.Checkbutton(
            tracking_row,
            text="Track stock for this product",
            variable=vars_map["stock_tracked"],
        ).pack(anchor="w")
        ttk.Label(
            tracking_row,
            text="If off, the product can still be scanned and sold.",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 0))

        parent_row = ttk.Frame(content)
        parent_row.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        ttk.Checkbutton(
            parent_row,
            text="Link stock to a parent item",
            variable=vars_map["parent_linked"],
        ).pack(anchor="w")

        self._field_row(content, "Parent Barcode", vars_map["parent_barcode"], 12)
        self._field_row(content, "Units per Parent", vars_map["parent_units"], 13)

        stock_buttons = ttk.Frame(content)
        stock_buttons.grid(row=14, column=0, columnspan=2, sticky="w", pady=(6, 10))

        def add_stock() -> None:
            try:
                current_stock = int(vars_map["stock"].get() or 0)
                vars_map["stock"].set(str(current_stock + 1))
            except ValueError:
                messagebox.showerror("Stock error", "Stock must be a whole number.", parent=modal)

        def remove_stock() -> None:
            try:
                current_stock = int(vars_map["stock"].get() or 0)
            except ValueError:
                messagebox.showerror("Stock error", "Stock must be a whole number.", parent=modal)
                return

            if current_stock > 0:
                vars_map["stock"].set(str(current_stock - 1))

        def clear_stock() -> None:
            vars_map["stock"].set("0")

        tk.Button(stock_buttons, text="Add Stock", command=add_stock, bg="#2563eb", fg="white", relief=tk.FLAT, padx=14, pady=8, font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT)
        tk.Button(stock_buttons, text="Remove Stock", command=remove_stock, bg="#dc2626", fg="white", relief=tk.FLAT, padx=14, pady=8, font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(8, 0))
        tk.Button(stock_buttons, text="Clear Stock", command=clear_stock, bg="#475569", fg="white", relief=tk.FLAT, padx=14, pady=8, font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(8, 0))

        button_row = ttk.Frame(content)
        button_row.grid(row=15, column=0, columnspan=2, sticky="e", pady=(18, 0))

        def submit() -> None:
            if not messagebox.askyesno(
                "Confirm update",
                f"Save changes to {product['name']}?",
                parent=modal,
            ):
                return

            try:
                payload = {key: value.get() for key, value in vars_map.items()}
                payload.update(self._resolve_parent_link(product["id"], payload["barcode"], vars_map))
                inventory.update_product(product["id"], payload)
            except ValueError as exc:
                messagebox.showerror("Validation error", str(exc), parent=modal)
                return

            modal.destroy()
            self.refresh_products(self.search_var.get())
            self.status_var.set(f"Product updated: {product['name']}")

        tk.Button(button_row, text="Cancel", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(button_row, text="Update", command=submit, bg="#f59e0b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)

        # Suggestion logic for update modal
        def _safe_float_update(val: str) -> float | None:
            try:
                return float(val)
            except (ValueError, TypeError):
                return None

        def _update_update_suggestions(*_args) -> None:
            orig = _safe_float_update(vars_map["original_price"].get())
            sell = _safe_float_update(vars_map["sell_price"].get())

            if orig is not None and (sell is None or sell == 0):
                suggested = orig * 1.2
                self._update_suggest_sell.config(text=f"Suggested sell price: {suggested:.2f} (20% markup)")
            else:
                self._update_suggest_sell.config(text="")

            if sell is not None and (orig is None or orig == 0):
                suggested_orig = sell / 1.2
                self._update_suggest_orig.config(text=f"Suggested original price: {suggested_orig:.2f} (≈ sell/1.2)")
            else:
                self._update_suggest_orig.config(text="")

        vars_map["original_price"].trace_add("write", _update_update_suggestions)
        vars_map["sell_price"].trace_add("write", _update_update_suggestions)

    def _open_restock_modal(self) -> None:
        modal = self._open_modal_shell("Restock Product", 640, 430)
        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(1, weight=1)

        ttk.Label(content, text="Restock Product", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(
            content,
            text="Scan a barcode, review the product, enter the restock quantity, then confirm.",
            font=("Segoe UI", 12),
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 12))

        barcode_var = tk.StringVar()
        qty_var = tk.StringVar(value="1")
        product_summary_var = tk.StringVar(value="Scan a barcode to load a product.")
        loaded_product: dict | None = None

        ttk.Label(content, text="Barcode").grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        barcode_entry = ttk.Entry(content, textvariable=barcode_var, font=("Consolas", 12))
        barcode_entry.grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(content, text="Item").grid(row=3, column=0, sticky="nw", pady=(10, 0), padx=(0, 10))
        summary_box = ttk.LabelFrame(content, text="Scanned Item", padding=10)
        summary_box.grid(row=3, column=1, sticky="ew", pady=(10, 0))
        summary_box.columnconfigure(0, weight=1)
        ttk.Label(summary_box, textvariable=product_summary_var, wraplength=430, justify=tk.LEFT).grid(row=0, column=0, sticky="w")

        ttk.Label(content, text="Quantity").grid(row=4, column=0, sticky="w", pady=6, padx=(0, 10))
        qty_entry = ttk.Entry(content, textvariable=qty_var, width=10)
        qty_entry.grid(row=4, column=1, sticky="w", pady=6)

        status_var = tk.StringVar(value="")
        ttk.Label(content, textvariable=status_var, foreground="#64748b").grid(row=5, column=0, columnspan=2, sticky="w", pady=(8, 0))

        button_row = ttk.Frame(content)
        button_row.grid(row=6, column=0, columnspan=2, sticky="e", pady=(18, 0))

        def _parse_qty() -> int | None:
            raw_value = qty_var.get().strip()
            if not raw_value:
                messagebox.showerror("Invalid input", "Enter a quantity to restock.", parent=modal)
                return None
            if not raw_value.isdigit():
                messagebox.showerror("Invalid input", "Quantity must be a whole number.", parent=modal)
                return None

            quantity = int(raw_value)
            if quantity <= 0:
                messagebox.showerror("Invalid input", "Quantity must be at least 1.", parent=modal)
                return None
            return quantity

        def load_product() -> None:
            nonlocal loaded_product
            barcode = barcode_var.get().strip()
            if not barcode:
                loaded_product = None
                product_summary_var.set("Enter or scan a barcode first.")
                status_var.set("")
                return

            product = inventory.get_product_by_barcode(barcode)
            if product is None:
                loaded_product = None
                product_summary_var.set(f"No product found for barcode: {barcode}")
                status_var.set("")
                return

            loaded_product = product
            product_summary_var.set(
                f"{product['name']}\n"
                f"Barcode: {product['barcode']}\n"
                f"Current stock: {product['stock']}\n"
                f"Tracked: {'Yes' if product.get('stock_tracked', False) else 'No'}"
            )
            status_var.set(f"Loaded: {product['name']}")
            qty_entry.focus_set()
            qty_entry.selection_range(0, tk.END)

        def restock_product() -> None:
            nonlocal loaded_product
            if loaded_product is None:
                messagebox.showerror("Invalid input", "Scan a barcode first.", parent=modal)
                return

            quantity = _parse_qty()
            if quantity is None:
                return

            if not messagebox.askyesno(
                "Confirm restock",
                f"Add {quantity} to stock for {loaded_product['name']}?",
                parent=modal,
            ):
                return

            try:
                new_stock = inventory.adjust_stock(loaded_product["id"], quantity)
            except ValueError as exc:
                messagebox.showerror("Restock error", str(exc), parent=modal)
                return

            self.refresh_products(self.search_var.get())
            self.status_var.set(f"Restocked {loaded_product['name']} by {quantity}. New stock: {new_stock}")
            loaded_product = None
            barcode_var.set("")
            qty_var.set("1")
            product_summary_var.set("Scan a barcode to load a product.")
            barcode_entry.focus_set()

        barcode_entry.bind("<Return>", lambda _event: load_product())
        qty_entry.bind("<Return>", lambda _event: restock_product())

        tk.Button(
            button_row,
            text="Load Item",
            command=load_product,
            bg="#1d4ed8",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            font=("Segoe UI", 11, "bold"),
        ).pack(side=tk.LEFT)
        tk.Button(
            button_row,
            text="Restock",
            command=restock_product,
            bg="#0ea5e9",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            font=("Segoe UI", 11, "bold"),
        ).pack(side=tk.LEFT, padx=(8, 0))
        tk.Button(
            button_row,
            text="Cancel",
            command=modal.destroy,
            bg="#64748b",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            font=("Segoe UI", 11, "bold"),
        ).pack(side=tk.RIGHT)

        barcode_entry.focus_set()

    def _open_delete_modal(self) -> None:
        product = self._selected_product()
        if product is None:
            messagebox.showinfo("Delete product", "Select a product first.", parent=self)
            return

        modal = self._open_modal_shell("Delete Product", 500, 320)
        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Confirm Delete", font=("Segoe UI", 15, "bold")).pack(anchor="w")
        ttk.Label(content, text="Review the selected product before confirming deletion.", font=("Segoe UI", 12)).pack(anchor="w", pady=(4, 12))

        details = ttk.LabelFrame(content, text="Product Details")
        details.pack(fill=tk.BOTH, expand=True)

        info_lines = [
            f"Name: {product['name']}",
            f"Description: {product['description']}",
            f"Barcode: {product['barcode']}",
            f"Sell Price: {product['sell_price']:.2f}",
            f"Stock: {product['stock']}",
        ]

        for line in info_lines:
            ttk.Label(details, text=line, font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=2)

        button_row = ttk.Frame(content)
        button_row.pack(anchor="e", pady=(16, 0))

        def confirm_delete() -> None:
            if not messagebox.askyesno(
                "Confirm delete",
                f"Delete {product['name']} permanently?",
                parent=modal,
            ):
                return

            try:
                inventory.delete_product(product["id"])
            except ValueError as exc:
                messagebox.showerror("Cannot delete product", str(exc), parent=modal)
                return

            modal.destroy()
            self.selected_product_id = None
            self.refresh_products(self.search_var.get())
            self.status_var.set(f"Product deleted: {product['name']}")

        tk.Button(button_row, text="Cancel", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(button_row, text="Confirm", command=confirm_delete, bg="#dc2626", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)

    def _open_settings_modal(self) -> None:
        modal = self._open_modal_shell("Inventory Settings", 980, 650)
        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(2, weight=1)

        ttk.Label(content, text="Inventory Settings", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(
            content,
            text="Configure low stock monitoring and choose which products appear in POS quick access.",
            font=("Segoe UI", 12),
        ).grid(row=1, column=0, sticky="w", pady=(4, 12))

        threshold_frame = ttk.LabelFrame(content, text="Low Stock Threshold", padding=12)
        threshold_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        threshold_frame.columnconfigure(1, weight=1)

        threshold_var = tk.StringVar(value=str(inventory.get_low_stock_threshold()))
        ttk.Label(threshold_frame, text="Threshold:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        threshold_entry = ttk.Entry(threshold_frame, textvariable=threshold_var, width=12)
        threshold_entry.grid(row=0, column=1, sticky="w")
        ttk.Label(
            threshold_frame,
            text="Products with stock at or below this number will be flagged as low stock.",
            font=("Segoe UI", 10),
            foreground="#64748b",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        quick_area = ttk.Frame(content)
        quick_area.grid(row=3, column=0, sticky="nsew")
        quick_area.columnconfigure(0, weight=3)
        quick_area.columnconfigure(1, weight=2)
        quick_area.rowconfigure(1, weight=1)

        search_frame = ttk.Frame(quick_area)
        search_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        search_frame.columnconfigure(1, weight=1)
        ttk.Label(search_frame, text="Search items:", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w")
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, font=("Segoe UI", 12))
        search_entry.grid(row=0, column=1, sticky="ew", padx=(10, 8))

        quick_status_var = tk.StringVar(value="Select an item and press Quicklist to add it to the quick access list.")
        ttk.Label(search_frame, textvariable=quick_status_var, foreground="#64748b").grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(6, 0)
        )

        item_panel = ttk.Frame(quick_area)
        item_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        item_panel.columnconfigure(0, weight=1)
        item_panel.rowconfigure(0, weight=1)

        item_columns = ("name", "price", "stock")
        item_tree = ttk.Treeview(item_panel, columns=item_columns, show="headings", height=14)
        item_tree.heading("name", text="Name")
        item_tree.heading("price", text="Price")
        item_tree.heading("stock", text="Stock")
        item_tree.column("name", width=320, anchor=tk.W)
        item_tree.column("price", width=100, anchor=tk.E)
        item_tree.column("stock", width=80, anchor=tk.CENTER)
        item_tree.grid(row=0, column=0, sticky="nsew")

        item_scroll = ttk.Scrollbar(item_panel, orient=tk.VERTICAL, command=item_tree.yview)
        item_scroll.grid(row=0, column=1, sticky="ns")
        item_tree.configure(yscrollcommand=item_scroll.set)

        quick_panel = ttk.Frame(quick_area)
        quick_panel.grid(row=0, column=1, rowspan=2, sticky="nsew")
        quick_panel.columnconfigure(0, weight=1)
        quick_panel.rowconfigure(1, weight=1)

        ttk.Label(quick_panel, text="Quick Access List", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w")

        quick_list_frame = ttk.Frame(quick_panel)
        quick_list_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        quick_list_frame.columnconfigure(0, weight=1)
        quick_list_frame.rowconfigure(0, weight=1)

        quick_columns = ("name", "price", "stock")
        quick_tree = ttk.Treeview(quick_list_frame, columns=quick_columns, show="headings", height=14)
        quick_tree.heading("name", text="Name")
        quick_tree.heading("price", text="Price")
        quick_tree.heading("stock", text="Stock")
        quick_tree.column("name", width=220, anchor=tk.W)
        quick_tree.column("price", width=90, anchor=tk.E)
        quick_tree.column("stock", width=70, anchor=tk.CENTER)
        quick_tree.grid(row=0, column=0, sticky="nsew")

        quick_scroll = ttk.Scrollbar(quick_list_frame, orient=tk.VERTICAL, command=quick_tree.yview)
        quick_scroll.grid(row=0, column=1, sticky="ns")
        quick_tree.configure(yscrollcommand=quick_scroll.set)

        quick_button_row = ttk.Frame(quick_panel)
        quick_button_row.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        current_quick_ids = []
        for product_id in inventory.get_quick_access_product_ids():
            if inventory.get_product_by_id(product_id) is not None and product_id not in current_quick_ids:
                current_quick_ids.append(product_id)

        product_lookup: dict[int, dict] = {}

        def refresh_items(search_term: str = "") -> None:
            for row_id in item_tree.get_children():
                item_tree.delete(row_id)

            product_lookup.clear()
            products = inventory.search_products(search_term) if search_term else inventory.list_products()
            for product in products:
                product_lookup[product["id"]] = product
                item_tree.insert(
                    "",
                    tk.END,
                    iid=str(product["id"]),
                    values=(
                        product["name"],
                        f"{product['sell_price']:.2f}",
                        product["stock"],
                    ),
                )

        def refresh_quick_list() -> None:
            for row_id in quick_tree.get_children():
                quick_tree.delete(row_id)

            sanitized_ids: list[int] = []
            for product_id in current_quick_ids:
                product = inventory.get_product_by_id(product_id)
                if product is None or product_id in sanitized_ids:
                    continue
                sanitized_ids.append(product_id)
                quick_tree.insert(
                    "",
                    tk.END,
                    iid=str(product_id),
                    values=(
                        product["name"],
                        f"{product['sell_price']:.2f}",
                        product["stock"],
                    ),
                )

            current_quick_ids[:] = sanitized_ids

        def add_selected_to_quicklist() -> None:
            selected = item_tree.selection()
            if not selected:
                messagebox.showerror("Invalid input", "Select an item first", parent=modal)
                return

            product_id = int(selected[0])
            if product_id in current_quick_ids:
                quick_status_var.set("That item is already in the quick access list.")
                return

            product = product_lookup.get(product_id)
            if product is None:
                messagebox.showerror("Invalid input", "Selected item not found", parent=modal)
                return

            current_quick_ids.append(product_id)
            refresh_quick_list()
            quick_status_var.set(f"Added to quick access: {product['name']}")

        def remove_selected_from_quicklist() -> None:
            selected = quick_tree.selection()
            if not selected:
                messagebox.showerror("Invalid input", "Select a quick access item first", parent=modal)
                return

            product_id = int(selected[0])
            if product_id in current_quick_ids:
                current_quick_ids.remove(product_id)
                refresh_quick_list()
                quick_status_var.set("Removed from quick access list.")

        def submit() -> None:
            try:
                threshold_value = int(threshold_var.get() or 10)
                if threshold_value < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Validation error",
                    "Low stock threshold must be a whole number of 0 or more.",
                    parent=modal,
                )
                return

            inventory.set_low_stock_threshold(threshold_value)
            inventory.set_quick_access_product_ids(current_quick_ids)
            modal.destroy()
            self.refresh_products()
            self.status_var.set(
                f"Settings saved: Low stock threshold set to {threshold_value} and {len(current_quick_ids)} quick items saved"
            )

        search_var.trace_add("write", lambda *_args: refresh_items(search_var.get().strip()))
        search_entry.bind("<Return>", lambda _event: refresh_items(search_var.get().strip()))
        item_tree.bind("<Double-1>", lambda _event: add_selected_to_quicklist())
        quick_tree.bind("<Delete>", lambda _event: remove_selected_from_quicklist())

        quicklist_button = tk.Button(
            quick_button_row,
            text="Quicklist",
            command=add_selected_to_quicklist,
            bg="#4f46e5",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        )
        quicklist_button.pack(side=tk.LEFT)

        tk.Button(
            quick_button_row,
            text="Remove",
            command=remove_selected_from_quicklist,
            bg="#64748b",
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(8, 0))

        button_row = ttk.Frame(content)
        button_row.grid(row=4, column=0, sticky="e", pady=(18, 0))

        tk.Button(
            button_row,
            text="Cancel",
            command=modal.destroy,
            bg="#64748b",
            fg="white",
            relief=tk.FLAT,
            padx=18,
            pady=8,
            font=("Segoe UI", 12, "bold"),
        ).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(
            button_row,
            text="Save",
            command=submit,
            bg="#a855f7",
            fg="white",
            relief=tk.FLAT,
            padx=18,
            pady=8,
            font=("Segoe UI", 12, "bold"),
        ).pack(side=tk.RIGHT)

        refresh_items()
        refresh_quick_list()
        search_entry.focus_set()