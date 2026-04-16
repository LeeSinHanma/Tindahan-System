import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core import inventory, shopping_list


class ShoppingListFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        top_level = master.winfo_toplevel()
        screen_w = top_level.winfo_screenwidth()
        screen_h = top_level.winfo_screenheight()
        self.compact_layout = screen_w < 1400 or screen_h < 820
        self.selected_product_id: int | None = None
        self.selected_list_item_id: int | None = None
        self.checked_product_ids: set[int] = set()
        self.checked_list_item_ids: set[int] = set()

        self.product_search_var = tk.StringVar()
        self.qty_var = tk.StringVar(value="1")
        self.include_done_var = tk.BooleanVar(value=True)
        self.total_var = tk.StringVar(value="Total: PHP 0.00")
        self.status_var = tk.StringVar(value="Create a shopping list from existing products.")

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X)

        ttk.Label(header, text="Shopping List", font=("Segoe UI", 20 if self.compact_layout else 24, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="Select products, set quantities, and track what to buy.",
            font=("Segoe UI", 11 if self.compact_layout else 13),
        ).pack(anchor="w", pady=(3 if self.compact_layout else 4, 0))

        content = ttk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True, pady=(8 if self.compact_layout else 12, 0))
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        self._build_product_panel(content)
        self._build_list_panel(content)

        footer = ttk.Frame(self)
        footer.pack(fill=tk.X, pady=(4 if self.compact_layout else 8, 0))
        ttk.Label(footer, textvariable=self.status_var).pack(side=tk.LEFT)

    def _build_product_panel(self, parent: ttk.Frame) -> None:
        panel = ttk.LabelFrame(parent, text="Products", padding=8 if self.compact_layout else 10)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 6 if self.compact_layout else 8))
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(2, weight=1)

        search_row = ttk.Frame(panel)
        search_row.grid(row=0, column=0, sticky="ew", pady=(0, 6 if self.compact_layout else 8))
        search_row.columnconfigure(0, weight=1)

        entry = ttk.Entry(search_row, textvariable=self.product_search_var)
        entry.grid(row=0, column=0, sticky="ew")
        entry.bind("<Return>", self._search_products)

        tk.Button(
            search_row,
            text="Search",
            command=self._search_products,
            bg="#1d4ed8",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).grid(row=0, column=1, padx=(6, 0))

        columns = ("pick", "id", "name", "price")
        self.product_table = ttk.Treeview(panel, columns=columns, show="headings", height=11 if self.compact_layout else 14)
        self.product_table.heading("pick", text="Pick")
        self.product_table.heading("id", text="ID")
        self.product_table.heading("name", text="Product")
        self.product_table.heading("price", text="Orig. Price")

        self.product_table.column("pick", width=48, anchor=tk.CENTER)
        self.product_table.column("id", width=48, anchor=tk.CENTER)
        self.product_table.column("name", width=190 if self.compact_layout else 220)
        self.product_table.column("price", width=88, anchor=tk.E)
        self.product_table.grid(row=2, column=0, sticky="nsew")

        product_scroll = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=self.product_table.yview)
        product_scroll.grid(row=2, column=1, sticky="ns")
        self.product_table.configure(yscrollcommand=product_scroll.set)
        self.product_table.bind("<<TreeviewSelect>>", self._on_product_select)
        self.product_table.bind("<Button-1>", self._toggle_product_check)

        add_row = ttk.Frame(panel)
        add_row.grid(row=3, column=0, sticky="ew", pady=(6 if self.compact_layout else 8, 0))

        ttk.Label(add_row, text="Qty:").pack(side=tk.LEFT)
        qty_entry = ttk.Entry(add_row, textvariable=self.qty_var, width=5, justify=tk.CENTER)
        qty_entry.pack(side=tk.LEFT, padx=(6, 8))
        qty_entry.bind("<Return>", self._add_to_list)

        tk.Button(
            add_row,
            text="Add To List",
            command=self._add_to_list,
            bg="#16a34a",
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT)

        tk.Button(
            add_row,
            text="Add Checked",
            command=self._add_checked_to_list,
            bg="#0f766e",
            fg="white",
            activebackground="#0f766e",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(6, 0))

        tk.Button(
            add_row,
            text="Add Low Stock",
            command=self._add_low_stock_items,
            bg="#7c3aed",
            fg="white",
            activebackground="#7c3aed",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(6, 0))

    def _build_list_panel(self, parent: ttk.Frame) -> None:
        panel = ttk.LabelFrame(parent, text="Current Shopping List", padding=8 if self.compact_layout else 10)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        top_row = ttk.Frame(panel)
        top_row.grid(row=0, column=0, sticky="ew", pady=(0, 6 if self.compact_layout else 8))

        ttk.Checkbutton(
            top_row,
            text="Show completed",
            variable=self.include_done_var,
            command=self.refresh,
        ).pack(side=tk.LEFT)

        ttk.Label(top_row, textvariable=self.total_var, font=("Segoe UI", 10 if self.compact_layout else 11, "bold")).pack(side=tk.RIGHT, padx=(8, 0))

        tk.Button(
            top_row,
            text="Refresh",
            command=self.refresh,
            bg="#64748b",
            fg="white",
            activebackground="#64748b",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.RIGHT)

        tk.Button(
            top_row,
            text="Save PDF",
            command=self._save_pdf,
            bg="#0f766e",
            fg="white",
            activebackground="#0f766e",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.RIGHT, padx=(6, 0))

        tk.Button(
            top_row,
            text="Remove All",
            command=self._remove_all,
            bg="#dc2626",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.RIGHT, padx=(6, 0))

        columns = ("pick", "id", "name", "description", "original_price", "qty", "status")
        self.list_table = ttk.Treeview(panel, columns=columns, show="headings", height=12 if self.compact_layout else 16)
        self.list_table.heading("pick", text="Pick")
        self.list_table.heading("id", text="Item")
        self.list_table.heading("name", text="Product")
        self.list_table.heading("description", text="Description")
        self.list_table.heading("original_price", text="Orig. Price")
        self.list_table.heading("qty", text="Qty")
        self.list_table.heading("status", text="Status")

        self.list_table.column("pick", width=48, anchor=tk.CENTER)
        self.list_table.column("id", width=55, anchor=tk.CENTER)
        self.list_table.column("name", width=160 if self.compact_layout else 170)
        self.list_table.column("description", width=190 if self.compact_layout else 220)
        self.list_table.column("original_price", width=90, anchor=tk.E)
        self.list_table.column("qty", width=55, anchor=tk.CENTER)
        self.list_table.column("status", width=80, anchor=tk.CENTER)
        self.list_table.grid(row=1, column=0, sticky="nsew")

        list_scroll = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=self.list_table.yview)
        list_scroll.grid(row=1, column=1, sticky="ns")
        self.list_table.configure(yscrollcommand=list_scroll.set)
        self.list_table.bind("<<TreeviewSelect>>", self._on_list_item_select)
        self.list_table.bind("<Button-1>", self._toggle_list_item_check)

        action_row = ttk.Frame(panel)
        action_row.grid(row=2, column=0, sticky="ew", pady=(6 if self.compact_layout else 8, 0))

        tk.Button(
            action_row,
            text="Select All",
            command=self._select_all_list_items,
            bg="#2563eb",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT)

        tk.Button(
            action_row,
            text="Clear Selection",
            command=self._clear_list_selection,
            bg="#64748b",
            fg="white",
            activebackground="#64748b",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(6, 0))

        tk.Button(
            action_row,
            text="Mark Done",
            command=lambda: self._mark_selected_done(True),
            bg="#0ea5e9",
            fg="white",
            activebackground="#0ea5e9",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(6, 0))

        tk.Button(
            action_row,
            text="Mark Pending",
            command=lambda: self._mark_selected_done(False),
            bg="#475569",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(6, 0))

        tk.Button(
            action_row,
            text="Remove",
            command=self._remove_selected,
            bg="#dc2626",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(6, 0))

        tk.Button(
            action_row,
            text="Set Qty",
            command=self._set_selected_qty,
            bg="#1d4ed8",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(6, 0))

        tk.Button(
            action_row,
            text="Clear Done",
            command=self._clear_done_items,
            bg="#b45309",
            fg="white",
            activebackground="#b45309",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side=tk.RIGHT)

    def _search_products(self, _event: tk.Event | None = None) -> None:
        self._load_products(self.product_search_var.get())

    def _load_products(self, search_term: str = "") -> None:
        products = inventory.search_products(search_term) if search_term.strip() else inventory.list_products()
        visible_product_ids = {int(product["id"]) for product in products}
        self.checked_product_ids.intersection_update(visible_product_ids)

        for row_id in self.product_table.get_children():
            self.product_table.delete(row_id)

        for product in products:
            product_id = int(product["id"])
            checked_marker = "[x]" if product_id in self.checked_product_ids else "[ ]"
            self.product_table.insert(
                "",
                tk.END,
                iid=f"p{product_id}",
                values=(
                    checked_marker,
                    product_id,
                    product["name"],
                    f"{product['original_price']:.2f}",
                ),
            )

    def _load_list_items(self) -> None:
        items = shopping_list.list_items(self.include_done_var.get())
        visible_item_ids = {int(item["id"]) for item in items}
        self.checked_list_item_ids.intersection_update(visible_item_ids)

        for row_id in self.list_table.get_children():
            self.list_table.delete(row_id)

        for item in items:
            status = "Done" if item["is_done"] else "Pending"
            item_id = int(item["id"])
            checked_marker = "[x]" if item_id in self.checked_list_item_ids else "[ ]"
            self.list_table.insert(
                "",
                tk.END,
                iid=f"s{item_id}",
                values=(
                    checked_marker,
                    item_id,
                    item["product"]["name"],
                    item["product"]["description"],
                    f"{item['product']['original_price']:.2f}",
                    item["quantity"],
                    status,
                ),
                tags=("done",) if item["is_done"] else (),
            )

        self.list_table.tag_configure("done", background="#dcfce7")
        self.total_var.set(f"Total: PHP {shopping_list.get_total():.2f}")
        self.status_var.set(f"Shopping list items loaded: {len(items)}")

    def _add_low_stock_items(self) -> None:
        added_count = shopping_list.add_low_stock_items()
        self.checked_product_ids.clear()
        self.checked_list_item_ids.clear()
        self._load_products(self.product_search_var.get())
        self._load_list_items()
        self.status_var.set(f"Added {added_count} low-stock item(s) to shopping list")

    def _on_product_select(self, _event: tk.Event) -> None:
        selected = self.product_table.selection()
        if not selected:
            self.selected_product_id = None
            return
        self.selected_product_id = int(self.product_table.item(selected[0], "values")[1])

    def _on_list_item_select(self, _event: tk.Event) -> None:
        selected = self.list_table.selection()
        if not selected:
            self.selected_list_item_id = None
            return
        self.selected_list_item_id = int(self.list_table.item(selected[0], "values")[1])

    def _toggle_product_check(self, event: tk.Event) -> str | None:
        row_id = self.product_table.identify_row(event.y)
        col_id = self.product_table.identify_column(event.x)
        if not row_id or col_id != "#1":
            return None

        values = self.product_table.item(row_id, "values")
        if len(values) < 2:
            return "break"

        product_id = int(values[1])
        if product_id in self.checked_product_ids:
            self.checked_product_ids.remove(product_id)
        else:
            self.checked_product_ids.add(product_id)

        self._load_products(self.product_search_var.get())
        return "break"

    def _toggle_list_item_check(self, event: tk.Event) -> str | None:
        row_id = self.list_table.identify_row(event.y)
        col_id = self.list_table.identify_column(event.x)
        if not row_id or col_id != "#1":
            return None

        values = self.list_table.item(row_id, "values")
        if len(values) < 2:
            return "break"

        item_id = int(values[1])
        if item_id in self.checked_list_item_ids:
            self.checked_list_item_ids.remove(item_id)
        else:
            self.checked_list_item_ids.add(item_id)

        self._load_list_items()
        return "break"

    def _select_all_list_items(self) -> None:
        self.checked_list_item_ids = {
            int(self.list_table.item(row_id, "values")[1])
            for row_id in self.list_table.get_children()
        }
        self._load_list_items()
        self.status_var.set(f"Selected {len(self.checked_list_item_ids)} shopping-list item(s)")

    def _clear_list_selection(self) -> None:
        self.checked_list_item_ids.clear()
        self._load_list_items()
        self.status_var.set("Shopping-list selection cleared")

    def _target_product_ids(self) -> list[int]:
        if self.checked_product_ids:
            return sorted(self.checked_product_ids)
        if self.selected_product_id is not None:
            return [self.selected_product_id]
        return []

    def _target_list_item_ids(self) -> list[int]:
        if self.checked_list_item_ids:
            return sorted(self.checked_list_item_ids)
        if self.selected_list_item_id is not None:
            return [self.selected_list_item_id]
        return []

    def _add_to_list(self, _event: tk.Event | None = None) -> None:
        if self.selected_product_id is None:
            self.status_var.set("Select a product first")
            return

        try:
            shopping_list.add_item(self.selected_product_id, self.qty_var.get())
        except ValueError as exc:
            messagebox.showerror("Validation error", str(exc), parent=self)
            return

        self.qty_var.set("1")
        self._load_list_items()
        self.status_var.set("Product added to shopping list")

    def _add_checked_to_list(self) -> None:
        product_ids = self._target_product_ids()
        if not product_ids:
            self.status_var.set("Select or check product(s) first")
            return

        added_count = 0
        for product_id in product_ids:
            try:
                shopping_list.add_item(product_id, self.qty_var.get())
                added_count += 1
            except ValueError as exc:
                messagebox.showerror("Validation error", str(exc), parent=self)
                return

        self.checked_product_ids.clear()
        self.qty_var.set("1")
        self._load_products(self.product_search_var.get())
        self._load_list_items()
        self.status_var.set(f"Added {added_count} product(s) to shopping list")

    def _set_selected_qty(self) -> None:
        item_ids = self._target_list_item_ids()
        if not item_ids:
            self.status_var.set("Select or check shopping-list item(s) first")
            return

        for item_id in item_ids:
            try:
                shopping_list.update_item_quantity(item_id, self.qty_var.get())
            except ValueError as exc:
                messagebox.showerror("Validation error", str(exc), parent=self)
                return

        self.qty_var.set("1")
        self.checked_list_item_ids.clear()
        self._load_list_items()
        self.status_var.set(f"Quantity updated for {len(item_ids)} item(s)")

    def _mark_selected_done(self, is_done: bool) -> None:
        item_ids = self._target_list_item_ids()
        if not item_ids:
            self.status_var.set("Select or check shopping-list item(s) first")
            return

        for item_id in item_ids:
            shopping_list.mark_done(item_id, is_done)

        self.checked_list_item_ids.clear()
        self._load_list_items()
        self.status_var.set(f"Status updated for {len(item_ids)} item(s)")

    def _remove_selected(self) -> None:
        item_ids = self._target_list_item_ids()
        if not item_ids:
            self.status_var.set("Select or check shopping-list item(s) first")
            return

        for item_id in item_ids:
            shopping_list.remove_item(item_id)

        self.checked_list_item_ids.clear()
        self.selected_list_item_id = None
        self._load_list_items()
        self.status_var.set(f"Removed {len(item_ids)} item(s) from shopping list")

    def _clear_done_items(self) -> None:
        shopping_list.clear_done_items()
        self.selected_list_item_id = None
        self._load_list_items()
        self.status_var.set("Completed shopping-list items cleared")

    def _select_all_list_items(self) -> None:
        item_ids: set[int] = set()
        for row_id in self.list_table.get_children():
            values = self.list_table.item(row_id, "values")
            if len(values) >= 2:
                item_ids.add(int(values[1]))

        self.checked_list_item_ids = item_ids
        self._load_list_items()
        self.status_var.set(f"Selected {len(item_ids)} shopping-list item(s)")

    def _clear_list_selection(self) -> None:
        self.checked_list_item_ids.clear()
        self.selected_list_item_id = None
        self._load_list_items()
        self.status_var.set("Shopping-list selection cleared")

    def _remove_all(self) -> None:
        if not messagebox.askyesno(
            "Remove all items",
            "Clear the entire shopping list?",
            parent=self,
        ):
            return

        shopping_list.clear_all_items()
        self.selected_product_id = None
        self.selected_list_item_id = None
        self.checked_product_ids.clear()
        self.checked_list_item_ids.clear()
        self._load_products(self.product_search_var.get())
        self._load_list_items()
        self.status_var.set("Shopping list cleared")

    def _save_pdf(self) -> None:
        default_name = "shopping_list.pdf"
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save Shopping List as PDF",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf")],
        )
        if not file_path:
            return

        try:
            shopping_list.save_pdf(file_path, self.include_done_var.get())
        except Exception as exc:
            messagebox.showerror("Save error", str(exc), parent=self)
            return

        self.status_var.set(f"Shopping list saved to PDF: {file_path}")

    def refresh(self) -> None:
        self._load_products(self.product_search_var.get())
        self._load_list_items()
