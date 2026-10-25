"""Shared cash-in/out ledger, stacking fees, and completion protection.

Legacy table/column names remain compatible with existing cash-out records.
The saved shop account sends funds for cash-in and receives funds for cash-out;
sender_account holds the customer's opposite account in each case.
"""

import re
import sqlite3
from contextlib import closing
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from db import database

MAX_CENTS = 9_000_000_000_000
TRANSACTION_TYPES = ("cash_out", "cash_in")
RULE_FIELDS = (
    "block_amount_cents",
    "split_amount_cents",
    "block_fee_cents",
    "lower_fee_cents",
    "upper_fee_cents",
)


class DuplicateTransactionError(ValueError):
    def __init__(self, matches):
        self.matches = matches
        super().__init__(
            "A transfer of the same type, shop account, date, amount, and reference ending already exists."
        )


def _validate_type(transaction_type, *, allow_all=False):
    if allow_all and transaction_type is None:
        return
    if transaction_type not in TRANSACTION_TYPES:
        raise ValueError("Choose Cash-In or Cash-Out.")


def money_to_cents(value, label="Amount", *, allow_zero=False):
    try:
        number = Decimal(str(value).strip().replace(",", ""))
        if not number.is_finite():
            raise InvalidOperation
        if number > Decimal(MAX_CENTS) / 100:
            raise ValueError(f"{label} is too large.")
        if number != number.quantize(Decimal("0.01")):
            raise ValueError(f"{label} must have at most two decimal places.")
        cents = number * 100
        if cents < 0 or (not allow_zero and cents == 0):
            raise ValueError(
                f"{label} must be {'zero or more' if allow_zero else 'greater than zero'}."
            )
        return int(cents)
    except (InvalidOperation, TypeError) as exc:
        raise ValueError(f"Enter a valid {label.lower()}.") from exc


def money_text(cents):
    return f"{Decimal(cents) / 100:,.2f}"


def _timestamp(value):
    for pattern in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(str(value).strip(), pattern).isoformat(
                " ", timespec="seconds"
            )
        except ValueError:
            continue
    raise ValueError("Enter a valid transfer date and time: YYYY-MM-DD HH:MM.")


def list_accounts():
    with closing(database.get_connection()) as conn:
        return [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM cash_out_accounts ORDER BY name COLLATE NOCASE, id"
            )
        ]


def save_account(name, account_number, account_id=None):
    name = str(name if name is not None else "").strip()
    number = str(account_number if account_number is not None else "").strip()
    if not name or not number:
        raise ValueError("Enter an account name and account number.")
    try:
        with closing(database.get_connection()) as conn, conn:
            if account_id is None:
                return conn.execute(
                    "INSERT INTO cash_out_accounts (name, account_number) VALUES (?, ?)",
                    (name, number),
                ).lastrowid
            cursor = conn.execute(
                "UPDATE cash_out_accounts SET name = ?, account_number = ? WHERE id = ?",
                (name, number, account_id),
            )
            if cursor.rowcount != 1:
                raise ValueError("The shop account no longer exists.")
            return account_id
    except sqlite3.IntegrityError as exc:
        raise ValueError(
            "That account name is already in use. Choose another name."
        ) from exc


def _rules(conn):
    return dict(
        conn.execute("SELECT * FROM cash_out_fee_rules WHERE id = 1").fetchone()
    )


def get_fee_rules():
    with closing(database.get_connection()) as conn:
        return _rules(conn)


def validate_fee_rules(block_amount, split_amount, block_fee, lower_fee, upper_fee):
    values = (
        money_to_cents(block_amount, "Block amount"),
        money_to_cents(split_amount, "Remaining amount split"),
        money_to_cents(block_fee, "Full-block fee", allow_zero=True),
        money_to_cents(lower_fee, "Lower remaining fee", allow_zero=True),
        money_to_cents(upper_fee, "Upper remaining fee", allow_zero=True),
    )
    if values[1] >= values[0]:
        raise ValueError(
            "The remaining amount split must be below the full block amount."
        )
    return dict(zip(RULE_FIELDS, values))


def save_fee_rules(block_amount, split_amount, block_fee, lower_fee, upper_fee):
    rules = validate_fee_rules(
        block_amount, split_amount, block_fee, lower_fee, upper_fee
    )
    with closing(database.get_connection()) as conn, conn:
        conn.execute(
            "UPDATE cash_out_fee_rules SET block_amount_cents=?, split_amount_cents=?, "
            "block_fee_cents=?, lower_fee_cents=?, upper_fee_cents=? WHERE id=1",
            tuple(rules[field] for field in RULE_FIELDS),
        )


def _calculate_fee(amount_cents, rules):
    blocks, remainder = divmod(amount_cents, rules["block_amount_cents"])
    fee = blocks * rules["block_fee_cents"]
    if remainder:
        fee += (
            rules["lower_fee_cents"]
            if remainder < rules["split_amount_cents"]
            else rules["upper_fee_cents"]
        )
    if fee > MAX_CENTS:
        raise ValueError("The calculated fee is too large. Review the fee rules.")
    return fee


def calculate_fee(amount, rules=None):
    """Return the suggested fee in centavos, using complete blocks plus a remainder."""
    return _calculate_fee(money_to_cents(amount), rules or get_fee_rules())


def _duplicates(conn, account_id, timestamp, amount_cents, reference, transaction_type):
    return [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM cash_out_transactions WHERE receiving_account_id=? AND transaction_type=? "
            "AND transferred_at >= ? AND transferred_at < ? "
            "AND amount_cents=? AND reference_last5=? ORDER BY id DESC",
            (
                account_id,
                transaction_type,
                timestamp[:10] + " 00:00:00",
                timestamp[:10] + " 24:00:00",
                amount_cents,
                reference,
            ),
        )
    ]


def create_transaction(
    *,
    transferred_at,
    receiving_account_id,
    sender_account,
    amount,
    reference_last5,
    fee=None,
    allow_duplicate=False,
    transaction_type="cash_out",
):
    _validate_type(transaction_type)
    timestamp = _timestamp(transferred_at)
    sender = str(sender_account if sender_account is not None else "").strip()
    reference = str(reference_last5).strip()
    if not sender:
        raise ValueError("Enter the customer's account details shown on the transfer.")
    if re.fullmatch(r"[0-9]{5}", reference) is None:
        raise ValueError(
            "Enter exactly the last five reference digits, including leading zeros."
        )
    amount_cents = money_to_cents(amount)
    override = (
        money_to_cents(fee, "Service fee", allow_zero=True) if fee is not None else None
    )
    with closing(database.get_connection()) as conn, conn:
        # Check and insert in one write transaction, so concurrent duplicate entries also warn.
        conn.execute("BEGIN IMMEDIATE")
        account = conn.execute(
            "SELECT * FROM cash_out_accounts WHERE id=?", (receiving_account_id,)
        ).fetchone()
        if account is None:
            raise ValueError("Select an existing shop account.")
        matches = _duplicates(
            conn,
            receiving_account_id,
            timestamp,
            amount_cents,
            reference,
            transaction_type,
        )
        if matches and not allow_duplicate:
            raise DuplicateTransactionError(matches)
        suggested = _calculate_fee(amount_cents, _rules(conn))
        cursor = conn.execute(
            "INSERT INTO cash_out_transactions "
            "(transferred_at, receiving_account_id, receiving_account_name, "
            "receiving_account_number, sender_account, amount_cents, fee_cents, "
            "suggested_fee_cents, reference_last5, created_at, transaction_type) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                timestamp,
                receiving_account_id,
                account["name"],
                account["account_number"],
                sender,
                amount_cents,
                suggested if override is None else override,
                suggested,
                reference,
                datetime.now().isoformat(" ", timespec="seconds"),
                transaction_type,
            ),
        )
        return cursor.lastrowid


def get_transaction(transaction_id):
    with closing(database.get_connection()) as conn:
        row = conn.execute(
            "SELECT * FROM cash_out_transactions WHERE id=?", (transaction_id,)
        ).fetchone()
        return dict(row) if row is not None else None


def list_transactions(
    reference="", status="all", account_id=None, transaction_type=None
):
    _validate_type(transaction_type, allow_all=True)
    reference = str(reference).strip()
    if reference and re.fullmatch(r"[0-9]{1,5}", reference) is None:
        raise ValueError("Search using one to five reference digits.")
    if status not in ("all", "unclaimed", "claimed"):
        raise ValueError("Choose a valid claim status.")
    clauses, params = [], []
    if reference:
        clauses.append("reference_last5 LIKE ?")
        params.append(f"%{reference}%")
    if status != "all":
        clauses.append("status = ?")
        params.append(status)
    if account_id is not None:
        clauses.append("receiving_account_id = ?")
        params.append(account_id)
    if transaction_type is not None:
        clauses.append("transaction_type = ?")
        params.append(transaction_type)
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    with closing(database.get_connection()) as conn:
        return [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM cash_out_transactions"
                + where
                + " ORDER BY transferred_at DESC, id DESC",
                params,
            )
        ]


def get_fee_totals(today=None, transaction_type=None):
    """Calendar-to-date totals using transfer dates and the fees actually saved."""
    _validate_type(transaction_type, allow_all=True)
    today = today if today is not None else datetime.now().date()
    starts = {
        "day": today,
        "week": today - timedelta(days=today.weekday()),
        "month": today.replace(day=1),
        "year": today.replace(month=1, day=1),
    }
    end = (today + timedelta(days=1)).isoformat() + " 00:00:00"
    totals = {}
    with closing(database.get_connection()) as conn, conn:
        # Keep all four periods consistent when another instance records a handover.
        conn.execute("BEGIN")
        for period, start in starts.items():
            query = (
                "SELECT status, transaction_type, COUNT(*) AS count, SUM(fee_cents) AS fees "
                "FROM cash_out_transactions "
                "WHERE transferred_at >= ? AND transferred_at < ?"
            )
            params = [start.isoformat() + " 00:00:00", end]
            if transaction_type is not None:
                query += " AND transaction_type=?"
                params.append(transaction_type)
            rows = conn.execute(
                query + " GROUP BY status, transaction_type", params
            ).fetchall()
            fees = {"claimed": 0, "unclaimed": 0}
            service_fees = {service: 0 for service in TRANSACTION_TYPES}
            for row in rows:
                fees[row["status"]] += row["fees"]
                service_fees[row["transaction_type"]] += row["fees"]
            totals[period] = {
                "start_date": start.isoformat(),
                "end_date": today.isoformat(),
                "total_fee_cents": sum(fees.values()),
                "claimed_fee_cents": fees.get("claimed", 0),
                "unclaimed_fee_cents": fees.get("unclaimed", 0),
                "transaction_count": sum(row["count"] for row in rows),
                "cash_out_fee_cents": service_fees["cash_out"],
                "cash_in_fee_cents": service_fees["cash_in"],
            }
    return totals


def complete_transaction(transaction_id):
    with closing(database.get_connection()) as conn, conn:
        cursor = conn.execute(
            "UPDATE cash_out_transactions SET status='claimed', claimed_at=? "
            "WHERE id=? AND status='unclaimed'",
            (datetime.now().isoformat(" ", timespec="seconds"), transaction_id),
        )
        if cursor.rowcount != 1:
            row = conn.execute(
                "SELECT claimed_at, transaction_type FROM cash_out_transactions WHERE id=?",
                (transaction_id,),
            ).fetchone()
            if row is None:
                raise ValueError("This transfer no longer exists.")
            state = "completed" if row["transaction_type"] == "cash_in" else "claimed"
            raise ValueError(
                f"This transfer was already {state} at {row['claimed_at']}."
            )


def claim_transaction(transaction_id):
    """Compatibility name for completing an existing cash-out or cash-in record."""
    complete_transaction(transaction_id)
