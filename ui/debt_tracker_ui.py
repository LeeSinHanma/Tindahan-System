import tkinter as tk
from tkinter import messagebox, ttk

from core import debt_tracker
from .theme_manager import ThemeManager


class DebtTrackerFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        top_level = master.winfo_toplevel()
        screen_w = top_level.winfo_screenwidth()
        screen_h = top_level.winfo_screenheight()
        self.compact_layout = screen_w < 1400 or screen_h < 820
        self.theme = ThemeManager(self.compact_layout)
        self.selected_customer: str | None = None
        self.selected_debt_id: int | None = None
        self.person_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.new_customer_var = tk.StringVar()
        self.new_customer_var.trace_add("write", lambda *args: self.refresh())
        self.status_var = tk.StringVar(value="Manage customer debt accounts.")

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X)

        ttk.Label(header, text="Debt Tracker", font=("Segoe UI", self.theme.heading_huge, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="View customer accounts and manage individual debts.",
            font=("Segoe UI", self.theme.body_medium),
        ).pack(anchor="w", pady=(4, 0))

        # Customers section
        customers_label = ttk.Label(header, text="Customers", font=("Segoe UI", self.theme.body_medium, "bold"))
        customers_label.pack(anchor="w", pady=(12, 8))

        customers_frame = ttk.Frame(self)
        customers_frame.pack(fill=tk.BOTH, expand=True)
        customers_frame.rowconfigure(0, weight=1)
        customers_frame.columnconfigure(0, weight=2)
        customers_frame.columnconfigure(1, weight=3)

        # Left panel: Customer list
        left_panel = ttk.Frame(customers_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left_panel.rowconfigure(1, weight=1)

        ttk.Label(left_panel, text="Customer Accounts", font=("Segoe UI", self.theme.body_medium, "bold")).pack(anchor="w", pady=(0, 6))

        # New customer form
        new_cust_row = ttk.Frame(left_panel)
        new_cust_row.pack(fill=tk.X, pady=(0, 6))
        new_cust_entry = ttk.Entry(new_cust_row, textvariable=self.new_customer_var)
        new_cust_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._create_button(new_cust_row, "New Customer", self._add_customer, "#4f46e5", self.theme.button_padding_x, self.theme.button_padding_y, self.theme.body_small).pack(side=tk.LEFT, padx=(6, 0))

        customer_table_frame = ttk.Frame(left_panel)
        customer_table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("customer", "total", "pending")
        self.customer_table = ttk.Treeview(customer_table_frame, columns=columns, show="headings", height=12)
        self.customer_table.heading("customer", text="Customer")
        self.customer_table.heading("total", text="Total Debt")
        self.customer_table.heading("pending", text="Items")

        self.customer_table.column("customer", width=self.theme.table_column_width_name)
        self.customer_table.column("total", width=100, anchor=tk.E)
        self.customer_table.column("pending", width=70, anchor=tk.CENTER)
        self.customer_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        customer_scroll = ttk.Scrollbar(customer_table_frame, orient=tk.VERTICAL, command=self.customer_table.yview)
        customer_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.customer_table.configure(yscrollcommand=customer_scroll.set)
        self.customer_table.bind("<<TreeviewSelect>>", self._on_customer_select)

        # Right panel: Customer details and debts
        right_panel = ttk.LabelFrame(customers_frame, text="Customer Details", padding=10)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.rowconfigure(3, weight=1)

        # Customer info
        info_frame = ttk.Frame(right_panel)
        info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(info_frame, text="Customer:", font=("Segoe UI", self.theme.body_small, "bold")).pack(side=tk.LEFT)
        ttk.Label(info_frame, textvariable=self.person_var, font=("Segoe UI", self.theme.body_small)).pack(side=tk.LEFT, padx=(8, 0))

        # Add debt form
        form_frame = ttk.LabelFrame(right_panel, text="Add New Debt", padding=8)
        form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Amount:", font=("Segoe UI", self.theme.body_small, "bold")).grid(row=0, column=0, sticky="w")
        amount_entry = ttk.Entry(form_frame, textvariable=self.amount_var, font=("Segoe UI", self.theme.body_small))
        amount_entry.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        ttk.Label(form_frame, text="Description:", font=("Segoe UI", self.theme.body_small, "bold")).grid(row=1, column=0, sticky="w", pady=(6, 0))
        desc_entry = ttk.Entry(form_frame, textvariable=self.description_var, font=("Segoe UI", self.theme.body_small))
        desc_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(6, 0))

        self._create_button(form_frame, "Add Debt", self._add_debt_to_customer, "#16a34a", self.theme.button_padding_x, self.theme.button_padding_y, self.theme.body_small).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        # Debts list for selected customer
        debts_label = ttk.Label(right_panel, text="Debts", font=("Segoe UI", self.theme.body_medium, "bold"))
        debts_label.grid(row=2, column=0, sticky="w", pady=(8, 6))

        debts_table_frame = ttk.Frame(right_panel)
        debts_table_frame.grid(row=3, column=0, sticky="nsew")

        debt_columns = ("id", "amount", "status", "description", "date")
        self.debt_table = ttk.Treeview(debts_table_frame, columns=debt_columns, show="headings", height=8)
        self.debt_table.heading("id", text="ID")
        self.debt_table.heading("amount", text="Amount")
        self.debt_table.heading("status", text="Status")
        self.debt_table.heading("description", text="Description")
        self.debt_table.heading("date", text="Date")

        self.debt_table.column("id", width=40, anchor=tk.CENTER)
        self.debt_table.column("amount", width=80, anchor=tk.E)
        self.debt_table.column("status", width=70, anchor=tk.CENTER)
        self.debt_table.column("description", width=120)
        self.debt_table.column("date", width=90, anchor=tk.CENTER)
        self.debt_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        debt_scroll = ttk.Scrollbar(debts_table_frame, orient=tk.VERTICAL, command=self.debt_table.yview)
        debt_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.debt_table.configure(yscrollcommand=debt_scroll.set)
        self.debt_table.bind("<<TreeviewSelect>>", self._on_debt_select)

        self.debt_table.tag_configure("pending", background="#fff2cc")
        self.debt_table.tag_configure("paid", background="#d1fae5")

        # Debt actions
        action_frame = ttk.Frame(right_panel)
        action_frame.grid(row=4, column=0, sticky="ew", pady=(8, 0))

        self._create_button(action_frame, "Mark Paid", self._mark_debt_paid, "#0ea5e9", self.theme.button_padding_x, self.theme.button_padding_y, self.theme.body_small).pack(side=tk.LEFT)
        self._create_button(action_frame, "Delete", self._delete_debt, "#dc2626", self.theme.button_padding_x, self.theme.button_padding_y, self.theme.body_small).pack(side=tk.LEFT, padx=(6, 0))
        # Pay by amount controls
        pay_frame = ttk.Frame(right_panel)
        pay_frame.grid(row=5, column=0, sticky="ew", pady=(8, 0))
        pay_frame.columnconfigure(0, weight=1)
        self.pay_amount_var = tk.StringVar()
        ttk.Label(pay_frame, text="Pay Amount:", font=("Segoe UI", self.theme.body_small, "bold")).grid(row=0, column=0, sticky="w")
        pay_entry = ttk.Entry(pay_frame, textvariable=self.pay_amount_var)
        pay_entry.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        self.pay_button = tk.Button(
            pay_frame,
            text="Pay",
            command=self._pay_amount_for_customer,
            bg="#059669",
            fg="white",
            relief=tk.FLAT,
            padx=self.theme.button_padding_x,
            pady=self.theme.button_padding_y,
        )
        self.pay_button.grid(row=0, column=2, padx=(8, 0))
        pay_entry.bind("<Return>", lambda _event: self._pay_amount_for_customer() or "break")
        pay_entry.bind("<KeyRelease>", lambda _event: self._update_pay_button_state())

        footer = ttk.Frame(self)
        footer.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(footer, textvariable=self.status_var).pack(side=tk.LEFT)

    def _create_button(self, parent: tk.Widget, text: str, command, color: str, padx: int, pady: int, font_size: int) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief=tk.FLAT,
            padx=padx,
            pady=pady,
            font=("Segoe UI", font_size, "bold"),
            cursor="hand2",
        )

    def _add_customer(self) -> None:
        name = self.new_customer_var.get().strip()
        if not name:
            messagebox.showerror("Invalid input", "Enter a customer name", parent=self)
            return
        if debt_tracker.add_customer(name):
            self.new_customer_var.set("")
            self.status_var.set(f"Customer '{name}' added")
            self.refresh()
        else:
            messagebox.showerror("Invalid input", "Failed to add customer or customer already exists", parent=self)

    def _on_customer_select(self, _event: tk.Event) -> None:
        selected = self.customer_table.selection()
        if selected:
            values = self.customer_table.item(selected[0], "values")
            self.selected_customer = values[0]
            self.person_var.set(self.selected_customer)
            self.amount_var.set("")
            self.description_var.set("")
            self._load_customer_debts()

    def _on_debt_select(self, _event: tk.Event) -> None:
        selected = self.debt_table.selection()
        if selected:
            values = self.debt_table.item(selected[0], "values")
            self.selected_debt_id = int(values[0])

    def _load_customer_debts(self) -> None:
        if not self.selected_customer:
            return

        for row_id in self.debt_table.get_children():
            self.debt_table.delete(row_id)

        debts = debt_tracker.get_customer_debts(self.selected_customer)
        for debt in debts:
            status = "PAID" if debt["is_paid"] else "PENDING"
            tag = "paid" if debt["is_paid"] else "pending"
            self.debt_table.insert(
                "",
                tk.END,
                iid=str(debt["id"]),
                values=(
                    debt["id"],
                    f"{debt['amount']:.2f}",
                    status,
                    debt["description"] or "-",
                    debt["created_at"][:10],
                ),
                tags=(tag,),
            )

    def _add_debt_to_customer(self) -> None:
        if not self.selected_customer:
            messagebox.showerror("Invalid input", "Please select a customer first", parent=self)
            return

        amount_str = self.amount_var.get().strip()
        description = self.description_var.get().strip()

        if not amount_str:
            messagebox.showerror("Invalid input", "Please enter an amount", parent=self)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid amount", parent=self)
            return

        confirm = messagebox.askyesno(
            "Confirm Add Debt",
            f"Add PHP {amount:.2f} debt for {self.selected_customer}?\n\nDescription: {description or '-'}",
            parent=self,
        )
        if not confirm:
            return

        if debt_tracker.add_debt(self.selected_customer, amount, description):
            self.amount_var.set("")
            self.description_var.set("")
            self.status_var.set(f"Added PHP {amount:.2f} debt for {self.selected_customer}")
            self.refresh()
        else:
            messagebox.showerror("Invalid input", "Failed to add debt", parent=self)

    def _pay_amount_for_customer(self) -> None:
        if not self.selected_customer:
            messagebox.showerror("Invalid input", "Select a customer first", parent=self)
            return

        amt_text = self.pay_amount_var.get().strip()
        if not amt_text:
            messagebox.showerror("Invalid input", "Enter an amount to pay", parent=self)
            return

        try:
            amount = float(amt_text)
        except ValueError:
            messagebox.showerror("Invalid input", "Enter a valid numeric amount", parent=self)
            return

        total_debt = debt_tracker.get_customer_total_debt(self.selected_customer)
        if amount <= 0:
            messagebox.showerror(
                "Invalid input",
                "Enter an amount greater than PHP 0.00 to pay.",
                parent=self,
            )
            self._update_pay_button_state()
            return

        confirm_message = f"Apply PHP {amount:.2f} payment to {self.selected_customer}?"
        if amount > total_debt:
            change = amount - total_debt
            confirm_message = (
                f"The pay amount is higher than the current debt.\n\n"
                f"Current debt: PHP {total_debt:.2f}\n"
                f"Amount given: PHP {amount:.2f}\n"
                f"Change: PHP {change:.2f}\n\n"
                "Do you want to continue?"
            )

        confirm = messagebox.askyesno("Confirm Payment", confirm_message, parent=self)
        if not confirm:
            return

        summary = debt_tracker.apply_payment_to_customer(self.selected_customer, amount)
        applied = summary.get("applied", 0.0)
        remaining = summary.get("remaining", 0.0)
        if applied <= 0:
            self.status_var.set("No unpaid debts to apply payment to")
            return

        self.pay_amount_var.set("")
        if amount > total_debt:
            self.status_var.set(
                f"Applied PHP {applied:.2f} to {self.selected_customer}. Change: PHP {remaining:.2f}"
            )
        else:
            self.status_var.set(f"Applied PHP {applied:.2f} to {self.selected_customer}. Remaining: PHP {remaining:.2f}")
        self.refresh()

    def _mark_debt_paid(self) -> None:
        if not self.selected_debt_id:
            messagebox.showerror("Invalid input", "Please select a debt to mark as paid", parent=self)
            return

        if not messagebox.askyesno("Confirm Payment", "Mark this selected debt as paid?", parent=self):
            return

        if debt_tracker.mark_paid(self.selected_debt_id):
            self.status_var.set("Debt marked as paid")
            self.selected_debt_id = None
            self.refresh()
        else:
            self.status_var.set("Failed to mark debt as paid")

    def _delete_debt(self) -> None:
        if not self.selected_debt_id:
            messagebox.showerror("Invalid input", "Please select a debt to delete", parent=self)
            return

        if messagebox.askyesno("Confirm", "Delete this debt entry?"):
            if debt_tracker.delete_debt(self.selected_debt_id):
                self.status_var.set("Debt deleted")
                self.selected_debt_id = None
                self.refresh()
            else:
                self.status_var.set("Failed to delete debt")

    def _update_pay_button_state(self) -> None:
        if not hasattr(self, "pay_button"):
            return

        enabled = False
        if self.selected_customer:
            try:
                amount = float(self.pay_amount_var.get().strip())
                total_debt = debt_tracker.get_customer_total_debt(self.selected_customer)
                enabled = amount > 0 and total_debt > 0
            except ValueError:
                enabled = False
            except Exception:
                enabled = False

        self.pay_button.config(state=tk.NORMAL if enabled else tk.DISABLED)

    def refresh(self) -> None:
        # Refresh customer list
        for row_id in self.customer_table.get_children():
            self.customer_table.delete(row_id)

        search_term = self.new_customer_var.get().strip().lower()
        customers = debt_tracker.get_customers_with_totals()
        for customer in customers:
            if search_term and search_term not in customer["person_name"].lower():
                continue
            # show all customers, even if total_debt is zero
            total = customer.get("total_debt") or 0.0
            pending = customer.get("pending_count") or 0
            self.customer_table.insert(
                "",
                tk.END,
                values=(
                    customer["person_name"],
                    f"{total:.2f}",
                    pending,
                ),
            )

        # Refresh debts if a customer is selected
        if self.selected_customer:
            self._load_customer_debts()

        # Update status
        total_debt = debt_tracker.get_total_debt()
        self.status_var.set(f"Total pending debt: PHP {total_debt:.2f}")
        self._update_pay_button_state()
