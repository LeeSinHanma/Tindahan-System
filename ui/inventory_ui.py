import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core import inventory
from ui import theme as visual
from ui.widgets import (
    ActionButton,
    FlowFrame,
    ScrollFrame,
    center_dialog,
    page_header,
    table,
)


class InventoryFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        top_level = master.winfo_toplevel()
        self.theme = visual.get_theme()
        self.selected_product_id: int | None = None
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(
            value="Select a product, then use Create / Update / Delete"
        )
        self.show_only_untracked_var = tk.BooleanVar(value=False)
        self.search_entry: ttk.Entry | None = None

        self._build_ui()
        self.refresh_products()
        top_level.bind("<F1>", self._on_create_hotkey, add="+")
        top_level.bind("<F2>", self._on_update_hotkey, add="+")
        top_level.bind("<F3>", self._on_delete_hotkey, add="+")
        top_level.bind("<F4>", self._on_restock_hotkey, add="+")
        top_level.bind("<F5>", self._on_settings_hotkey, add="+")

    def _build_ui(self) -> None:
        self.configure(padding=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        page_header(
            self, "Inventory", "Manage products, prices, and stock levels."
        ).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        actions = FlowFrame(self)
        actions.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        actions.add(
            ActionButton(
                actions,
                text="Add product · F1",
                variant="Primary",
                command=self._open_create_modal,
            )
        )
        self.edit_button = actions.add(
            ActionButton(
                actions,
                text="Edit · F2",
                command=self._open_update_modal,
                state="disabled",
            )
        )
        actions.add(
            ActionButton(actions, text="Restock · F4", command=self._open_restock_modal)
        )
        more = ttk.Menubutton(actions, text="More actions", direction="below")
        menu = tk.Menu(more, tearoff=False)
        menu.add_command(label="Export inventory PDF", command=self._export_pdf)
        menu.add_command(
            label="Inventory settings · F5", command=self._open_settings_modal
        )
        menu.add_separator()
        menu.add_command(
            label="Delete selected product · F3", command=self._open_delete_modal
        )
        more.configure(menu=menu)
        actions.add(more)
        search = ttk.Frame(self)
        search.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        search.columnconfigure(0, weight=1)
        self.search_entry = ttk.Entry(search, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=0, sticky="ew")
        ttk.Label(search, text="Search name or barcode", style="Muted.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        self.search_entry.bind("<Return>", self._on_search)
        ActionButton(search, text="Search", command=self._on_search).grid(
            row=1, column=1, padx=8
        )
        self.filter_var = tk.StringVar(value="All products")
        filters = ttk.Combobox(
            search,
            textvariable=self.filter_var,
            values=("All products", "Low stock", "Out of stock", "Untracked"),
            state="readonly",
            width=16,
        )
        filters.grid(row=1, column=2)
        filters.bind("<<ComboboxSelected>>", lambda e: self._apply_filter())
        box, self.product_table = table(
            self,
            (
                "id",
                "name",
                "barcode",
                "original_price",
                "sell_price",
                "stock",
                "tracked",
            ),
            ("ID", "Product", "Barcode", "Cost", "Sell price", "Stock", "Status"),
            (44, 220, 150, 85, 85, 60, 110),
            displaycolumns=(
                "name",
                "barcode",
                "original_price",
                "sell_price",
                "stock",
                "tracked",
            ),
            empty_text="No products yet. Add your first product above.",
            height=6,
        )
        box.grid(row=3, column=0, sticky="nsew")
        self.product_table.tag_configure("low_stock", background="#fffbeb")
        self.product_table.tag_configure("out_of_stock", background="#fff1f2")
        self.product_table.tag_configure("untracked", foreground=visual.MUTED)
        self.product_table.bind("<<TreeviewSelect>>", self._on_row_select)
        self.product_table.bind("<Double-1>", self._open_update_modal)
        ttk.Label(self, textvariable=self.status_var, style="Muted.TLabel").grid(
            row=4, column=0, sticky="w", pady=(8, 0)
        )

    def _apply_filter(self):
        self.show_only_untracked_var.set(self.filter_var.get() == "Untracked")
        self.refresh_products()

    def _on_create_hotkey(self, _event: tk.Event | None = None) -> str:
        if getattr(self.winfo_toplevel(), "active_screen", None) != "inventory":
            return ""
        self._open_create_modal()
        return "break"

    def _on_update_hotkey(self, _event: tk.Event | None = None) -> str:
        if getattr(self.winfo_toplevel(), "active_screen", None) != "inventory":
            return ""
        self._open_update_modal()
        return "break"

    def _on_delete_hotkey(self, _event: tk.Event | None = None) -> str:
        if getattr(self.winfo_toplevel(), "active_screen", None) != "inventory":
            return ""
        self._open_delete_modal()
        return "break"

    def _on_restock_hotkey(self, _event: tk.Event | None = None) -> str:
        if getattr(self.winfo_toplevel(), "active_screen", None) != "inventory":
            return ""
        self._open_restock_modal()
        return "break"

    def _on_settings_hotkey(self, _event: tk.Event | None = None) -> str:
        if getattr(self.winfo_toplevel(), "active_screen", None) != "inventory":
            return ""
        self._open_settings_modal()
        return "break"

    def _open_modal_shell(
        self, title: str, width: int = 520, height: int = 420
    ) -> tk.Toplevel:
        modal = tk.Toplevel(self)
        modal.title(title)
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
        return modal

    def _center_modal(self, modal, width, height):
        center_dialog(modal, width, height)

    def _field_row(
        self, parent: tk.Widget, label_text: str, variable: tk.StringVar, row: int
    ) -> ttk.Entry:
        ttk.Label(parent, text=label_text).grid(
            row=row, column=0, sticky="w", pady=6, padx=(0, 10)
        )
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky="ew", pady=6)
        return entry

    def _resolve_parent_link(
        self,
        current_product_id: int | None,
        current_barcode: str,
        vars_map: dict[str, tk.Variable],
    ) -> dict:
        if not bool(vars_map["parent_linked"].get()):
            return {"parent_product_id": None, "parent_units": 1}

        parent_barcode = str(vars_map["parent_barcode"].get()).strip()
        if not parent_barcode:
            raise ValueError("Enter the parent item barcode")

        parent_product = inventory.get_product_by_barcode(parent_barcode)
        if parent_product is None:
            raise ValueError("Parent product not found")

        if (
            current_product_id is not None
            and parent_product["id"] == current_product_id
        ):
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
        self.filter_var.set("All products")
        self.search_var.set("")
        self._apply_filter()

    def _show_untracked(self) -> None:
        self.filter_var.set("Untracked")
        self._apply_filter()

    def _export_pdf(self) -> None:
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save Inventory as PDF",
            defaultextension=".pdf",
            initialfile="inventory_report.pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not file_path:
            return

        try:
            inventory.save_pdf(file_path)
        except Exception as exc:
            messagebox.showerror(
                "Export failed", f"Could not save PDF:\n{exc}", parent=self
            )
            return

        self.status_var.set(f"Inventory PDF saved to: {file_path}")
        messagebox.showinfo(
            "Export complete", f"Inventory report saved to:\n{file_path}", parent=self
        )

    def _on_search(self, _event: tk.Event | None = None) -> None:
        self.refresh_products(self.search_var.get())

    def focus_search(self) -> None:
        if self.search_entry:
            self.search_entry.focus()

    def _on_row_select(self, _event=None) -> None:
        selected = self.product_table.selection()
        self.selected_product_id = int(selected[0]) if selected else None
        self.edit_button.configure(state="normal" if selected else "disabled")

    def refresh_products(self, search_term=None) -> None:
        term = self.search_var.get() if search_term is None else search_term
        products = (
            inventory.search_products(term)
            if term.strip()
            else inventory.list_products()
        )
        threshold = inventory.get_low_stock_threshold()
        filter_name = self.filter_var.get()
        if filter_name == "Untracked":
            products = [p for p in products if not p.get("stock_tracked")]
        elif filter_name == "Low stock":
            products = [
                p
                for p in products
                if p.get("stock_tracked") and 0 < p["stock"] <= threshold
            ]
        elif filter_name == "Out of stock":
            products = [
                p for p in products if p.get("stock_tracked") and p["stock"] <= 0
            ]
        selected = str(self.selected_product_id) if self.selected_product_id else None
        self.product_table.delete(*self.product_table.get_children())
        self.product_table.empty_text = (
            "No matching products. Try a different search or filter."
            if term or filter_name != "All products"
            else "No products yet. Add your first product above."
        )
        self.product_table._refresh_empty()
        for product in products:
            tracked = product.get("stock_tracked", False)
            status = (
                "Untracked"
                if not tracked
                else "Out of stock"
                if product["stock"] <= 0
                else "Low stock"
                if product["stock"] <= threshold
                else "In stock"
            )
            tag = (
                "untracked"
                if not tracked
                else "out_of_stock"
                if product["stock"] <= 0
                else "low_stock"
                if product["stock"] <= threshold
                else ""
            )
            self.product_table.insert(
                "",
                "end",
                iid=str(product["id"]),
                values=(
                    product["id"],
                    product["name"],
                    product["barcode"],
                    f"{product['original_price']:,.2f}",
                    f"{product['sell_price']:,.2f}",
                    product["stock"] if tracked else "—",
                    status,
                ),
                tags=(tag,),
            )
        if selected and self.product_table.exists(selected):
            self.product_table.selection_set(selected)
        self._on_row_select()
        self.status_var.set(
            f"{len(products)} products  ·  {len(inventory.get_low_stock_products())} need restocking"
        )

    def _open_create_modal(self) -> None:
        self._open_product_editor()

    def _open_update_modal(self, _event=None) -> None:
        product = self._selected_product()
        if product is not None:
            self._open_product_editor(product)

    def _open_product_editor(self, product=None):
        editing = product is not None
        product = product or {}
        modal = self._open_modal_shell(
            "Edit product" if editing else "Add product", 600, 640
        )
        modal.columnconfigure(0, weight=1)
        modal.rowconfigure(1, weight=1)
        header = page_header(
            modal,
            "Edit product" if editing else "Add product",
            "Enter product details and at least one price. Stock tracking is optional.",
        )
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 8))
        form = ScrollFrame(modal)
        form.grid(row=1, column=0, sticky="nsew", padx=4)
        body = form.content
        body.columnconfigure(1, weight=1)
        vars_map = {
            "name": tk.StringVar(value=product.get("name", "")),
            "description": tk.StringVar(value=product.get("description", "")),
            "barcode": tk.StringVar(value=product.get("barcode", "")),
            "original_price": tk.StringVar(
                value=str(product.get("original_price", ""))
            ),
            "sell_price": tk.StringVar(value=str(product.get("sell_price", ""))),
            "stock": tk.StringVar(value=str(product.get("stock", 0))),
            "stock_tracked": tk.BooleanVar(
                value=bool(product.get("stock_tracked", False))
            ),
            "parent_linked": tk.BooleanVar(
                value=product.get("parent_product_id") is not None
            ),
            "parent_barcode": tk.StringVar(),
            "parent_units": tk.StringVar(value=str(product.get("parent_units", 1))),
        }
        if editing:
            self._update_vars = vars_map
        else:
            self._create_vars = vars_map
        if product.get("parent_product_id") is not None:
            parent = inventory.get_product_by_id(int(product["parent_product_id"]))
            if parent:
                vars_map["parent_barcode"].set(parent["barcode"])
        entries = {}
        for row, (key, label) in enumerate(
            [
                ("name", "Product name *"),
                ("barcode", "Barcode *"),
                ("description", "Description"),
                ("original_price", "Cost price"),
                ("sell_price", "Selling price"),
                ("stock", "Stock quantity"),
            ]
        ):
            entries[key] = self._field_row(body, label, vars_map[key], row)
        ttk.Checkbutton(
            body,
            text="Track stock for this product",
            variable=vars_map["stock_tracked"],
        ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 4))
        ttk.Label(
            body,
            text="Untracked items can be sold without counting stock.",
            style="Muted.TLabel",
            wraplength=460,
        ).grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 12))
        advanced = ttk.LabelFrame(body, text="Parent stock", padding=12)
        advanced.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        advanced.columnconfigure(1, weight=1)
        self._field_row(advanced, "Parent barcode", vars_map["parent_barcode"], 0)
        self._field_row(advanced, "Units per parent", vars_map["parent_units"], 1)

        def toggle_parent():
            advanced.grid() if vars_map[
                "parent_linked"
            ].get() else advanced.grid_remove()

        ttk.Checkbutton(
            body,
            text="Link stock to a parent item",
            variable=vars_map["parent_linked"],
            command=toggle_parent,
        ).grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 8))
        toggle_parent()
        hint = tk.StringVar()
        ttk.Label(body, textvariable=hint, style="Muted.TLabel", wraplength=460).grid(
            row=10, column=0, columnspan=2, sticky="w"
        )

        def suggest(*args):
            try:
                cost = float(vars_map["original_price"].get())
                hint.set(
                    f"20% markup suggestion: PHP {cost * 1.2:,.2f}"
                    if not vars_map["sell_price"].get()
                    else ""
                )
            except ValueError:
                hint.set("")

        vars_map["original_price"].trace_add("write", suggest)
        vars_map["sell_price"].trace_add("write", suggest)
        footer = ttk.Frame(modal, padding=(20, 12))
        footer.grid(row=2, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)
        error = tk.StringVar()
        ttk.Label(
            footer, textvariable=error, foreground="#be123c", wraplength=540
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        def submit():
            try:
                payload = {key: variable.get() for key, variable in vars_map.items()}
                payload.update(
                    self._resolve_parent_link(
                        product.get("id"), payload["barcode"], vars_map
                    )
                )
                if editing:
                    inventory.update_product(product["id"], payload)
                else:
                    inventory.create_product(payload)
            except ValueError as exc:
                error.set(str(exc))
                return
            modal.destroy()
            self.refresh_products()
            self.status_var.set(
                f"Product {'updated' if editing else 'added'}: {payload['name']}"
            )

        ActionButton(footer, text="Cancel", command=modal.destroy).grid(
            row=1, column=0, sticky="e", padx=(0, 8)
        )
        ActionButton(
            footer,
            text="Save changes" if editing else "Add product",
            variant="Primary",
            command=submit,
        ).grid(row=1, column=1)
        modal.bind("<Control-Return>", lambda e: submit())
        entries["name"].focus_set()

    def _open_restock_modal(self) -> None:
        modal = self._open_modal_shell("Restock products", 760, 640)
        modal.minsize(
            min(600, modal.winfo_screenwidth() - 32),
            min(520, modal.winfo_screenheight() - 80),
        )
        content = ttk.Frame(modal, padding=20)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(2, weight=1)
        page_header(
            content,
            "Restock products",
            "Search by product name or scan a barcode, then select an item to restock.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 12))
        query_var = tk.StringVar()
        qty_var = tk.StringVar(value="1")
        summary_var = tk.StringVar(value="Select a product from the results.")
        status_var = tk.StringVar()
        state = {"product_id": None, "pending": None, "displayed_query": ""}

        search = ttk.Frame(content)
        search.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        search.columnconfigure(0, weight=1)
        ttk.Label(search, text="Product name or barcode", style="Muted.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        query_entry = ttk.Entry(search, textvariable=query_var)
        query_entry.grid(row=1, column=0, sticky="ew")
        box, results = table(
            content,
            ("name", "barcode", "stock", "tracked"),
            ("Product", "Barcode", "Stock", "Tracking"),
            (280, 170, 80, 100),
            height=4,
            empty_text="Enter a product name or barcode to find matching items.",
        )
        box.grid(row=2, column=0, sticky="nsew")
        summary = ttk.Label(
            content, textvariable=summary_var, wraplength=700, justify="left"
        )
        summary.grid(row=3, column=0, sticky="ew", pady=(12, 8))
        content.bind(
            "<Configure>",
            lambda e: summary.configure(wraplength=max(200, e.width - 40)),
            add="+",
        )
        quantity = ttk.Frame(content)
        quantity.grid(row=4, column=0, sticky="ew")
        ttk.Label(quantity, text="Quantity to add").pack(side="left", padx=(0, 12))
        qty_entry = ttk.Entry(quantity, textvariable=qty_var, width=10)
        qty_entry.pack(side="left")
        status = ttk.Label(
            content, textvariable=status_var, style="Muted.TLabel", wraplength=700
        )
        status.grid(row=5, column=0, sticky="ew", pady=(8, 0))
        content.bind(
            "<Configure>",
            lambda e: status.configure(wraplength=max(200, e.width - 40)),
            add="+",
        )
        actions = ttk.Frame(content)
        actions.grid(row=6, column=0, sticky="e", pady=(12, 0))

        def clear_selection():
            state["product_id"] = None
            selected = results.selection()
            if selected:
                results.selection_remove(selected)
            restock_button.configure(state="disabled")
            summary_var.set("Select a product from the results.")

        def select_product(event=None):
            selected = results.selection()
            if not selected or state["displayed_query"] != query_var.get().strip():
                state["product_id"] = None
                restock_button.configure(state="disabled")
                return
            product = inventory.get_product_by_id(int(selected[0]))
            if product is None:
                clear_selection()
                status_var.set("This product is no longer available. Search again.")
                return
            state["product_id"] = product["id"]
            summary_var.set(
                f"{product['name']}\nBarcode: {product['barcode']}  ·  Stock: {product['stock']}  ·  Tracking: {'On' if product.get('stock_tracked') else 'Off'}"
            )
            restock_button.configure(state="normal")

        def focus_quantity(event=None):
            select_product()
            if state["product_id"] is not None:
                qty_entry.focus_set()
                qty_entry.selection_range(0, "end")
            return "break"

        def cancel_pending():
            if state["pending"] is not None:
                modal.after_cancel(state["pending"])
                state["pending"] = None

        def search_products(autoselect_barcode=False):
            cancel_pending()
            clear_selection()
            query = query_var.get().strip()
            state["displayed_query"] = query
            results.delete(*results.get_children())
            products = inventory.search_products(query) if query else []
            for product in products:
                results.insert(
                    "",
                    "end",
                    iid=str(product["id"]),
                    values=(
                        product["name"],
                        product["barcode"],
                        product["stock"],
                        "Tracked" if product.get("stock_tracked") else "Untracked",
                    ),
                )
            results.empty_text = (
                "No matching products found. Try another name or barcode."
                if query
                else "Enter a product name or barcode to find matching items."
            )
            results._refresh_empty()
            status_var.set(
                f"{len(products)} matching products. Select an item to restock."
                if query
                else "Enter a product name or barcode."
            )
            if autoselect_barcode:
                exact = next(
                    (product for product in products if product["barcode"] == query),
                    None,
                )
                if exact is not None:
                    results.selection_set(str(exact["id"]))
                    results.see(str(exact["id"]))
                    focus_quantity()

        def query_changed(*args):
            cancel_pending()
            clear_selection()
            status_var.set("Searching…")

            def delayed_search():
                state["pending"] = None
                search_products()

            state["pending"] = modal.after(200, delayed_search)

        def restock_product(event=None):
            if state["product_id"] is None:
                status_var.set("Select a product from the results first.")
                return "break"
            raw = qty_var.get().strip()
            if not raw.isdecimal() or int(raw) <= 0:
                status_var.set("Enter a whole-number quantity greater than zero.")
                qty_entry.focus_set()
                return "break"
            product = inventory.get_product_by_id(state["product_id"])
            if product is None:
                clear_selection()
                status_var.set("This product is no longer available. Search again.")
                return "break"
            amount = int(raw)
            if not messagebox.askyesno(
                "Confirm restock",
                f"Add {amount} to stock for {product['name']}?\nBarcode: {product['barcode']}",
                parent=modal,
            ):
                return "break"
            try:
                new_stock = inventory.adjust_stock(product["id"], amount)
            except ValueError as exc:
                status_var.set(str(exc))
                return "break"
            self.refresh_products(self.search_var.get())
            message = f"Restocked {product['name']} by {amount}. New stock: {new_stock}"
            self.status_var.set(message)
            if query_var.get().strip() == product["barcode"]:
                query_var.set("")
            qty_var.set("1")
            search_products()
            status_var.set(message)
            query_entry.focus_set()
            query_entry.selection_range(0, "end")
            return "break"

        def on_search_enter(event=None):
            search_products(autoselect_barcode=True)
            return "break"

        ActionButton(search, text="Search", command=on_search_enter).grid(
            row=1, column=1, padx=(8, 0)
        )
        ActionButton(actions, text="Close", command=modal.destroy).pack(
            side="right", padx=(8, 0)
        )
        restock_button = ActionButton(
            actions,
            text="Restock",
            variant="Primary",
            command=restock_product,
            state="disabled",
        )
        restock_button.pack(side="right")
        results.bind("<<TreeviewSelect>>", select_product)
        results.bind("<Double-1>", focus_quantity)
        results.bind("<Return>", focus_quantity)
        query_entry.bind("<Return>", on_search_enter)
        qty_entry.bind("<Return>", restock_product)
        query_var.trace_add("write", query_changed)
        modal.bind(
            "<Destroy>",
            lambda e: cancel_pending() if e.widget is modal else None,
            add="+",
        )
        query_entry.focus_set()

    def _open_delete_modal(self) -> None:
        product = self._selected_product()
        if product is None:
            self.status_var.set("Select a product to delete.")
            return
        modal = self._open_modal_shell("Delete product", 520, 360)
        content = ttk.Frame(modal, padding=24)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)
        ttk.Label(content, text="Delete this product?", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 16)
        )
        ttk.Label(
            content,
            text=f"{product['name']}\n\nBarcode: {product['barcode']}\n\nThis permanently removes the product from Inventory.",
            wraplength=460,
            justify="left",
        ).grid(row=1, column=0, sticky="nw")
        error = tk.StringVar()
        ttk.Label(
            content, textvariable=error, foreground="#be123c", wraplength=460
        ).grid(row=2, column=0, sticky="w", pady=8)
        actions = ttk.Frame(content)
        actions.grid(row=3, column=0, sticky="e")

        def remove():
            try:
                inventory.delete_product(product["id"])
            except ValueError as exc:
                error.set(str(exc))
                return
            modal.destroy()
            self.selected_product_id = None
            self.refresh_products()
            self.status_var.set(f"Product deleted: {product['name']}")

        ActionButton(actions, text="Cancel", command=modal.destroy).pack(
            side="left", padx=(0, 8)
        )
        ActionButton(
            actions, text="Delete product", variant="Danger", command=remove
        ).pack(side="left")

    def _open_settings_modal(self) -> None:
        modal = self._open_modal_shell("Inventory settings", 760, 600)
        modal.columnconfigure(0, weight=1)
        modal.rowconfigure(3, weight=1)
        page_header(
            modal,
            "Inventory settings",
            "Set stock alerts and choose items for POS quick access.",
        ).grid(row=0, column=0, sticky="ew", padx=20, pady=16)
        options = ttk.Frame(modal)
        options.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))
        threshold_var = tk.StringVar(value=str(inventory.get_low_stock_threshold()))
        ttk.Label(options, text="Low-stock threshold").pack(side="left", padx=(0, 12))
        ttk.Entry(options, textvariable=threshold_var, width=8).pack(side="left")
        search_var = tk.StringVar()
        search = ttk.Entry(modal, textvariable=search_var)
        search.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 12))
        box, products = table(
            modal,
            ("name", "price", "stock", "quick"),
            ("Product", "Sell price", "Stock", "Quick access"),
            (260, 100, 70, 120),
            empty_text="No matching products.",
        )
        box.grid(row=3, column=0, sticky="nsew", padx=20)
        quick_ids = list(inventory.get_quick_access_product_ids())

        def load(*args):
            products.delete(*products.get_children())
            for product in inventory.list_products(search_var.get().strip()):
                products.insert(
                    "",
                    "end",
                    iid=str(product["id"]),
                    values=(
                        product["name"],
                        f"{product['sell_price']:,.2f}",
                        product["stock"] if product.get("stock_tracked") else "—",
                        "Included" if product["id"] in quick_ids else "—",
                    ),
                )

        def toggle(event=None):
            selected = products.selection()
            if not selected:
                return
            product_id = int(selected[0])
            quick_ids.remove(
                product_id
            ) if product_id in quick_ids else quick_ids.append(product_id)
            products.set(
                selected[0], "quick", "Included" if product_id in quick_ids else "—"
            )

        products.bind("<Double-1>", toggle)
        products.bind("<space>", toggle)
        search_var.trace_add("write", load)
        feedback = tk.StringVar(
            value="Double-click a product or press Space to toggle quick access."
        )
        footer = ttk.Frame(modal, padding=20)
        footer.grid(row=4, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)
        ttk.Label(
            footer, textvariable=feedback, style="Muted.TLabel", wraplength=680
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))

        def save():
            try:
                value = int(threshold_var.get())
                if value < 0:
                    raise ValueError
            except ValueError:
                feedback.set("Enter a whole-number threshold of zero or more.")
                return
            inventory.set_low_stock_threshold(value)
            inventory.set_quick_access_product_ids(quick_ids)
            self.refresh_products()
            self.status_var.set("Inventory settings saved.")
            modal.destroy()

        ActionButton(footer, text="Toggle quick access", command=toggle).grid(
            row=1, column=0, sticky="w"
        )
        ActionButton(footer, text="Cancel", command=modal.destroy).grid(
            row=1, column=1, padx=(8, 8)
        )
        ActionButton(
            footer, text="Save settings", variant="Primary", command=save
        ).grid(row=1, column=2)
        load()
        search.focus_set()
