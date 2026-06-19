from db.database import get_connection
from datetime import datetime



def add_debt(person_name: str, amount: float, description: str = "", sale_linked: bool = True) -> bool:
    """Add a new debt entry."""
    if not person_name or amount <= 0:
        return False
    
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO debt_tracker (person_name, amount, is_paid, description, sale_linked)
            VALUES (?, ?, 0, ?, ?)
            """,
            (person_name, amount, description, 1 if sale_linked else 0),
        )
        conn.commit()
    return True


def get_all_debts() -> list[dict]:
    """Get all debt entries."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, person_name, amount, is_paid, created_at, paid_at, description
            FROM debt_tracker
            ORDER BY person_name ASC, is_paid ASC, created_at DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_customers_with_totals() -> list[dict]:
    """Get customers with their total pending debt."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                c.name as person_name,
                COALESCE(SUM(CASE WHEN d.is_paid = 0 THEN d.amount ELSE 0 END), 0) as total_debt,
                COALESCE(SUM(CASE WHEN d.is_paid = 0 THEN 1 ELSE 0 END), 0) as pending_count,
                COALESCE(COUNT(d.id), 0) as total_count
            FROM customers c
            LEFT JOIN debt_tracker d ON d.person_name = c.name
            GROUP BY c.name
            ORDER BY total_debt DESC, c.name ASC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def add_customer(name: str) -> bool:
    """Create a new customer account."""
    if not name:
        return False
    with get_connection() as conn:
        try:
            conn.execute("INSERT INTO customers (name) VALUES (?)", (name,))
            conn.commit()
            return True
        except Exception:
            return False


def get_customers() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, name, created_at FROM customers ORDER BY name COLLATE NOCASE").fetchall()
    return [dict(row) for row in rows]


def delete_customer(name: str) -> bool:
    if not name:
        return False

    with get_connection() as conn:
        # Keep debt/customer data consistent by removing both account and its debt rows.
        conn.execute("DELETE FROM debt_tracker WHERE person_name = ?", (name,))
        conn.execute("DELETE FROM customers WHERE name = ?", (name,))
        deleted_rows = conn.total_changes
        conn.commit()
    return deleted_rows > 0


def get_customer_debts(person_name: str) -> list[dict]:
    """Get all debts for a specific customer."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, person_name, amount, is_paid, created_at, paid_at, description
            FROM debt_tracker
            WHERE person_name = ?
            ORDER BY is_paid ASC, created_at DESC
            """,
            (person_name,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_pending_debts() -> list[dict]:
    """Get only unpaid debts."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, person_name, amount, is_paid, created_at, paid_at, description
            FROM debt_tracker
            WHERE is_paid = 0
            ORDER BY person_name ASC, created_at DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def update_debt(debt_id: int, amount: float, description: str = "") -> bool:
    """Update a debt entry."""
    if amount <= 0:
        return False
    
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE debt_tracker
            SET amount = ?, description = ?
            WHERE id = ?
            """,
            (amount, description, debt_id),
        )
        conn.commit()
    return True


def mark_paid(debt_id: int) -> bool:
    """Mark a debt as paid."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT amount, sale_linked FROM debt_tracker WHERE id = ? AND is_paid = 0",
            (debt_id,),
        ).fetchone()
        if not row:
            return False
        amount = float(row["amount"])
        sale_linked = int(row["sale_linked"] or 0) == 1

        conn.execute(
            """
            UPDATE debt_tracker
            SET is_paid = 1, paid_at = datetime('now')
            WHERE id = ?
            """,
            (debt_id,),
        )
        if sale_linked:
            # Record a sale only when the debt came from a sale
            conn.execute(
                "INSERT INTO sales (total, date) VALUES (?, ?)",
                (amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
        conn.commit()
    return True



def mark_unpaid(debt_id: int) -> bool:
    """Mark a debt as unpaid."""
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE debt_tracker
            SET is_paid = 0, paid_at = NULL
            WHERE id = ?
            """,
            (debt_id,),
        )
        conn.commit()
    return True


def delete_debt(debt_id: int) -> bool:
    """Delete a debt entry."""
    with get_connection() as conn:
        conn.execute("DELETE FROM debt_tracker WHERE id = ?", (debt_id,))
        conn.commit()
    return True


def get_total_debt() -> float:
    """Get total pending debt across all customers."""
    with get_connection() as conn:
        result = conn.execute(
            "SELECT SUM(amount) as total FROM debt_tracker WHERE is_paid = 0"
        ).fetchone()
    return result["total"] if result["total"] else 0.0


def get_customer_total_debt(person_name: str) -> float:
    """Get total pending debt for a specific customer."""
    with get_connection() as conn:
        result = conn.execute(
            "SELECT SUM(amount) as total FROM debt_tracker WHERE person_name = ? AND is_paid = 0",
            (person_name,),
        ).fetchone()
    return result["total"] if result["total"] else 0.0


def apply_payment_to_customer(person_name: str, payment_amount: float) -> dict:
    """Apply a payment amount across a customer's unpaid debts (oldest first).

    Returns a summary dict: { 'applied': float, 'remaining': float, 'details': [ {debt_id, before, after, paid} ] }
    """
    if not person_name or payment_amount <= 0:
        return {"applied": 0.0, "remaining": payment_amount, "details": []}

    remaining = float(payment_amount)
    details: list[dict] = []
    sale_total = 0.0
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, amount, sale_linked
            FROM debt_tracker
            WHERE person_name = ? AND is_paid = 0
            ORDER BY created_at ASC
            """,
            (person_name,),
        ).fetchall()

        for row in rows:
            debt_id = row["id"]
            debt_amount = float(row["amount"])
            sale_linked = int(row["sale_linked"] or 0) == 1
            if remaining <= 0:
                break

            if remaining >= debt_amount:
                # pay off this debt
                conn.execute(
                    """
                    UPDATE debt_tracker
                    SET is_paid = 1, paid_at = datetime('now'), amount = 0
                    WHERE id = ?
                    """,
                    (debt_id,),
                )
                conn.commit()
                details.append({"debt_id": debt_id, "before": debt_amount, "after": 0.0, "paid": True})
                if sale_linked:
                    sale_total += debt_amount
                remaining -= debt_amount
            else:
                # partially pay this debt, reduce amount
                new_amount = round(debt_amount - remaining, 2)
                conn.execute(
                    """
                    UPDATE debt_tracker
                    SET amount = ?
                    WHERE id = ?
                    """,
                    (new_amount, debt_id),
                )
                conn.commit()
                details.append({"debt_id": debt_id, "before": debt_amount, "after": new_amount, "paid": False})
                if sale_linked:
                    sale_total += remaining
                remaining = 0.0

    applied = float(round(payment_amount - remaining, 2))
    if sale_total > 0:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO sales (total, date) VALUES (?, ?)",
                (round(sale_total, 2), datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
            conn.commit()

    return {"applied": applied, "remaining": float(round(remaining, 2)), "details": details}

