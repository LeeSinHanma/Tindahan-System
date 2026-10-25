import tkinter as tk
from tkinter import messagebox, ttk

from core import debt_tracker
from ui import theme as visual
from ui.widgets import (
    ActionButton,
    AdaptivePanels,
    FlowFrame,
    center_dialog,
    page_header,
    table,
)


class DebtTrackerFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        self.theme = visual.get_theme()
        self.selected_customer: str | None = None
        self.selected_debt_id: int | None = None
        self.person_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.sale_linked_var = tk.BooleanVar(value=True)
        self.new_customer_var = tk.StringVar()
        self.new_customer_var.trace_add("write", lambda *args: self.refresh())
        self.status_var = tk.StringVar(value="Manage customer debt accounts.")

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        self.configure(padding=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        page_header(
            self, "Customers & Debt", "Review customer balances and record payments."
        ).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self.panels = AdaptivePanels(self)
        self.panels.grid(row=1, column=0, sticky="nsew")
        left = self.panels.add("Customers")
        right = self.panels.add("Customer details")
        self.detail_panel = right
        left.columnconfigure(0, weight=1)
        left.rowconfigure(3, weight=1)
        ttk.Label(left, text="Customer accounts", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        search = ttk.Entry(left, textvariable=self.new_customer_var)
        search.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        actions = FlowFrame(left)
        actions.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        actions.add(
            ActionButton(
                actions,
                text="New customer",
                variant="Primary",
                command=self._open_customer_dialog,
            )
        )
        self.delete_customer_button = actions.add(
            ActionButton(
                actions,
                text="Delete",
                variant="Danger",
                command=self._delete_customer,
                state="disabled",
            )
        )
        box, self.customer_table = table(
            left,
            ("customer", "total", "pending"),
            ("Customer", "Balance", "Unpaid"),
            (180, 110, 65),
            empty_text="No matching customers. Create a customer account above.",
            height=4,
        )
        box.grid(row=3, column=0, sticky="nsew")
        self.customer_table.bind("<<TreeviewSelect>>", self._on_customer_select)
        self.customer_table.bind("<Double-1>", lambda e: self.panels.show(right))
        self.customer_table.bind("<Return>", lambda e: self.panels.show(right))
        right.columnconfigure(0, weight=1)
        right.rowconfigure(3, weight=1)
        self.person_var.set("Select a customer")
        ttk.Label(right, textvariable=self.person_var, style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        form = ttk.Frame(right)
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(1, weight=1)
        ttk.Label(form, text="Debt amount").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.amount_entry = ttk.Entry(form, textvariable=self.amount_var, width=10)
        self.amount_entry.grid(row=0, column=1, sticky="ew")
        ttk.Label(form, text="Description").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(6, 0)
        )
        self.description_entry = ttk.Entry(form, textvariable=self.description_var)
        self.description_entry.grid(row=1, column=1, sticky="ew", pady=(6, 0))
        tools = FlowFrame(right)
        tools.grid(row=2, column=0, sticky="ew", pady=(8, 8))
        tools.add(
            ttk.Checkbutton(tools, text="Record as sale", variable=self.sale_linked_var)
        )
        self.add_debt_button = tools.add(
            ActionButton(
                tools,
                text="Add debt",
                command=self._add_debt_to_customer,
                state="disabled",
            )
        )
        box, self.debt_table = table(
            right,
            ("id", "amount", "status", "description", "date"),
            ("ID", "Amount", "Status", "Description", "Date"),
            (40, 90, 85, 160, 100),
            displaycolumns=("amount", "status", "description", "date"),
            empty_text="Select a customer to review their debt history.",
            height=3,
        )
        box.grid(row=3, column=0, sticky="nsew")
        self.debt_table.bind("<<TreeviewSelect>>", self._on_debt_select)
        self.debt_table.tag_configure("pending", background="#fffbeb")
        self.debt_table.tag_configure("paid", background="#ecfdf5")
        debt_actions = FlowFrame(right)
        debt_actions.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        self.paid_button = debt_actions.add(
            ActionButton(
                debt_actions,
                text="Mark paid",
                command=self._mark_debt_paid,
                state="disabled",
            )
        )
        self.delete_debt_button = debt_actions.add(
            ActionButton(
                debt_actions,
                text="Delete debt",
                variant="Danger",
                command=self._delete_debt,
                state="disabled",
            )
        )
        pay = ttk.Frame(right)
        pay.grid(row=5, column=0, sticky="ew", pady=(8, 0))
        pay.columnconfigure(1, weight=1)
        ttk.Label(pay, text="Payment").grid(row=0, column=0, padx=(0, 8))
        self.pay_amount_var = tk.StringVar()
        pay_entry = ttk.Entry(pay, textvariable=self.pay_amount_var, width=10)
        pay_entry.grid(row=0, column=1, sticky="ew")
        self.pay_button = ActionButton(
            pay,
            text="Record payment",
            variant="Primary",
            command=self._pay_amount_for_customer,
            state="disabled",
        )
        self.pay_button.grid(row=0, column=2, padx=(8, 0))
        pay_entry.bind("<Return>", lambda e: self._pay_amount_for_customer())
        self.pay_amount_var.trace_add(
            "write", lambda *args: self._update_pay_button_state()
        )
        status = ttk.Label(
            self, textvariable=self.status_var, style="Muted.TLabel", wraplength=700
        )
        status.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        self.bind(
            "<Configure>",
            lambda e: status.configure(wraplength=max(200, e.width)),
            add="+",
        )

    def _open_customer_dialog(self):
        modal = tk.Toplevel(self)
        modal.title("New customer")
        modal.transient(self.winfo_toplevel())
        modal.resizable(False, False)
        center_dialog(modal, 440, 260)
        content = ttk.Frame(modal, padding=24)
        content.pack(fill="both", expand=True)
        ttk.Label(content, text="New customer", style="Section.TLabel").pack(
            anchor="w", pady=(0, 16)
        )
        name = tk.StringVar()
        error = tk.StringVar()
        entry = ttk.Entry(content, textvariable=name)
        entry.pack(fill="x")
        ttk.Label(
            content, textvariable=error, foreground="#be123c", wraplength=380
        ).pack(anchor="w", pady=8)

        def submit():
            customer_name = name.get().strip()
            if not customer_name or not debt_tracker.add_customer(customer_name):
                error.set("Enter a unique customer name.")
                return
            self.new_customer_var.set("")
            self.selected_customer = customer_name
            self.person_var.set(customer_name)
            self.refresh()
            modal.destroy()
            self.panels.show(self.detail_panel)

        ActionButton(
            content, text="Create customer", variant="Primary", command=submit
        ).pack(anchor="e")
        modal.bind("<Return>", lambda e: submit())
        modal.grab_set()
        entry.focus_set()

    def _update_customer_actions(self):
        state = "normal" if self.selected_customer else "disabled"
        self.add_debt_button.configure(state=state)
        self.delete_customer_button.configure(state=state)
        selected = bool(self.debt_table.selection())
        for button in (self.paid_button, self.delete_debt_button):
            button.configure(state="normal" if selected else "disabled")

    def _delete_customer(self) -> None:
        if not self.selected_customer:
            messagebox.showerror(
                "Invalid input", "Please select a customer to delete", parent=self
            )
            return

        customer_name = self.selected_customer
        customer_debts = debt_tracker.get_customer_debts(customer_name)
        pending_count = sum(1 for debt in customer_debts if not debt.get("is_paid", 0))
        total_count = len(customer_debts)

        confirm_message = (
            f"Delete customer account '{customer_name}'?\n\n"
            f"This will remove {total_count} debt record(s) "
            f"({pending_count} pending).\n"
            "This action cannot be undone."
        )
        if not messagebox.askyesno("Confirm Delete", confirm_message, parent=self):
            return

        if debt_tracker.delete_customer(customer_name):
            self.status_var.set(f"Customer '{customer_name}' deleted")
            self.selected_customer = None
            self.selected_debt_id = None
            self.person_var.set("")
            self.amount_var.set("")
            self.description_var.set("")
            self.pay_amount_var.set("")
            for row_id in self.debt_table.get_children():
                self.debt_table.delete(row_id)
            self.refresh()
        else:
            messagebox.showerror(
                "Delete failed", "Failed to delete customer", parent=self
            )

    def _on_customer_select(self, _event: tk.Event) -> None:
        selected = self.customer_table.selection()
        if selected:
            values = self.customer_table.item(selected[0], "values")
            self.selected_customer = values[0]
            self.person_var.set(self.selected_customer)
            self.amount_var.set("")
            self.description_var.set("")
            self._load_customer_debts()
            self._update_customer_actions()
            self._update_pay_button_state()

    def _on_debt_select(self, _event: tk.Event) -> None:
        selected = self.debt_table.selection()
        if selected:
            values = self.debt_table.item(selected[0], "values")
            self.selected_debt_id = int(values[0])
        else:
            self.selected_debt_id = None
        self._update_customer_actions()

    def _load_customer_debts(self) -> None:
        if not self.selected_customer:
            return

        for row_id in self.debt_table.get_children():
            self.debt_table.delete(row_id)

        self.selected_debt_id = None
        self.debt_table.empty_text = "This customer has no debt records."
        self.debt_table._refresh_empty()
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
            messagebox.showerror(
                "Invalid input", "Please select a customer first", parent=self
            )
            return

        amount_str = self.amount_var.get().strip()
        description = self.description_var.get().strip()

        if not amount_str:
            messagebox.showerror("Invalid input", "Please enter an amount", parent=self)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror(
                "Invalid input", "Please enter a valid amount", parent=self
            )
            return

        if debt_tracker.add_debt(
            self.selected_customer, amount, description, self.sale_linked_var.get()
        ):
            self.amount_var.set("")
            self.description_var.set("")
            self.sale_linked_var.set(True)
            self.status_var.set(
                f"Added PHP {amount:.2f} debt for {self.selected_customer}"
            )
            self.refresh()
        else:
            messagebox.showerror("Invalid input", "Failed to add debt", parent=self)

    def _pay_amount_for_customer(self) -> None:
        if not self.selected_customer:
            messagebox.showerror(
                "Invalid input", "Select a customer first", parent=self
            )
            return

        amt_text = self.pay_amount_var.get().strip()
        if not amt_text:
            messagebox.showerror("Invalid input", "Enter an amount to pay", parent=self)
            return

        try:
            amount = float(amt_text)
        except ValueError:
            messagebox.showerror(
                "Invalid input", "Enter a valid numeric amount", parent=self
            )
            return

        total_debt = debt_tracker.get_customer_total_debt(self.selected_customer)
        if amount <= 0:
            messagebox.showerror(
                "Invalid input",
                "Enter an amount greater than PHP 0.00 to pay.",
                parent=self,
            )
            self._update_pay_button_state()
            self._update_customer_actions()
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
            self.status_var.set(
                f"Applied PHP {applied:.2f} to {self.selected_customer}. Remaining: PHP {remaining:.2f}"
            )
        self.refresh()

    def _mark_debt_paid(self) -> None:
        if not self.selected_debt_id:
            messagebox.showerror(
                "Invalid input", "Please select a debt to mark as paid", parent=self
            )
            return

        if not messagebox.askyesno(
            "Confirm Payment", "Mark this selected debt as paid?", parent=self
        ):
            return

        if debt_tracker.mark_paid(self.selected_debt_id):
            self.status_var.set("Debt marked as paid")
            self.selected_debt_id = None
            self.refresh()
        else:
            self.status_var.set("Failed to mark debt as paid")

    def _delete_debt(self) -> None:
        if not self.selected_debt_id:
            messagebox.showerror(
                "Invalid input", "Please select a debt to delete", parent=self
            )
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
                total_debt = debt_tracker.get_customer_total_debt(
                    self.selected_customer
                )
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
        self._update_customer_actions()
