from db.database import record_sale


def complete_sale(cart_items: list[dict], total: float, date_value: str) -> int:
    if not cart_items:
        raise ValueError("Cart is empty")
    return record_sale(cart_items, total, date_value)