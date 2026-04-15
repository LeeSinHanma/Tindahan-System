import tkinter as tk
from tkinter import messagebox, ttk

from core import inventory


class InventoryFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
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

        ttk.Label(header, text="Inventory CRUD", font=("Segoe UI", 24, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="Create products from a modal form, update stock with buttons, or delete with confirmation.",
            font=("Segoe UI", 13),
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

        self.product_table.column("id", width=60, anchor=tk.CENTER)
        self.product_table.column("name", width=280)
        self.product_table.column("barcode", width=180)
        self.product_table.column("original_price", width=120, anchor=tk.E)
        self.product_table.column("sell_price", width=120, anchor=tk.E)
        self.product_table.column("stock", width=90, anchor=tk.CENTER)
        self.product_table.column("tracked", width=90, anchor=tk.CENTER)
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
            padx=16,
            pady=8,
            font=("Segoe UI", 13, "bold"),
            cursor="hand2",
        )

    def _open_modal_shell(self, title: str, width: int = 520, height: int = 420) -> tk.Toplevel:
        modal = tk.Toplevel(self)
        modal.title(title)
        modal.geometry(f"{width}x{height}")
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        self._center_modal(modal, width, height)
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
        modal = self._open_modal_shell("Create Product", 540, 500)

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
        }

        content.columnconfigure(1, weight=1)
        self._field_row(content, "Name", self._create_vars["name"], 2)
        self._field_row(content, "Description", self._create_vars["description"], 3)
        self._field_row(content, "Barcode", self._create_vars["barcode"], 4)
        self._field_row(content, "Original Price", self._create_vars["original_price"], 5)
        self._field_row(content, "Sell Price", self._create_vars["sell_price"], 6)
        self._field_row(content, "Stock", self._create_vars["stock"], 7)

        tracking_row = ttk.Frame(content)
        tracking_row.grid(row=8, column=0, columnspan=2, sticky="w", pady=(4, 8))
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

        button_row = ttk.Frame(content)
        button_row.grid(row=9, column=0, columnspan=2, sticky="e", pady=(18, 0))

        def submit() -> None:
            try:
                product_id = inventory.create_product(self._product_payload())
            except ValueError as exc:
                messagebox.showerror("Validation error", str(exc), parent=modal)
                return

            modal.destroy()
            self.refresh_products()
            self.status_var.set(f"Product created: {product_id}")

        tk.Button(button_row, text="Cancel", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(button_row, text="Add", command=submit, bg="#16a34a", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)

    def _open_update_modal(self, _event: tk.Event | None = None) -> None:
        product = self._selected_product()
        if product is None:
            messagebox.showinfo("Update product", "Select a product first.", parent=self)
            return

        modal = self._open_modal_shell("Update Product", 560, 580)
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
        }

        self._update_vars = vars_map

        content.columnconfigure(1, weight=1)
        self._field_row(content, "Name", vars_map["name"], 2)
        self._field_row(content, "Description", vars_map["description"], 3)
        self._field_row(content, "Barcode", vars_map["barcode"], 4)
        self._field_row(content, "Original Price", vars_map["original_price"], 5)
        self._field_row(content, "Sell Price", vars_map["sell_price"], 6)
        self._field_row(content, "Stock", vars_map["stock"], 7)

        tracking_row = ttk.Frame(content)
        tracking_row.grid(row=8, column=0, columnspan=2, sticky="w", pady=(4, 8))
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

        stock_buttons = ttk.Frame(content)
        stock_buttons.grid(row=9, column=0, columnspan=2, sticky="w", pady=(6, 10))

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
        button_row.grid(row=10, column=0, columnspan=2, sticky="e", pady=(18, 0))

        def submit() -> None:
            if not messagebox.askyesno(
                "Confirm update",
                f"Save changes to {product['name']}?",
                parent=modal,
            ):
                return

            try:
                inventory.update_product(product["id"], {key: value.get() for key, value in vars_map.items()})
            except ValueError as exc:
                messagebox.showerror("Validation error", str(exc), parent=modal)
                return

            modal.destroy()
            self.refresh_products(self.search_var.get())
            self.status_var.set(f"Product updated: {product['name']}")

        tk.Button(button_row, text="Cancel", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(button_row, text="Update", command=submit, bg="#f59e0b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)

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

            inventory.delete_product(product["id"])
            modal.destroy()
            self.selected_product_id = None
            self.refresh_products(self.search_var.get())
            self.status_var.set(f"Product deleted: {product['name']}")

        tk.Button(button_row, text="Cancel", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(button_row, text="Confirm", command=confirm_delete, bg="#dc2626", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)

    def _open_settings_modal(self) -> None:
        modal = self._open_modal_shell("Inventory Settings", 480, 280)
        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Inventory Settings", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(content, text="Configure how inventory is monitored and managed.", font=("Segoe UI", 12)).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 12))

        current_threshold = inventory.get_low_stock_threshold()
        threshold_var = tk.StringVar(value=str(current_threshold))

        content.columnconfigure(1, weight=1)
        ttk.Label(content, text="Low Stock Threshold:").grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        threshold_entry = ttk.Entry(content, textvariable=threshold_var)
        threshold_entry.grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(
            content,
            text="Products with stock at or below this number will be flagged as low stock.",
            font=("Segoe UI", 10),
            foreground="#64748b",
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(2, 12))

        button_row = ttk.Frame(content)
        button_row.grid(row=4, column=0, columnspan=2, sticky="e", pady=(18, 0))

        def submit() -> None:
            try:
                threshold_value = int(threshold_var.get() or 10)
                if threshold_value < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Validation error", "Low stock threshold must be a whole number of 0 or more.", parent=modal)
                return

            inventory.set_low_stock_threshold(threshold_value)
            modal.destroy()
            self.refresh_products()
            self.status_var.set(f"Settings saved: Low stock threshold set to {threshold_value}")

        tk.Button(button_row, text="Cancel", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(button_row, text="Save", command=submit, bg="#a855f7", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)