import tkinter as tk
from tkinter import messagebox, ttk

from core import inventory


class UntrackedFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        self.selected_product_id: int | None = None
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Products without stock tracking are listed here.")

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X)

        ttk.Label(header, text="Untracked Items", font=("Segoe UI", 24, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="These products can be sold without stock counting. Enable tracking later if needed.",
            font=("Segoe UI", 13),
        ).pack(anchor="w", pady=(4, 0))

        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=(12, 10))

        search_row = ttk.Frame(toolbar)
        search_row.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(search_row, text="Search name / barcode:", font=("Segoe UI", 13, "bold")).pack(side=tk.LEFT)
        search_entry = ttk.Entry(search_row, textvariable=self.search_var, font=("Segoe UI", 13))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 8))
        search_entry.bind("<Return>", self._on_search)

        tk.Button(
            toolbar,
            text="Search",
            command=self._on_search,
            bg="#1d4ed8",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=16,
            pady=8,
            font=("Segoe UI", 13, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh,
            bg="#64748b",
            fg="white",
            activebackground="#64748b",
            activeforeground="white",
            relief=tk.FLAT,
            padx=16,
            pady=8,
            font=("Segoe UI", 13, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(
            toolbar,
            text="Enable Tracking",
            command=self._open_enable_tracking_modal,
            bg="#4f46e5",
            fg="white",
            activebackground="#4f46e5",
            activeforeground="white",
            relief=tk.FLAT,
            padx=16,
            pady=8,
            font=("Segoe UI", 13, "bold"),
            cursor="hand2",
        ).pack(side=tk.RIGHT)

        table_box = ttk.Frame(self)
        table_box.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "barcode", "sell_price", "stock")
        self.product_table = ttk.Treeview(table_box, columns=columns, show="headings", height=20)
        self.product_table.heading("id", text="ID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("barcode", text="Barcode")
        self.product_table.heading("sell_price", text="Sell Price")
        self.product_table.heading("stock", text="Stock")

        self.product_table.column("id", width=60, anchor=tk.CENTER)
        self.product_table.column("name", width=300)
        self.product_table.column("barcode", width=180)
        self.product_table.column("sell_price", width=120, anchor=tk.E)
        self.product_table.column("stock", width=90, anchor=tk.CENTER)
        self.product_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(table_box, orient=tk.VERTICAL, command=self.product_table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_table.configure(yscrollcommand=scrollbar.set)

        self.product_table.bind("<<TreeviewSelect>>", self._on_row_select)
        self.product_table.bind("<Double-1>", self._open_enable_tracking_modal)

        footer = ttk.Frame(self)
        footer.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(footer, textvariable=self.status_var).pack(side=tk.LEFT)

    def _on_search(self, _event: tk.Event | None = None) -> None:
        self.refresh(self.search_var.get())

    def _on_row_select(self, _event: tk.Event) -> None:
        selected = self.product_table.selection()
        self.selected_product_id = int(selected[0]) if selected else None

    def _selected_product(self) -> dict | None:
        if self.selected_product_id is None:
            return None
        return inventory.get_product_by_id(self.selected_product_id)

    def _center_modal(self, modal: tk.Toplevel, width: int, height: int) -> None:
        modal.update_idletasks()
        screen_w = modal.winfo_screenwidth()
        screen_h = modal.winfo_screenheight()
        modal.geometry(f"{width}x{height}+{max((screen_w - width) // 2, 0)}+{max((screen_h - height) // 2, 0)}")

    def _open_enable_tracking_modal(self, _event: tk.Event | None = None) -> None:
        product = self._selected_product()
        if product is None:
            messagebox.showinfo("Enable tracking", "Select a product first.", parent=self)
            return

        modal = tk.Toplevel(self)
        modal.title("Enable Stock Tracking")
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()
        self._center_modal(modal, 480, 320)

        content = ttk.Frame(modal, padding=16)
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(1, weight=1)

        ttk.Label(content, text="Enable Stock Tracking", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(
            content,
            text=f"Product: {product['name']} (ID {product['id']})",
            font=("Segoe UI", 12),
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 12))

        stock_var = tk.StringVar(value="0")
        ttk.Label(content, text="Starting stock:").grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        ttk.Entry(content, textvariable=stock_var).grid(row=2, column=1, sticky="ew", pady=6)

        button_row = ttk.Frame(content)
        button_row.grid(row=3, column=0, columnspan=2, sticky="e", pady=(18, 0))

        def submit() -> None:
            try:
                stock_value = int(stock_var.get() or 0)
                if stock_value < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Validation error", "Starting stock must be a whole number of 0 or more.", parent=modal)
                return

            try:
                inventory.set_stock_tracking(product["id"], True, stock_value)
            except ValueError as exc:
                messagebox.showerror("Update error", str(exc), parent=modal)
                return

            modal.destroy()
            self.selected_product_id = None
            self.refresh(self.search_var.get())
            self.status_var.set(f"Tracking enabled for {product['name']}")

        tk.Button(button_row, text="Cancel", command=modal.destroy, bg="#64748b", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(button_row, text="Enable", command=submit, bg="#4f46e5", fg="white", relief=tk.FLAT, padx=18, pady=8, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT)

    def refresh(self, search_term: str | None = None) -> None:
        term = self.search_var.get() if search_term is None else search_term
        products = inventory.get_untracked_products(term)

        for row_id in self.product_table.get_children():
            self.product_table.delete(row_id)

        for product in products:
            self.product_table.insert(
                "",
                tk.END,
                iid=str(product["id"]),
                values=(
                    product["id"],
                    product["name"],
                    product["barcode"],
                    f"{product['sell_price']:.2f}",
                    product["stock"],
                ),
            )

        self.status_var.set(f"Loaded {len(products)} untracked products.")
