from db.database import record_sale, reduce_stock_for_cart_items, validate_cart_item_stock


def complete_sale(cart_items: list[dict], total: float, date_value: str) -> int:
    if not cart_items:
        raise ValueError("Cart is empty")
    return record_sale(cart_items, total, date_value)


def finalize_debt_checkout(cart_items: list[dict]) -> None:
    if not cart_items:
        raise ValueError("Cart is empty")
    reduce_stock_for_cart_items(cart_items)


def validate_checkout_stock(cart_items: list[dict]) -> None:
    validate_cart_item_stock(cart_items)