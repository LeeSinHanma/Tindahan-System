from db import database
from core import inventory
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from datetime import datetime


def _to_positive_int(value: int | str, label: str = "Quantity") -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a whole number")

    if parsed <= 0:
        raise ValueError(f"{label} must be at least 1")
    return parsed


def list_items(include_done: bool = True) -> list[dict]:
    return database.list_shopping_list_items(include_done)


def get_total(include_done: bool = True) -> float:
    total = 0.0
    for item in list_items(include_done):
        total += float(item["product"]["original_price"] or 0) * int(item["quantity"] or 0)
    return total


def add_item(product_id: int, quantity: int | str = 1) -> int:
    qty = _to_positive_int(quantity)
    return database.add_shopping_list_item(int(product_id), qty)


def add_low_stock_items() -> int:
    threshold = inventory.get_low_stock_threshold()
    products = inventory.get_low_stock_products(threshold)
    added_count = 0

    for product in products:
        restock_quantity = max(threshold - int(product["stock"] or 0), 1)
        database.add_shopping_list_item(int(product["id"]), restock_quantity)
        added_count += 1

    return added_count


def update_item_quantity(item_id: int, quantity: int | str) -> None:
    qty = _to_positive_int(quantity)
    database.update_shopping_list_item_quantity(int(item_id), qty)


def mark_done(item_id: int, is_done: bool) -> None:
    database.set_shopping_list_item_done(int(item_id), bool(is_done))


def remove_item(item_id: int) -> None:
    database.delete_shopping_list_item(int(item_id))


def clear_done_items() -> None:
    database.clear_done_shopping_list_items()


def clear_all_items() -> None:
    database.clear_all_shopping_list_items()


def save_pdf(file_path: str, include_done: bool = True) -> None:
    items = list_items(include_done)
    total = get_total(include_done)

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
        "ShoppingListTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "ShoppingListBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
    )

    story: list = []
    story.append(Paragraph("Shopping List", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    story.append(Paragraph(f"Total: PHP {total:.2f}", body_style))
    story.append(Spacer(1, 0.2 * inch))

    table_data = [["Product", "Description", "Orig. Price", "Qty", "Status", "Purchased At"]]
    for item in items:
        table_data.append(
            [
                Paragraph(item["product"]["name"], body_style),
                Paragraph(item["product"]["description"] or "-", body_style),
                f"PHP {float(item['product']['original_price'] or 0):.2f}",
                str(item["quantity"]),
                "Done" if item["is_done"] else "Pending",
                item["purchased_at"] or "-",
            ]
        )

    table = Table(table_data, repeatRows=1, colWidths=[1.8 * inch, 2.3 * inch, 0.9 * inch, 0.5 * inch, 0.8 * inch, 1.2 * inch])
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
