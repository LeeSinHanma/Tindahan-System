"""Shared cash-in/out tracking, independent of the product checkout flow."""

import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from core import cash_out
from ui import theme as visual
from ui.widgets import (
    ActionButton,
    FlowFrame,
    MetricGrid,
    ScrollFrame,
    center_dialog,
    page_header,
    table,
)

SERVICES = {"Cash-Out": "cash_out", "Cash-In": "cash_in"}
TYPE_LABELS = {value: label for label, value in SERVICES.items()}


def account_roles(transaction_type):
    if transaction_type == "cash_in":
        return "Shop sending account", "Customer receiving account"
    return "Shop receiving account", "Customer sending account"


def status_text(row):
    if row["transaction_type"] == "cash_in":
        return "Completed" if row["status"] == "claimed" else "Pending"
    return "Claimed" if row["status"] == "claimed" else "Unclaimed"


def completion_action(row):
    return (
        "Confirm transfer completed"
        if row["transaction_type"] == "cash_in"
        else "Confirm cash handed over"
    )


class CashOutFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.reference_var = tk.StringVar()
        self.status_filter = tk.StringVar(value="All statuses")
        self.type_filter = tk.StringVar(value="Both services")
        self.fee_service_var = tk.StringVar(value="Both services")
        self.account_filter = tk.StringVar(value="All shop accounts")
        self.status_var = tk.StringVar()
        self._transactions = {}
        self._accounts = {}
        self._account_labels = {}
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        page_header(
            self,
            "Cash In / Out",
            "Track cash-in and cash-out transfers, completion, and service fees.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        self.transactions_panel = ttk.Frame(self.notebook, padding=12)
        self.totals_panel = ttk.Frame(self.notebook, padding=12)
        self.accounts_panel = ttk.Frame(self.notebook, padding=12)
        self.rules_panel = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.transactions_panel, text="Transactions")
        self.notebook.add(self.totals_panel, text="Fee totals")
        self.notebook.add(self.accounts_panel, text="Accounts")
        self.notebook.add(self.rules_panel, text="Fee rules")
        self._build_transactions()
        self._build_totals()
        self._build_accounts()
        self._build_rules()
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        status = ttk.Label(
            self, textvariable=self.status_var, style="Muted.TLabel", wraplength=700
        )
        status.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        self.bind(
            "<Configure>",
            lambda e: status.configure(wraplength=max(200, e.width)),
            add="+",
        )

    def _build_transactions(self):
        panel = self.transactions_panel
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(3, weight=1)
        actions = FlowFrame(panel)
        actions.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        actions.add(
            ActionButton(
                actions,
                text="Record transfer",
                variant="Primary",
                command=self._open_transfer,
            )
        )
        self.details_button = actions.add(
            ActionButton(
                actions,
                text="View details",
                command=self._open_details,
                state="disabled",
            )
        )
        self.claim_button = actions.add(
            ActionButton(
                actions,
                text="Confirm completion",
                command=self._claim_selected,
                state="disabled",
            )
        )
        actions.add(
            ActionButton(actions, text="Refresh", variant="Quiet", command=self.refresh)
        )
        search = ttk.Frame(panel)
        search.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        search.columnconfigure(0, weight=1)
        ttk.Label(
            search,
            text="Search the last reference digits · includes all dates",
            style="Muted.TLabel",
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))
        self.reference_entry = ttk.Entry(search, textvariable=self.reference_var)
        self.reference_entry.grid(row=1, column=0, sticky="ew")
        self.reference_entry.bind("<Return>", lambda e: self._load_transactions())
        ActionButton(search, text="Search", command=self._load_transactions).grid(
            row=1, column=1, padx=(8, 0)
        )
        ActionButton(search, text="Clear", command=self._clear_search).grid(
            row=1, column=2, padx=(8, 0)
        )
        filters = FlowFrame(panel)
        filters.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        self.type_combo = filters.add(
            ttk.Combobox(
                filters,
                textvariable=self.type_filter,
                values=("Both services", *SERVICES),
                width=14,
                state="readonly",
            )
        )
        self.type_combo.bind(
            "<<ComboboxSelected>>", lambda e: self._load_transactions()
        )
        status = filters.add(
            ttk.Combobox(
                filters,
                textvariable=self.status_filter,
                values=("All statuses", "Unclaimed / Pending", "Claimed / Completed"),
                width=22,
                state="readonly",
            )
        )
        status.bind("<<ComboboxSelected>>", lambda e: self._load_transactions())
        self.account_combo = filters.add(
            ttk.Combobox(
                filters, textvariable=self.account_filter, width=28, state="readonly"
            )
        )
        self.account_combo.bind(
            "<<ComboboxSelected>>", lambda e: self._load_transactions()
        )
        box, self.transactions_table = table(
            panel,
            (
                "type",
                "status",
                "reference",
                "amount",
                "fee",
                "account",
                "transferred",
                "sender",
                "claimed",
            ),
            (
                "Service",
                "Status",
                "Ref. last 5",
                "Amount",
                "Fee",
                "Shop account",
                "Transfer time",
                "Customer account",
                "Completed at",
            ),
            (90, 100, 90, 110, 90, 220, 170, 220, 170),
            empty_text="No transfers recorded. Add a shop account, then record a transfer.",
            height=4,
        )
        box.grid(row=3, column=0, sticky="nsew")
        self.transactions_table.column("account", stretch=True)
        self.transactions_table.column("type", stretch=False)
        self.transactions_table.column("status", stretch=False)
        self.transactions_table.column("fee", anchor="e")
        self.transactions_table.tag_configure("unclaimed", background="#fffbeb")
        self.transactions_table.tag_configure("claimed", background="#ecfdf5")
        self.transactions_table.bind(
            "<<TreeviewSelect>>", lambda e: self._update_selection()
        )
        self.transactions_table.bind("<Double-1>", lambda e: self._open_details())
        self.transactions_table.bind("<Return>", lambda e: self._open_details())

    def _build_accounts(self):
        panel = self.accounts_panel
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(2, weight=1)
        note = ttk.Label(
            panel,
            text="Shared shop accounts for Cash-In and Cash-Out. Use names such as GCash 1, GCash 2, Maya, or BDO, each with its own number.",
            style="Muted.TLabel",
            wraplength=650,
        )
        note.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        panel.bind(
            "<Configure>",
            lambda e: note.configure(wraplength=max(200, e.width - 24)),
            add="+",
        )
        actions = FlowFrame(panel)
        actions.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        actions.add(
            ActionButton(
                actions,
                text="Add shop account",
                variant="Primary",
                command=self._open_account,
            )
        )
        self.edit_account_button = actions.add(
            ActionButton(
                actions,
                text="Edit selected account",
                command=self._edit_account,
                state="disabled",
            )
        )
        box, self.accounts_table = table(
            panel,
            ("name", "number"),
            ("Account name", "Account number"),
            (260, 240),
            empty_text="Add your first shop account above.",
        )
        box.grid(row=2, column=0, sticky="nsew")
        self.accounts_table.bind(
            "<<TreeviewSelect>>",
            lambda e: self.edit_account_button.configure(
                state="normal" if self.accounts_table.selection() else "disabled"
            ),
        )
        self.accounts_table.bind("<Double-1>", lambda e: self._edit_account())

    def _build_totals(self):
        panel = self.totals_panel
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)
        controls = FlowFrame(panel)
        controls.grid(row=0, column=0, sticky="ew", padx=12)
        controls.add(ttk.Label(controls, text="Service"))
        service = controls.add(
            ttk.Combobox(
                controls,
                textvariable=self.fee_service_var,
                values=("Both services", *SERVICES),
                width=16,
                state="readonly",
            )
        )
        service.bind("<<ComboboxSelected>>", lambda e: self._refresh_fee_totals())
        scroll = ScrollFrame(panel)
        scroll.grid(row=1, column=0, sticky="nsew")
        content = scroll.content
        content.columnconfigure(0, weight=1)
        note = ttk.Label(
            content,
            text="Service fees across all shop accounts, using transfer dates. "
            "Weeks start Monday; totals run through today. Search filters do not change these totals.",
            style="Muted.TLabel",
            wraplength=650,
        )
        note.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        content.bind(
            "<Configure>",
            lambda e: note.configure(wraplength=max(200, e.width - 32)),
            add="+",
        )
        cards = MetricGrid(
            content,
            [
                ("Today · Total fees", "day"),
                ("This week · Total fees", "week"),
                ("This month · Total fees", "month"),
                ("This year · Total fees", "year"),
            ],
        )
        cards.grid(row=1, column=0, sticky="ew")
        self.fee_totals = cards.values
        self.fee_breakdowns = {}
        self.fee_dates = {}
        for period, card in zip(self.fee_totals, cards.cards):
            details = self.fee_breakdowns[period] = tk.StringVar()
            date_range = self.fee_dates[period] = tk.StringVar()
            ttk.Label(
                card,
                textvariable=details,
                style="Panel.TLabel",
                foreground=visual.MUTED,
            ).pack(anchor="w", pady=(10, 6))
            ttk.Label(
                card,
                textvariable=date_range,
                style="Panel.TLabel",
                foreground=visual.MUTED,
                font=(visual.FONT, 9),
            ).pack(anchor="w")
        footer = ttk.Frame(panel, padding=(12, 8))
        footer.grid(row=2, column=0, sticky="ew")
        ActionButton(
            footer, text="Refresh fee totals", command=self._refresh_fee_totals
        ).pack(side="left")

    def _on_tab_changed(self, event=None):
        if self.notebook.select() == str(self.totals_panel):
            self._refresh_fee_totals()

    def _refresh_fee_totals(self):
        for period, totals in cash_out.get_fee_totals(
            transaction_type=SERVICES.get(self.fee_service_var.get())
        ).items():
            self.fee_totals[period].configure(
                text="PHP " + cash_out.money_text(totals["total_fee_cents"])
            )
            self.fee_breakdowns[period].set(
                "Cash-Out: PHP "
                + cash_out.money_text(totals["cash_out_fee_cents"])
                + "\nCash-In: PHP "
                + cash_out.money_text(totals["cash_in_fee_cents"])
                + "\nCompleted / Claimed: PHP "
                + cash_out.money_text(totals["claimed_fee_cents"])
                + "\nPending / Unclaimed: PHP "
                + cash_out.money_text(totals["unclaimed_fee_cents"])
                + f"\n{totals['transaction_count']} transfers"
            )
            self.fee_dates[period].set(
                totals["start_date"]
                if totals["start_date"] == totals["end_date"]
                else f"{totals['start_date']} – {totals['end_date']}"
            )

    def _build_rules(self):
        self.rules_panel.columnconfigure(0, weight=1)
        self.rules_panel.rowconfigure(0, weight=1)
        scroll = ScrollFrame(self.rules_panel)
        scroll.grid(row=0, column=0, sticky="nsew")
        panel = scroll.content
        panel.columnconfigure(1, weight=1)
        note = ttk.Label(
            panel,
            text="Shared Cash-In / Cash-Out fees stack: each full block has a fee, then any remaining amount adds its own fee. Saved transfers keep their recorded fee.",
            wraplength=650,
            style="Muted.TLabel",
        )
        note.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))
        panel.bind(
            "<Configure>",
            lambda e: note.configure(wraplength=max(200, e.width - 32)),
            add="+",
        )
        self.rule_vars = {}
        for row, (field, label) in enumerate(
            [
                ("block_amount_cents", "Full block amount (PHP)"),
                ("block_fee_cents", "Fee per full block (PHP)"),
                ("split_amount_cents", "Remaining amount split (PHP)"),
                ("lower_fee_cents", "Fee below the split (PHP)"),
                ("upper_fee_cents", "Fee at or above the split (PHP)"),
            ],
            start=1,
        ):
            variable = self.rule_vars[field] = tk.StringVar()
            ttk.Label(panel, text=label).grid(
                row=row, column=0, sticky="w", padx=(0, 16), pady=6
            )
            ttk.Entry(panel, textvariable=variable, width=14).grid(
                row=row, column=1, sticky="w", pady=6
            )
        self.rule_preview = tk.StringVar()
        preview = ttk.Label(
            panel,
            textvariable=self.rule_preview,
            wraplength=650,
            style="Muted.TLabel",
            justify="left",
        )
        preview.grid(row=6, column=0, columnspan=2, sticky="w", pady=(16, 12))
        panel.bind(
            "<Configure>",
            lambda e: preview.configure(wraplength=max(200, e.width - 32)),
            add="+",
        )
        footer = ttk.Frame(self.rules_panel, padding=(12, 8))
        footer.grid(row=1, column=0, sticky="ew")
        self.rule_feedback = tk.StringVar()
        ttk.Label(
            footer,
            textvariable=self.rule_feedback,
            style="Muted.TLabel",
            wraplength=620,
        ).pack(anchor="w", pady=(0, 8))
        ActionButton(
            footer, text="Save fee rules", variant="Primary", command=self._save_rules
        ).pack(anchor="w")
        self._loading_rules = False
        for variable in self.rule_vars.values():
            variable.trace_add("write", lambda *args: self._preview_rules())

    def _rule_arguments(self):
        return [
            self.rule_vars[field].get()
            for field in (
                "block_amount_cents",
                "split_amount_cents",
                "block_fee_cents",
                "lower_fee_cents",
                "upper_fee_cents",
            )
        ]

    def _preview_rules(self):
        if self._loading_rules:
            return
        self.rule_feedback.set("")
        try:
            rules = cash_out.validate_fee_rules(*self._rule_arguments())
            examples = "   ·   ".join(
                f"PHP {amount:,} → {cash_out.money_text(cash_out.calculate_fee(amount, rules))} fee"
                for amount in (499, 750, 1000, 1500, 2000)
            )
            self.rule_preview.set(
                "No additional remainder fee applies to exact full blocks.\n\n"
                + examples
            )
        except ValueError as exc:
            self.rule_preview.set(str(exc))

    def _save_rules(self):
        try:
            cash_out.save_fee_rules(*self._rule_arguments())
        except ValueError as exc:
            self.rule_preview.set(str(exc))
            self.rule_feedback.set(str(exc))
            return
        self.rule_feedback.set(
            "Saved. Future transfers will use these fee suggestions."
        )
        self.status_var.set(
            "Fee rules saved. New transfers will use these suggestions."
        )

    def refresh(self):
        selected_account = self.accounts_table.selection()
        filter_id = self._account_labels.get(self.account_filter.get())
        self._accounts = {
            account["id"]: account for account in cash_out.list_accounts()
        }
        self._account_labels = {
            f"{account['name']} · {account['account_number']}": account["id"]
            for account in self._accounts.values()
        }
        self.account_combo.configure(
            values=("All shop accounts", *self._account_labels)
        )
        self.account_filter.set(
            next(
                (
                    label
                    for label, account_id in self._account_labels.items()
                    if account_id == filter_id
                ),
                "All shop accounts",
            )
        )
        self.accounts_table.delete(*self.accounts_table.get_children())
        for account in self._accounts.values():
            self.accounts_table.insert(
                "",
                "end",
                iid=str(account["id"]),
                values=(account["name"], account["account_number"]),
            )
        if selected_account and self.accounts_table.exists(selected_account[0]):
            self.accounts_table.selection_set(selected_account)
        self.edit_account_button.configure(
            state="normal" if self.accounts_table.selection() else "disabled"
        )
        self._loading_rules = True
        for field, value in cash_out.get_fee_rules().items():
            if field in self.rule_vars:
                self.rule_vars[field].set(cash_out.money_text(value))
        self._loading_rules = False
        self._preview_rules()
        self._load_transactions()
        self._refresh_fee_totals()

    def _clear_search(self):
        self.reference_var.set("")
        self.status_filter.set("All statuses")
        self.account_filter.set("All shop accounts")
        self.type_filter.set("Both services")
        self._load_transactions()

    def _load_transactions(self):
        selected = self.transactions_table.selection()
        try:
            rows = cash_out.list_transactions(
                self.reference_var.get(),
                {
                    "All statuses": "all",
                    "Unclaimed / Pending": "unclaimed",
                    "Claimed / Completed": "claimed",
                    "Unclaimed": "unclaimed",
                    "Claimed": "claimed",
                }[self.status_filter.get()],
                self._account_labels.get(self.account_filter.get()),
                transaction_type=SERVICES.get(self.type_filter.get()),
            )
        except ValueError as exc:
            self.transactions_table.delete(*self.transactions_table.get_children())
            self._transactions = {}
            self.transactions_table.empty_text = str(exc)
            self.transactions_table._refresh_empty()
            self.status_var.set(str(exc))
            self._update_selection()
            return
        self._transactions = {row["id"]: row for row in rows}
        self.transactions_table.delete(*self.transactions_table.get_children())
        self.transactions_table.empty_text = (
            "No matching transfer found."
            if self.reference_var.get()
            or self.status_filter.get() != "All statuses"
            or self.account_filter.get() != "All shop accounts"
            or self.type_filter.get() != "Both services"
            else "No transfers recorded. Add a shop account, then record a transfer."
        )
        self.transactions_table._refresh_empty()
        for row in rows:
            self.transactions_table.insert(
                "",
                "end",
                iid=str(row["id"]),
                values=(
                    TYPE_LABELS[row["transaction_type"]],
                    status_text(row),
                    row["reference_last5"],
                    cash_out.money_text(row["amount_cents"]),
                    cash_out.money_text(row["fee_cents"]),
                    f"{row['receiving_account_name']} · {row['receiving_account_number']}",
                    row["transferred_at"],
                    row["sender_account"],
                    row["claimed_at"] or "—",
                ),
                tags=(row["status"],),
            )
        if selected and self.transactions_table.exists(selected[0]):
            self.transactions_table.selection_set(selected)
        self._update_selection()
        self.status_var.set(
            f"{len(rows)} transfers found · Service fees are separate from product sales."
        )

    def _selected_transaction(self):
        selected = self.transactions_table.selection()
        return self._transactions.get(int(selected[0])) if selected else None

    def _update_selection(self):
        row = self._selected_transaction()
        self.details_button.configure(state="normal" if row else "disabled")
        self.claim_button.configure(
            text=completion_action(row) if row else "Confirm completion",
            state="normal" if row and row["status"] == "unclaimed" else "disabled",
        )

    def _dialog(self, title, width, height):
        modal = tk.Toplevel(self)
        modal.title(title)
        modal.transient(self.winfo_toplevel())
        center_dialog(modal, width, height)
        modal.grab_set()
        return modal

    def _edit_account(self):
        selected = self.accounts_table.selection()
        if selected:
            self._open_account(self._accounts[int(selected[0])])

    def _open_account(self, account=None):
        modal = self._dialog("Shop account", 520, 360)
        body = ttk.Frame(modal, padding=24)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        page_header(
            body,
            "Edit account" if account else "Add account",
            "Choose a name and enter the shop account number.",
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        self.account_vars = {
            "name": tk.StringVar(value=account["name"] if account else ""),
            "number": tk.StringVar(value=account["account_number"] if account else ""),
        }
        for row, (key, label) in enumerate(
            [("name", "Account name"), ("number", "Account number")], start=1
        ):
            ttk.Label(body, text=label).grid(
                row=row, column=0, sticky="w", padx=(0, 16), pady=6
            )
            entry = ttk.Entry(body, textvariable=self.account_vars[key])
            entry.grid(row=row, column=1, sticky="ew", pady=6)
            if key == "name":
                entry.focus_set()
        error = tk.StringVar()
        ttk.Label(body, textvariable=error, foreground="#be123c", wraplength=460).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=8
        )
        buttons = ttk.Frame(body)
        buttons.grid(row=4, column=0, columnspan=2, sticky="e", pady=(8, 0))

        def save():
            try:
                cash_out.save_account(
                    self.account_vars["name"].get(),
                    self.account_vars["number"].get(),
                    account["id"] if account else None,
                )
            except ValueError as exc:
                error.set(str(exc))
                return
            self.refresh()
            self.status_var.set("Shop account saved.")
            modal.destroy()

        ActionButton(buttons, text="Cancel", command=modal.destroy).pack(
            side="left", padx=(0, 8)
        )
        ActionButton(
            buttons, text="Save account", variant="Primary", command=save
        ).pack(side="left")
        modal.bind("<Return>", lambda e: save())

    def _open_transfer(self, transaction_type="cash_out"):
        self.refresh()
        if not self._accounts:
            self.notebook.select(self.accounts_panel)
            self.status_var.set("Add a shop account before recording a transfer.")
            return
        modal = self._dialog("Record transfer", 660, 680)
        modal.columnconfigure(0, weight=1)
        modal.rowconfigure(1, weight=1)
        page_header(
            modal,
            "Record transfer",
            "Choose Cash-In or Cash-Out and enter its transfer details.",
        ).grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 8))
        scroll = ScrollFrame(modal)
        scroll.grid(row=1, column=0, sticky="nsew", padx=4)
        body = scroll.content
        body.columnconfigure(1, weight=1)
        now = datetime.now()
        self.transfer_vars = {
            "type": tk.StringVar(value=TYPE_LABELS[transaction_type]),
            "date": tk.StringVar(value=now.strftime("%Y-%m-%d")),
            "time": tk.StringVar(value=now.strftime("%H:%M:%S")),
            "account": tk.StringVar(
                value=next(iter(self._account_labels))
                if len(self._accounts) == 1
                else ""
            ),
            "sender": tk.StringVar(),
            "amount": tk.StringVar(),
            "fee": tk.StringVar(),
            "reference": tk.StringVar(),
        }
        fields = self.transfer_vars
        self.transfer_labels = {}
        for row, (key, label) in enumerate(
            [
                ("type", "Service"),
                ("date", "Transfer date (YYYY-MM-DD)"),
                ("time", "Transfer time (HH:MM)"),
                ("account", "Receiving account"),
                ("sender", "Sending account"),
                ("amount", "Cash-out amount (PHP)"),
                ("fee", "Service fee (PHP)"),
                ("reference", "Reference · last 5 digits"),
            ]
        ):
            self.transfer_labels[key] = ttk.Label(body, text=label)
            self.transfer_labels[key].grid(
                row=row, column=0, sticky="w", padx=(0, 12), pady=6
            )
            if key == "type":
                entry = ttk.Combobox(
                    body,
                    textvariable=fields[key],
                    values=tuple(SERVICES),
                    state="readonly",
                    width=18,
                )
            elif key == "account":
                entry = ttk.Combobox(
                    body,
                    textvariable=fields[key],
                    values=tuple(self._account_labels),
                    state="readonly",
                    width=18,
                )
            else:
                entry = ttk.Entry(body, textvariable=fields[key], width=18)
            entry.grid(row=row, column=1, sticky="ew", pady=6)
            if key == "sender":
                entry.focus_set()

        def update_roles(*args):
            service = SERVICES[fields["type"].get()]
            shop_role, customer_role = account_roles(service)
            self.transfer_labels["account"].configure(text=shop_role)
            self.transfer_labels["sender"].configure(text=customer_role)
            self.transfer_labels["amount"].configure(
                text=fields["type"].get() + " amount (PHP)"
            )

        fields["type"].trace_add("write", update_roles)
        update_roles()
        hint = tk.StringVar(
            value="Enter the amount to suggest a fee. You can type a different fee."
        )
        hint_label = ttk.Label(
            body, textvariable=hint, style="Muted.TLabel", wraplength=560
        )
        hint_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=(8, 8))
        context = {
            "updating": False,
            "custom": False,
            "suggested": None,
            "rules": cash_out.get_fee_rules(),
        }

        def amount_changed(*args):
            try:
                context["suggested"] = cash_out.calculate_fee(
                    fields["amount"].get(), context["rules"]
                )
            except ValueError:
                context["suggested"] = None
            if context["suggested"] is not None:
                hint.set(
                    f"Suggested fee: PHP {cash_out.money_text(context['suggested'])}"
                    + (
                        " · Custom fee kept"
                        if context["custom"]
                        else " · Edit the fee if needed"
                    )
                )
                if not context["custom"]:
                    context["updating"] = True
                    fields["fee"].set(cash_out.money_text(context["suggested"]))
                    context["updating"] = False
            else:
                hint.set("Enter a valid amount to suggest a fee.")
                if not context["custom"]:
                    context["updating"] = True
                    fields["fee"].set("")
                    context["updating"] = False

        def fee_changed(*args):
            if context["updating"]:
                return
            # Typing in the field opts out of automation until explicitly reset.
            # Do not reformat the text while someone is entering a custom fee.
            context["custom"] = True
            amount_changed()

        def reset_fee():
            context["custom"] = False
            amount_changed()

        fields["amount"].trace_add("write", amount_changed)
        fields["fee"].trace_add("write", fee_changed)
        ActionButton(body, text="Use suggested fee", command=reset_fee).grid(
            row=9, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )
        footer = ttk.Frame(modal, padding=(20, 12))
        footer.grid(row=2, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)
        error = tk.StringVar()
        ttk.Label(
            footer, textvariable=error, foreground="#be123c", wraplength=590
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        def save():
            try:
                account_id = self._account_labels.get(fields["account"].get())
                if account_id is None:
                    raise ValueError("Choose a shop account.")
                payload = dict(
                    transferred_at=f"{fields['date'].get()} {fields['time'].get()}",
                    receiving_account_id=account_id,
                    sender_account=fields["sender"].get(),
                    amount=fields["amount"].get(),
                    reference_last5=fields["reference"].get(),
                    fee=fields["fee"].get(),
                    transaction_type=SERVICES[fields["type"].get()],
                )
                try:
                    transaction_id = cash_out.create_transaction(**payload)
                except cash_out.DuplicateTransactionError as duplicate:
                    matches = "\n".join(
                        f"#{row['id']} · {TYPE_LABELS[row['transaction_type']]} · {row['transferred_at']} · {row['sender_account']} · {status_text(row).upper()}"
                        + (f" at {row['claimed_at']}" if row["claimed_at"] else "")
                        for row in duplicate.matches[:5]
                    )
                    if not messagebox.askyesno(
                        "Possible duplicate " + fields["type"].get().lower(),
                        "The service, shop account, date, amount, and reference ending match existing records:\n\n"
                        + matches
                        + "\n\nReview these entries before saving. Save another record anyway?",
                        parent=modal,
                        default="no",
                        icon="warning",
                    ):
                        error.set("Not saved. Review the existing matching records.")
                        return
                    transaction_id = cash_out.create_transaction(
                        **payload, allow_duplicate=True
                    )
            except ValueError as exc:
                error.set(str(exc))
                return
            self._clear_search()
            self._refresh_fee_totals()
            self.transactions_table.selection_set(str(transaction_id))
            self.transactions_table.see(str(transaction_id))
            self._update_selection()
            self.notebook.select(self.transactions_panel)
            self.status_var.set(
                f"{fields['type'].get()} saved as {'pending' if payload['transaction_type'] == 'cash_in' else 'unclaimed'}, including its service fee."
            )
            modal.destroy()

        ActionButton(footer, text="Cancel", command=modal.destroy).grid(
            row=1, column=0, sticky="e", padx=(0, 8)
        )
        ActionButton(
            footer, text="Save transfer", variant="Primary", command=save
        ).grid(row=1, column=1)
        modal.bind("<Control-Return>", lambda e: save())

    def _claim_selected(self):
        row = self._selected_transaction()
        if row:
            self._claim(row["id"], self.winfo_toplevel())

    def _claim(self, transaction_id, parent):
        row = cash_out.get_transaction(transaction_id)
        if row is None:
            self.status_var.set("This transfer no longer exists.")
            self._load_transactions()
            return False
        service = TYPE_LABELS[row["transaction_type"]]
        cash_in = row["transaction_type"] == "cash_in"
        if row["status"] == "claimed":
            messagebox.showinfo(
                "Already completed" if cash_in else "Already claimed",
                f"This {service} was already completed at {row['claimed_at']}.",
                parent=parent,
            )
            self._load_transactions()
            return False
        shop_role, customer_role = account_roles(row["transaction_type"])
        question = (
            "Has PHP "
            + cash_out.money_text(row["amount_cents"])
            + (
                " been sent to the customer's account?"
                if cash_in
                else " cash been handed to the customer?"
            )
        )
        if not messagebox.askyesno(
            completion_action(row),
            question
            + f"\n\n{shop_role}: {row['receiving_account_name']} · {row['receiving_account_number']}\n{customer_role}: {row['sender_account']}\nReference ending: {row['reference_last5']}\nTransfer time: {row['transferred_at']}\nService fee: PHP {cash_out.money_text(row['fee_cents'])}\n\nConfirm to mark this {service} as {'completed' if cash_in else 'claimed'}.",
            parent=parent,
            default="no",
        ):
            return False
        try:
            cash_out.complete_transaction(transaction_id)
        except ValueError as exc:
            messagebox.showerror("Transfer not updated", str(exc), parent=parent)
            self._load_transactions()
            return False
        self._load_transactions()
        self._refresh_fee_totals()
        self.status_var.set(
            f"{service} #{transaction_id} marked as {'completed' if cash_in else 'claimed'}."
        )
        return True

    def _open_details(self):
        selected = self._selected_transaction()
        if not selected:
            return
        row = cash_out.get_transaction(selected["id"])
        if row is None:
            self._load_transactions()
            return
        service = TYPE_LABELS[row["transaction_type"]]
        shop_role, customer_role = account_roles(row["transaction_type"])
        cash_in = row["transaction_type"] == "cash_in"
        modal = self._dialog(service + " details", 660, 580)
        modal.columnconfigure(0, weight=1)
        modal.rowconfigure(1, weight=1)
        page_header(modal, f"{service} #{row['id']}", status_text(row)).grid(
            row=0, column=0, sticky="ew", padx=20, pady=16
        )
        scroll = ScrollFrame(modal)
        scroll.grid(row=1, column=0, sticky="nsew")
        body = scroll.content
        body.columnconfigure(1, weight=1)
        for index, (label, value) in enumerate(
            [
                ("Service", service),
                ("Transfer time", row["transferred_at"]),
                (
                    shop_role,
                    f"{row['receiving_account_name']}\n{row['receiving_account_number']}",
                ),
                (customer_role, row["sender_account"]),
                (
                    service + " amount",
                    "PHP " + cash_out.money_text(row["amount_cents"]),
                ),
                ("Service fee", "PHP " + cash_out.money_text(row["fee_cents"])),
                (
                    "Suggested at entry",
                    "PHP " + cash_out.money_text(row["suggested_fee_cents"]),
                ),
                ("Reference ending", row["reference_last5"]),
                (
                    "Completed at" if cash_in else "Claimed at",
                    row["claimed_at"]
                    or ("Not completed" if cash_in else "Not claimed"),
                ),
            ]
        ):
            ttk.Label(body, text=label, style="Muted.TLabel").grid(
                row=index, column=0, sticky="nw", padx=(0, 16), pady=8
            )
            ttk.Label(body, text=value, wraplength=380, justify="left").grid(
                row=index, column=1, sticky="nw", pady=8
            )
        actions = ttk.Frame(modal, padding=20)
        actions.grid(row=2, column=0, sticky="ew")
        ActionButton(actions, text="Close", command=modal.destroy).pack(side="right")
        if row["status"] == "unclaimed":

            def claim():
                if self._claim(row["id"], modal):
                    modal.destroy()

            ActionButton(
                actions, text=completion_action(row), variant="Primary", command=claim
            ).pack(side="right", padx=(0, 8))
