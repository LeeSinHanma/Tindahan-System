from core.inventory import get_product_by_barcode, search_products


def lookup_product(barcode: str) -> dict | None:
    return get_product_by_barcode(barcode)