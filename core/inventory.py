from datetime import datetime

from db import database
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def get_low_stock_threshold() -> int:
    return database.get_low_stock_threshold()


def set_low_stock_threshold(threshold: int) -> None:
    if threshold < 0:
        raise ValueError("Low stock threshold cannot be negative")
    database.set_setting("low_stock_threshold", threshold)


def get_quick_access_product_ids() -> list[int]:
    return database.get_quick_access_product_ids()


def set_quick_access_product_ids(product_ids: list[int]) -> None:
    database.set_quick_access_product_ids(product_ids)


def get_quick_access_products() -> list[dict]:
    products: list[dict] = []
    for product_id in get_quick_access_product_ids():
        product = get_product_by_id(product_id)
        if product is not None:
            products.append(product)
    return products




def _clean_text(value: str | None) -> str:
    return (value or "").strip()


def _to_int(value, default: int = 0) -> int:
    if value in (None, ""):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError("Stock must be a whole number")


def _to_float(value, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError("Price must be a number")


def _normalize_product_data(product_data: dict) -> dict:
    name = _clean_text(product_data.get("name"))
    description = _clean_text(product_data.get("description"))
    barcode = _clean_text(product_data.get("barcode"))
    stock_tracked = bool(product_data.get("stock_tracked", False))
    original_price = _to_float(product_data.get("original_price"))
    sell_price = _to_float(product_data.get("sell_price"))
    stock = _to_int(product_data.get("stock"))

    if not name:
        raise ValueError("Product name is required")
    if not barcode:
        raise ValueError("Barcode is required")
    if original_price < 0 or sell_price < 0:
        raise ValueError("Price cannot be negative")
    if stock < 0:
        raise ValueError("Stock cannot be negative")
    if original_price == 0 and sell_price == 0:
        raise ValueError("At least one price is required")

    if original_price == 0 and sell_price > 0:
        original_price = sell_price
    if sell_price == 0 and original_price > 0:
        sell_price = original_price

    if not stock_tracked:
        stock = 0

    return {
        "name": name,
        "description": description,
        "barcode": barcode,
        "original_price": original_price,
        "sell_price": sell_price,
        "stock": stock,
        "stock_tracked": stock_tracked,
    }


def list_products(search_term: str = "") -> list[dict]:
    return database.list_products(search_term)


def search_products(search_term: str) -> list[dict]:
    return database.list_products(search_term)


def get_product_by_id(product_id: int) -> dict | None:
    return database.get_product_by_id(product_id)


def get_product_by_barcode(barcode: str) -> dict | None:
    return database.get_product_by_barcode(barcode)


def get_untracked_products(search_term: str = "") -> list[dict]:
    return database.get_untracked_products(search_term)


def create_product(product_data: dict) -> int:
    return database.create_product(_normalize_product_data(product_data))


def update_product(product_id: int, product_data: dict) -> None:
    database.update_product(product_id, _normalize_product_data(product_data))


def delete_product(product_id: int) -> None:
    database.delete_product(product_id)


def set_stock(product_id: int, stock_value: int) -> None:
    if stock_value < 0:
        raise ValueError("Stock cannot be negative")
    database.set_stock(product_id, stock_value)


def adjust_stock(product_id: int, delta: int) -> int:
    return database.adjust_stock(product_id, delta)


def apply_stock_changes(cart_items: list[dict]) -> None:
    database.apply_stock_changes(cart_items)


def set_stock_tracking(product_id: int, stock_tracked: bool, stock_value: int | None = None) -> None:
    database.set_stock_tracking(product_id, stock_tracked, stock_value)


def get_low_stock_products(threshold: int | None = None) -> list[dict]:
    if threshold is None:
        threshold = get_low_stock_threshold()
    return database.get_low_stock_products(threshold)


def save_pdf(file_path: str) -> None:
    products = list_products()
    summary = database.get_sales_summary()

    document = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "InventoryTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "InventoryBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
    )

    story: list = []
    story.append(Paragraph("Inventory Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    story.append(Paragraph(f"Products: {summary['product_count']}", body_style))
    story.append(Paragraph(f"Total Stock: {summary['total_stock']}", body_style))
    story.append(Paragraph(f"Inventory Value: PHP {summary['inventory_value']:.2f}", body_style))
    story.append(Spacer(1, 0.2 * inch))

    table_data = [["ID", "Name", "Barcode", "Orig. Price", "Sell Price", "Stock", "Tracked"]]
    for product in products:
        table_data.append(
            [
                str(product["id"]),
                Paragraph(product["name"], body_style),
                Paragraph(product["barcode"] or "-", body_style),
                f"PHP {float(product['original_price'] or 0):.2f}",
                f"PHP {float(product['sell_price'] or 0):.2f}",
                str(product["stock"]),
                "Yes" if product.get("stock_tracked", False) else "No",
            ]
        )

    if len(table_data) == 1:
        table_data.append(["-", "No products found", "-", "-", "-", "-", "-"])

    table = Table(
        table_data,
        repeatRows=1,
        colWidths=[0.45 * inch, 1.8 * inch, 1.15 * inch, 0.9 * inch, 0.9 * inch, 0.6 * inch, 0.7 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#f8fafc")]),
            ]
        )
    )
    story.append(table)

    document.build(story)