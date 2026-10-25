import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core import inventory, shopping_list
from ui import theme as visual
from ui.theme import get_theme
from ui.widgets import ActionButton, AdaptivePanels, FlowFrame, page_header, table


class ShoppingListFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        top_level = master.winfo_toplevel()
        self.theme = get_theme()
        self.selected_product_id: int | None = None
        self.selected_list_item_id: int | None = None
        self.checked_product_ids: set[int] = set()
        self.checked_list_item_ids: set[int] = set()

        self.product_search_var = tk.StringVar()
        self.qty_var = tk.StringVar(value="1")
        self.include_done_var = tk.BooleanVar(value=True)
        self.total_var = tk.StringVar(value="Total: PHP 0.00")
        self.status_var = tk.StringVar(
            value="Create a shopping list from existing products."
        )

        self._build_ui()
        self.refresh()
        top_level.bind("<F1>", self._on_select_all_hotkey, add="+")
        top_level.bind("<F2>", self._on_clear_selection_hotkey, add="+")
        top_level.bind("<F3>", self._on_mark_done_hotkey, add="+")
        top_level.bind("<F4>", self._on_mark_pending_hotkey, add="+")
        top_level.bind("<F5>", self._on_remove_hotkey, add="+")
        top_level.bind("<F6>", self._on_set_qty_hotkey, add="+")
        top_level.bind("<F7>", self._on_clear_done_hotkey, add="+")

    def _build_ui(self) -> None:
        self.configure(padding=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        page_header(
            self,
            "Shopping List",
            "Plan your next restock. Add products, set quantities, and track purchases.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self.panels = AdaptivePanels(self)
        self.panels.grid(row=1, column=0, sticky="nsew")
        self._build_product_panel(self.panels.add("Find products"))
        self._build_list_panel(self.panels.add("Shopping list"))
        status = ttk.Label(
            self, textvariable=self.status_var, style="Muted.TLabel", wraplength=700
        )
        status.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        self.bind(
            "<Configure>",
            lambda e: status.configure(wraplength=max(200, e.width)),
            add="+",
        )

    def _build_product_panel(self, panel) -> None:
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(2, weight=1)
        ttk.Label(panel, text="Products", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        search = ttk.Frame(panel)
        search.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        search.columnconfigure(0, weight=1)
        entry = ttk.Entry(search, textvariable=self.product_search_var, width=12)
        entry.grid(row=0, column=0, sticky="ew")
        entry.bind("<Return>", self._search_products)
        ActionButton(search, text="Search", command=self._search_products).grid(
            row=0, column=1, padx=(6, 0)
        )
        box, self.product_table = table(
            panel,
            ("pick", "id", "name", "price"),
            ("Pick", "ID", "Product", "Cost"),
            (45, 44, 180, 80),
            displaycolumns=("pick", "name", "price"),
            empty_text="No matching products. Add products in Inventory first.",
            height=4,
        )
        box.grid(row=2, column=0, sticky="nsew")
        self.product_table.bind("<<TreeviewSelect>>", self._on_product_select)
        self.product_table.bind("<Button-1>", self._toggle_product_check)
        self.product_table.bind("<space>", self._toggle_product_keyboard)
        actions = FlowFrame(panel)
        actions.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        actions.add(ttk.Label(actions, text="Quantity"))
        qty = actions.add(ttk.Entry(actions, textvariable=self.qty_var, width=4))
        qty.bind("<Return>", self._add_checked_to_list_event)
        self.add_products_button = actions.add(
            ActionButton(
                actions,
                text="Add selected",
                variant="Primary",
                command=self._add_checked_to_list,
                state="disabled",
            )
        )
        actions.add(
            ActionButton(
                actions, text="Add low stock", command=self._add_low_stock_items
            )
        )

    def _add_checked_to_list_event(self, event=None):
        self._add_checked_to_list()

    def _toggle_product_keyboard(self, event=None):
        selected = self.product_table.selection()
        if selected:
            product_id = int(self.product_table.item(selected[0], "values")[1])
            if product_id in self.checked_product_ids:
                self.checked_product_ids.remove(product_id)
            else:
                self.checked_product_ids.add(product_id)
            self.product_table.set(
                selected[0],
                "pick",
                "[x]" if product_id in self.checked_product_ids else "[ ]",
            )
            self._update_selection_actions()
        return "break"

    def _build_list_panel(self, panel) -> None:
        self.list_panel = panel
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(3, weight=1)
        ttk.Label(panel, text="Restock list", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        ttk.Label(
            panel, textvariable=self.total_var, font=(visual.FONT, 16, "bold")
        ).grid(row=1, column=0, sticky="w", pady=(0, 8))
        toolbar = FlowFrame(panel)
        toolbar.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        toolbar.add(
            ttk.Checkbutton(
                toolbar,
                text="Show completed",
                variable=self.include_done_var,
                command=self.refresh,
            )
        )
        toolbar.add(ActionButton(toolbar, text="Save PDF", command=self._save_pdf))
        more = ttk.Menubutton(toolbar, text="More")
        menu = tk.Menu(more, tearoff=False)
        for label, command in [
            ("Select all · F1", self._select_all_list_items),
            ("Clear selection · F2", self._clear_list_selection),
            ("Set quantity · F6", self._set_selected_qty),
            ("Clear completed · F7", self._clear_done_items),
            ("Remove all items", self._remove_all),
            ("Refresh", self.refresh),
        ]:
            menu.add_command(label=label, command=command)
        more.configure(menu=menu)
        toolbar.add(more)
        box, self.list_table = table(
            panel,
            ("pick", "id", "name", "original_price", "qty", "status"),
            ("Pick", "ID", "Product", "Cost", "Qty", "Status"),
            (45, 44, 180, 80, 45, 85),
            displaycolumns=("pick", "name", "original_price", "qty", "status"),
            empty_text="Your restock list is empty. Add products from Find products.",
            height=4,
        )
        box.grid(row=3, column=0, sticky="nsew")
        self.list_table.bind("<<TreeviewSelect>>", self._on_list_item_select)
        self.list_table.bind("<Button-1>", self._toggle_list_item_check)
        self.list_table.bind("<space>", self._toggle_list_keyboard)
        actions = FlowFrame(panel)
        actions.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        self.list_action_buttons = [
            actions.add(
                ActionButton(
                    actions,
                    text="Mark purchased · F3",
                    command=lambda: self._mark_selected_done(True),
                    state="disabled",
                )
            ),
            actions.add(
                ActionButton(
                    actions,
                    text="Mark pending · F4",
                    command=lambda: self._mark_selected_done(False),
                    state="disabled",
                )
            ),
            actions.add(
                ActionButton(
                    actions,
                    text="Remove · F5",
                    variant="Danger",
                    command=self._remove_selected,
                    state="disabled",
                )
            ),
        ]

    def _toggle_list_keyboard(self, event=None):
        selected = self.list_table.selection()
        if selected:
            item_id = int(self.list_table.item(selected[0], "values")[1])
            if item_id in self.checked_list_item_ids:
                self.checked_list_item_ids.remove(item_id)
            else:
                self.checked_list_item_ids.add(item_id)
            self.list_table.set(
                selected[0],
                "pick",
                "[x]" if item_id in self.checked_list_item_ids else "[ ]",
            )
            self._update_selection_actions()
        return "break"

    def _search_products(self, _event: tk.Event | None = None) -> None:
        self._load_products(self.product_search_var.get())

    def _load_products(self, search_term: str = "") -> None:
        products = (
            inventory.search_products(search_term)
            if search_term.strip()
            else inventory.list_products()
        )
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

        selected = f"p{self.selected_product_id}"
        if self.product_table.exists(selected):
            self.product_table.selection_set(selected)
        else:
            self.selected_product_id = None
        self._update_selection_actions()

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
                    f"{item['product']['original_price']:.2f}",
                    item["quantity"],
                    status,
                ),
                tags=("done",) if item["is_done"] else (),
            )

        self.list_table.tag_configure("done", background="#dcfce7")
        self.total_var.set(f"Total: PHP {shopping_list.get_total():.2f}")
        self.status_var.set(f"{len(items)} items on your restock list")
        selected = f"s{self.selected_list_item_id}"
        if self.list_table.exists(selected):
            self.list_table.selection_set(selected)
        else:
            self.selected_list_item_id = None
        self._update_selection_actions()

    def _add_low_stock_items(self) -> None:
        added_count = shopping_list.add_low_stock_items()
        self.checked_product_ids.clear()
        self.checked_list_item_ids.clear()
        self._load_products(self.product_search_var.get())
        self._load_list_items()
        self.status_var.set(f"Added {added_count} low-stock item(s) to shopping list")

    def _on_product_select(self, _event=None) -> None:
        selected = self.product_table.selection()
        self.selected_product_id = (
            int(self.product_table.item(selected[0], "values")[1]) if selected else None
        )
        self._update_selection_actions()

    def _update_selection_actions(self):
        state = (
            "normal"
            if self.checked_product_ids or self.selected_product_id is not None
            else "disabled"
        )
        self.add_products_button.configure(state=state)
        state = (
            "normal"
            if self.checked_list_item_ids or self.selected_list_item_id is not None
            else "disabled"
        )
        for button in self.list_action_buttons:
            button.configure(state=state)

    def _on_list_item_select(self, _event=None) -> None:
        selected = self.list_table.selection()
        self.selected_list_item_id = (
            int(self.list_table.item(selected[0], "values")[1]) if selected else None
        )
        self._update_selection_actions()

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

    def _shopping_list_hotkey_active(self) -> bool:
        return getattr(self.winfo_toplevel(), "active_screen", None) == "shopping_list"

    def _on_select_all_hotkey(self, _event: tk.Event | None = None) -> str:
        if not self._shopping_list_hotkey_active():
            return ""
        self._select_all_list_items()
        return "break"

    def _on_clear_selection_hotkey(self, _event: tk.Event | None = None) -> str:
        if not self._shopping_list_hotkey_active():
            return ""
        self._clear_list_selection()
        return "break"

    def _on_mark_done_hotkey(self, _event: tk.Event | None = None) -> str:
        if not self._shopping_list_hotkey_active():
            return ""
        self._mark_selected_done(True)
        return "break"

    def _on_mark_pending_hotkey(self, _event: tk.Event | None = None) -> str:
        if not self._shopping_list_hotkey_active():
            return ""
        self._mark_selected_done(False)
        return "break"

    def _on_remove_hotkey(self, _event: tk.Event | None = None) -> str:
        if not self._shopping_list_hotkey_active():
            return ""
        self._remove_selected()
        return "break"

    def _on_set_qty_hotkey(self, _event: tk.Event | None = None) -> str:
        if not self._shopping_list_hotkey_active():
            return ""
        self._set_selected_qty()
        return "break"

    def _on_clear_done_hotkey(self, _event: tk.Event | None = None) -> str:
        if not self._shopping_list_hotkey_active():
            return ""
        self._clear_done_items()
        return "break"

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
            messagebox.showerror("Invalid input", "Select a product first", parent=self)
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
            messagebox.showerror(
                "Invalid input", "Select or check product(s) first", parent=self
            )
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
            messagebox.showerror(
                "Invalid input",
                "Select or check shopping-list item(s) first",
                parent=self,
            )
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
            messagebox.showerror(
                "Invalid input",
                "Select or check shopping-list item(s) first",
                parent=self,
            )
            return

        for item_id in item_ids:
            shopping_list.mark_done(item_id, is_done)

        self.checked_list_item_ids.clear()
        self._load_list_items()
        self.status_var.set(f"Status updated for {len(item_ids)} item(s)")

    def _remove_selected(self) -> None:
        item_ids = self._target_list_item_ids()
        if not item_ids:
            messagebox.showerror(
                "Invalid input",
                "Select or check shopping-list item(s) first",
                parent=self,
            )
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
