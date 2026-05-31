import json
import sqlite3
import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

DB_FILE = BASE_DIR / "pos.db"
LOW_STOCK_THRESHOLD = 10


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"] for row in rows}


def _ensure_column(
    conn: sqlite3.Connection,
    table_name: str,
    column_name: str,
    column_definition: str,
) -> None:
    columns = _table_columns(conn, table_name)
    if column_name not in columns:
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")


def _legacy_price_column_exists(conn: sqlite3.Connection) -> bool:
    return "price" in _table_columns(conn, "products")


def _stock_tracked_column_exists(conn: sqlite3.Connection) -> bool:
    return "stock_tracked" in _table_columns(conn, "products")


def init_database() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                barcode TEXT UNIQUE NOT NULL,
                original_price REAL NOT NULL DEFAULT 0,
                sell_price REAL NOT NULL DEFAULT 0,
                stock INTEGER NOT NULL DEFAULT 0,
                stock_tracked INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total REAL NOT NULL,
                date TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shopping_list_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                is_done INTEGER NOT NULL DEFAULT 0,
                purchased_at TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                UNIQUE(product_id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
            """
        )
        _ensure_column(conn, "shopping_list_items", "purchased_at", "TEXT")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS debt_tracker (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_name TEXT NOT NULL,
                amount REAL NOT NULL,
                is_paid INTEGER NOT NULL DEFAULT 0,
                description TEXT DEFAULT '',
                sale_linked INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                paid_at TEXT
            )
            """
        )

        _ensure_column(conn, "debt_tracker", "description", "TEXT DEFAULT ''")
        _ensure_column(conn, "debt_tracker", "sale_linked", "INTEGER NOT NULL DEFAULT 1")
        conn.execute("UPDATE debt_tracker SET sale_linked = COALESCE(sale_linked, 1)")

        # Customers table to support account-style debt tracking
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )

        # ensure default admin user exists (hardcoded credentials)
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            ("admin", "KennyDLuffy213", 1),
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                action TEXT NOT NULL,
                details TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )

        _ensure_column(conn, "products", "description", "TEXT NOT NULL DEFAULT ''")
        _ensure_column(conn, "products", "original_price", "REAL NOT NULL DEFAULT 0")
        _ensure_column(conn, "products", "sell_price", "REAL NOT NULL DEFAULT 0")
        _ensure_column(conn, "products", "stock", "INTEGER NOT NULL DEFAULT 0")
        _ensure_column(conn, "products", "stock_tracked", "INTEGER NOT NULL DEFAULT 0")

        columns = _table_columns(conn, "products")
        if "price" in columns:
            conn.execute(
                """
                UPDATE products
                SET original_price = CASE
                    WHEN original_price = 0 THEN price
                    ELSE original_price
                END,
                sell_price = CASE
                    WHEN sell_price = 0 THEN price
                    ELSE sell_price
                END
                WHERE price IS NOT NULL
                """
            )

        if _stock_tracked_column_exists(conn):
            conn.execute("UPDATE products SET stock_tracked = COALESCE(stock_tracked, 0)")

        conn.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            ("low_stock_threshold", "10"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            ("quick_access_product_ids", "[]"),
        )

        conn.commit()


def record_user_audit(username: str | None, user_id: int | None, action: str, details: str | None = None) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO user_audit (user_id, username, action, details) VALUES (?, ?, ?, ?)",
            (user_id, username, action, details),
        )
        conn.commit()


def _normalize_product_row(row: sqlite3.Row) -> dict:
    return {
        "id": int(row["id"]),
        "name": row["name"],
        "description": row["description"] or "",
        "barcode": row["barcode"],
        "original_price": float(row["original_price"] or 0),
        "sell_price": float(row["sell_price"] or 0),
        "stock": int(row["stock"] or 0),
        "stock_tracked": bool(int(row["stock_tracked"] or 0)) if "stock_tracked" in row.keys() else False,
    }


def list_products(search_term: str = "") -> list[dict]:
    search = search_term.strip()
    with get_connection() as conn:
        if search:
            rows = conn.execute(
                """
                SELECT id, name, description, barcode, original_price, sell_price, stock
                      , stock_tracked
                FROM products
                WHERE name LIKE ? OR barcode LIKE ?
                ORDER BY name COLLATE NOCASE
                """,
                (f"%{search}%", f"%{search}%"),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, name, description, barcode, original_price, sell_price, stock
                       , stock_tracked
                FROM products
                ORDER BY name COLLATE NOCASE
                """
            ).fetchall()

    return [_normalize_product_row(row) for row in rows]


def get_product_by_id(product_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, name, description, barcode, original_price, sell_price, stock
                     , stock_tracked
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()
    return None if row is None else _normalize_product_row(row)


def get_product_by_barcode(barcode: str) -> dict | None:
    clean_barcode = barcode.strip()
    if not clean_barcode:
        return None

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, name, description, barcode, original_price, sell_price, stock
                   , stock_tracked
            FROM products
            WHERE barcode = ?
            """,
            (clean_barcode,),
        ).fetchone()
    return None if row is None else _normalize_product_row(row)


def create_product(product_data: dict) -> int:
    with get_connection() as conn:
        columns = ["name", "description", "barcode", "original_price", "sell_price", "stock", "stock_tracked"]
        values = [
            product_data["name"],
            product_data.get("description", ""),
            product_data["barcode"],
            product_data["original_price"],
            product_data["sell_price"],
            product_data["stock"],
            int(bool(product_data.get("stock_tracked", False))),
        ]

        if _legacy_price_column_exists(conn):
            columns.insert(4, "price")
            values.insert(4, product_data["sell_price"])

        if not _stock_tracked_column_exists(conn):
            columns.remove("stock_tracked")
            values.pop()

        cursor = conn.execute(
            f"""
            INSERT INTO products ({', '.join(columns)})
            VALUES ({', '.join(['?'] * len(columns))})
            """,
            tuple(values),
        )
        conn.commit()
        return int(cursor.lastrowid)


def update_product(product_id: int, product_data: dict) -> None:
    with get_connection() as conn:
        if _legacy_price_column_exists(conn):
            conn.execute(
                """
                UPDATE products
                SET name = ?,
                    description = ?,
                    barcode = ?,
                    price = ?,
                    original_price = ?,
                    sell_price = ?,
                    stock = ?,
                    stock_tracked = ?
                WHERE id = ?
                """,
                (
                    product_data["name"],
                    product_data.get("description", ""),
                    product_data["barcode"],
                    product_data["sell_price"],
                    product_data["original_price"],
                    product_data["sell_price"],
                    product_data["stock"],
                    int(bool(product_data.get("stock_tracked", False))),
                    product_id,
                ),
            )
            conn.commit()
            return

        conn.execute(
            """
            UPDATE products
            SET name = ?,
                description = ?,
                barcode = ?,
                original_price = ?,
                sell_price = ?,
                stock = ?,
                stock_tracked = ?
            WHERE id = ?
            """,
            (
                product_data["name"],
                product_data.get("description", ""),
                product_data["barcode"],
                product_data["original_price"],
                product_data["sell_price"],
                product_data["stock"],
                int(bool(product_data.get("stock_tracked", False))),
                product_id,
            ),
        )
        conn.commit()


def delete_product(product_id: int) -> None:
    with get_connection() as conn:
        usage_count = conn.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM sale_items WHERE product_id = ?) +
                (SELECT COUNT(*) FROM shopping_list_items WHERE product_id = ?)
            AS usage_count
            """,
            (product_id, product_id),
        ).fetchone()["usage_count"]

        if usage_count:
            raise ValueError("Cannot delete a product that is used in a sale or shopping list.")

        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()


def set_stock(product_id: int, stock_value: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE products SET stock = ? WHERE id = ?",
            (stock_value, product_id),
        )
        conn.commit()


def set_stock_tracking(product_id: int, stock_tracked: bool, stock_value: int | None = None) -> None:
    with get_connection() as conn:
        if stock_value is None:
            conn.execute(
                "UPDATE products SET stock_tracked = ? WHERE id = ?",
                (1 if stock_tracked else 0, product_id),
            )
        else:
            conn.execute(
                "UPDATE products SET stock_tracked = ?, stock = ? WHERE id = ?",
                (1 if stock_tracked else 0, stock_value, product_id),
            )
        conn.commit()


def adjust_stock(product_id: int, delta: int) -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT stock FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        if row is None:
            raise ValueError("Product not found")

        current_stock = int(row["stock"] or 0)
        new_stock = current_stock + delta
        if new_stock < 0:
            raise ValueError("Insufficient stock")

        conn.execute(
            "UPDATE products SET stock = ? WHERE id = ?",
            (new_stock, product_id),
        )
        conn.commit()
        return new_stock


def get_low_stock_products(threshold: int | None = None) -> list[dict]:
    if threshold is None:
        threshold = get_low_stock_threshold()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, description, barcode, original_price, sell_price, stock, stock_tracked
            FROM products
            WHERE stock_tracked = 1 AND stock <= ?
            ORDER BY stock ASC, name COLLATE NOCASE
            """,
            (threshold,),
        ).fetchall()
    return [_normalize_product_row(row) for row in rows]


def get_untracked_products(search_term: str = "") -> list[dict]:
    search = search_term.strip()
    with get_connection() as conn:
        if search:
            rows = conn.execute(
                """
                SELECT id, name, description, barcode, original_price, sell_price, stock, stock_tracked
                FROM products
                WHERE stock_tracked = 0 AND (name LIKE ? OR barcode LIKE ?)
                ORDER BY name COLLATE NOCASE
                """,
                (f"%{search}%", f"%{search}%"),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, name, description, barcode, original_price, sell_price, stock, stock_tracked
                FROM products
                WHERE stock_tracked = 0
                ORDER BY name COLLATE NOCASE
                """
            ).fetchall()
    return [_normalize_product_row(row) for row in rows]


def _sales_period_clause(period_days: int | None) -> tuple[str, tuple]:
    if period_days is None:
        return "", ()

    days = max(int(period_days), 1)
    clause = "WHERE date(date) >= date('now', ?)"
    return clause, (f"-{days - 1} day",)


def get_sales_summary(period_days: int | None = None) -> dict:
    sales_clause, sales_params = _sales_period_clause(period_days)

    with get_connection() as conn:
        product_row = conn.execute(
            """
            SELECT COUNT(*) AS product_count,
                   COALESCE(SUM(stock), 0) AS total_stock,
                   COALESCE(SUM(stock * sell_price), 0) AS inventory_value
            FROM products
            """
        ).fetchone()

        low_stock_row = conn.execute(
            "SELECT COUNT(*) AS low_stock_count FROM products WHERE stock_tracked = 1 AND stock <= ?",
            (get_low_stock_threshold(),),
        ).fetchone()

        untracked_row = conn.execute(
            "SELECT COUNT(*) AS untracked_count FROM products WHERE stock_tracked = 0",
        ).fetchone()

        sales_row = conn.execute(
            f"""
            SELECT COALESCE(COUNT(*), 0) AS sale_count,
                   COALESCE(SUM(total), 0) AS total_sales
            FROM sales
            {sales_clause}
            """,
            sales_params,
        ).fetchone()

    return {
        "product_count": int(product_row["product_count"] or 0),
        "total_stock": int(product_row["total_stock"] or 0),
        "inventory_value": float(product_row["inventory_value"] or 0),
        "low_stock_count": int(low_stock_row["low_stock_count"] or 0),
        "untracked_count": int(untracked_row["untracked_count"] or 0),
        "sale_count": int(sales_row["sale_count"] or 0),
        "total_sales": float(sales_row["total_sales"] or 0),
    }


def get_recent_sales(limit: int = 5, period_days: int | None = None) -> list[dict]:
    sales_clause, sales_params = _sales_period_clause(period_days)

    with get_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT id, total, date
            FROM sales
            {sales_clause}
            ORDER BY datetime(date) DESC, id DESC
            LIMIT ?
            """,
            (*sales_params, limit),
        ).fetchall()

    return [
        {
            "id": int(row["id"]),
            "total": float(row["total"] or 0),
            "date": row["date"],
        }
        for row in rows
    ]


def get_daily_sales(days: int = 7) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT date(date) AS sale_day,
                   COALESCE(SUM(total), 0) AS total
            FROM sales
            WHERE date(date) >= date('now', ?)
            GROUP BY date(date)
            ORDER BY date(date) ASC
            """,
            (f"-{max(days - 1, 0)} day",),
        ).fetchall()

    return [{"day": row["sale_day"], "total": float(row["total"] or 0)} for row in rows]


def get_top_selling_products(limit: int = 5, period_days: int | None = None) -> list[dict]:
    sales_clause, sales_params = _sales_period_clause(period_days)

    with get_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT p.name AS product_name,
                   COALESCE(SUM(si.quantity), 0) AS total_qty,
                   COALESCE(SUM(si.quantity * si.price), 0) AS revenue
            FROM sale_items si
            INNER JOIN products p ON p.id = si.product_id
            INNER JOIN sales s ON s.id = si.sale_id
            {sales_clause.replace('date(date)', 'date(s.date)')}
            GROUP BY si.product_id, p.name
            ORDER BY total_qty DESC, revenue DESC
            LIMIT ?
            """,
            (*sales_params, limit),
        ).fetchall()

    return [
        {
            "product_name": row["product_name"],
            "total_qty": int(row["total_qty"] or 0),
            "revenue": float(row["revenue"] or 0),
        }
        for row in rows
    ]


def _validate_stock_for_cart_items(cursor: sqlite3.Cursor, cart_items: list[dict]) -> None:
    for item in cart_items:
        row = cursor.execute(
            "SELECT stock, stock_tracked FROM products WHERE id = ?",
            (item["product_id"],),
        ).fetchone()
        if row is None:
            raise ValueError("Product not found")

        quantity = int(item["quantity"])
        if int(row["stock_tracked"] or 0) == 1:
            current_stock = int(row["stock"] or 0)
            if current_stock < quantity:
                raise ValueError(f"Insufficient stock for {item['name']}")


def reduce_stock_for_cart_items(cart_items: list[dict]) -> None:
    if not cart_items:
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        _validate_stock_for_cart_items(cursor, cart_items)
        cursor.executemany(
            """
            UPDATE products
            SET stock = stock - ?
            WHERE id = ? AND stock_tracked = 1
            """,
            [(item["quantity"], item["product_id"]) for item in cart_items],
        )
        conn.commit()


def validate_cart_item_stock(cart_items: list[dict]) -> None:
    if not cart_items:
        raise ValueError("Cart is empty")

    _apply_stock_changes(cart_items)

    with get_connection() as conn:
        cursor = conn.cursor()
        _validate_stock_for_cart_items(cursor, cart_items)


def record_sale(cart_items: list[dict], total: float, date_value: str) -> int:
    if not cart_items:
        raise ValueError("Cart is empty")

    with get_connection() as conn:
        cursor = conn.cursor()
        _validate_stock_for_cart_items(cursor, cart_items)

        cursor.execute(
            "INSERT INTO sales (total, date) VALUES (?, ?)",
            (total, date_value),
        )
        sale_id = int(cursor.lastrowid)

        cursor.executemany(
            """
            INSERT INTO sale_items (sale_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    sale_id,
                    item["product_id"],
                    item["quantity"],
                    item["price"],
                )
                for item in cart_items
            ],
        )

        cursor.executemany(
            """
            UPDATE products
            SET stock = stock - ?
            WHERE id = ? AND stock_tracked = 1
            """,
            [(item["quantity"], item["product_id"]) for item in cart_items],
        )

        conn.commit()
        return sale_id


def _apply_stock_changes(cart_items: list[dict]) -> None:
    if not cart_items:
        raise ValueError("Cart is empty")

    with get_connection() as conn:
        cursor = conn.cursor()

        for item in cart_items:
            row = cursor.execute(
                "SELECT stock, stock_tracked FROM products WHERE id = ?",
                (item["product_id"],),
            ).fetchone()
            if row is None:
                raise ValueError("Product not found")

            quantity = int(item["quantity"])
            if int(row["stock_tracked"] or 0) == 1:
                current_stock = int(row["stock"] or 0)
                if current_stock < quantity:
                    raise ValueError(f"Insufficient stock for {item['name']}")

        cursor.executemany(
            """
            UPDATE products
            SET stock = stock - ?
            WHERE id = ? AND stock_tracked = 1
            """,
            [(item["quantity"], item["product_id"]) for item in cart_items],
        )

        conn.commit()


def apply_stock_changes(cart_items: list[dict]) -> None:
    _apply_stock_changes(cart_items)


def get_setting(key: str, default: str | int = "") -> int | str:
    with get_connection() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    
    if row is None:
        return default
    
    value = row["value"]
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


def set_setting(key: str, value: str | int) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, str(value)),
        )
        conn.commit()


def get_low_stock_threshold() -> int:
    return int(get_setting("low_stock_threshold", 10))


def get_quick_access_product_ids() -> list[int]:
    raw_value = get_setting("quick_access_product_ids", "[]")
    if isinstance(raw_value, int):
        raw_value = str(raw_value)

    try:
        parsed_value = json.loads(raw_value)
    except (TypeError, ValueError, json.JSONDecodeError):
        return []

    if not isinstance(parsed_value, list):
        return []

    product_ids: list[int] = []
    for item in parsed_value:
        try:
            product_ids.append(int(item))
        except (TypeError, ValueError):
            continue
    return product_ids


def set_quick_access_product_ids(product_ids: list[int]) -> None:
    unique_ids: list[int] = []
    seen_ids: set[int] = set()
    for item in product_ids:
        try:
            product_id = int(item)
        except (TypeError, ValueError):
            continue
        if product_id in seen_ids:
            continue
        seen_ids.add(product_id)
        unique_ids.append(product_id)

    set_setting("quick_access_product_ids", json.dumps(unique_ids))


def list_shopping_list_items(include_done: bool = True) -> list[dict]:
    with get_connection() as conn:
        if include_done:
            rows = conn.execute(
                """
                SELECT s.id,
                       s.product_id,
                       s.quantity,
                       s.is_done,
                     s.purchased_at,
                       s.created_at,
                       p.name,
                       p.description,
                       p.barcode,
                       p.original_price,
                       p.sell_price,
                       p.stock,
                       p.stock_tracked
                FROM shopping_list_items s
                INNER JOIN products p ON p.id = s.product_id
                ORDER BY s.is_done ASC, s.created_at ASC, p.name COLLATE NOCASE
                """
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT s.id,
                       s.product_id,
                       s.quantity,
                       s.is_done,
                     s.purchased_at,
                       s.created_at,
                       p.name,
                       p.description,
                       p.barcode,
                       p.original_price,
                       p.sell_price,
                       p.stock,
                       p.stock_tracked
                FROM shopping_list_items s
                INNER JOIN products p ON p.id = s.product_id
                WHERE s.is_done = 0
                ORDER BY s.created_at ASC, p.name COLLATE NOCASE
                """
            ).fetchall()

    items: list[dict] = []
    for row in rows:
        items.append(
            {
                "id": int(row["id"]),
                "product_id": int(row["product_id"]),
                "quantity": int(row["quantity"] or 1),
                "is_done": bool(int(row["is_done"] or 0)),
                "purchased_at": row["purchased_at"],
                "created_at": row["created_at"],
                "product": {
                    "id": int(row["product_id"]),
                    "name": row["name"],
                    "description": row["description"] or "",
                    "barcode": row["barcode"],
                    "original_price": float(row["original_price"] or 0),
                    "sell_price": float(row["sell_price"] or 0),
                    "stock": int(row["stock"] or 0),
                    "stock_tracked": bool(int(row["stock_tracked"] or 0)),
                },
            }
        )
    return items


def add_shopping_list_item(product_id: int, quantity: int = 1) -> int:
    if quantity <= 0:
        raise ValueError("Quantity must be at least 1")

    with get_connection() as conn:
        product_row = conn.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
        if product_row is None:
            raise ValueError("Product not found")

        existing = conn.execute(
            "SELECT id, quantity FROM shopping_list_items WHERE product_id = ?",
            (product_id,),
        ).fetchone()

        if existing is None:
            cursor = conn.execute(
                """
                INSERT INTO shopping_list_items (product_id, quantity, is_done)
                VALUES (?, ?, 0)
                """,
                (product_id, quantity),
            )
            conn.commit()
            return int(cursor.lastrowid)

        new_quantity = int(existing["quantity"] or 0) + quantity
        conn.execute(
            """
            UPDATE shopping_list_items
            SET quantity = ?,
                is_done = 0
            WHERE id = ?
            """,
            (new_quantity, int(existing["id"])),
        )
        conn.commit()
        return int(existing["id"])


def _shopping_list_item_row(conn: sqlite3.Connection, item_id: int) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT s.id,
               s.product_id,
               s.quantity,
               s.is_done,
               s.purchased_at,
               p.stock,
               p.stock_tracked
        FROM shopping_list_items s
        INNER JOIN products p ON p.id = s.product_id
        WHERE s.id = ?
        """,
        (item_id,),
    ).fetchone()


def update_shopping_list_item_quantity(item_id: int, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Quantity must be at least 1")

    with get_connection() as conn:
        row = _shopping_list_item_row(conn, item_id)
        if row is None:
            raise ValueError("Shopping list item not found")

        current_quantity = int(row["quantity"] or 0)
        is_done = int(row["is_done"] or 0) == 1
        if is_done:
            delta = quantity - current_quantity
            if delta > 0:
                conn.execute(
                    "UPDATE products SET stock = stock + ? WHERE id = ?",
                    (delta, int(row["product_id"])),
                )
            elif delta < 0:
                stock_value = int(row["stock"] or 0)
                if stock_value < abs(delta):
                    raise ValueError("Insufficient stock to reduce purchased quantity")
                conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ?",
                    (abs(delta), int(row["product_id"])),
                )

        conn.execute(
            "UPDATE shopping_list_items SET quantity = ? WHERE id = ?",
            (quantity, item_id),
        )
        conn.commit()


def set_shopping_list_item_done(item_id: int, is_done: bool) -> None:
    with get_connection() as conn:
        row = _shopping_list_item_row(conn, item_id)
        if row is None:
            raise ValueError("Shopping list item not found")

        current_done = int(row["is_done"] or 0) == 1
        target_done = bool(is_done)
        quantity = int(row["quantity"] or 0)

        if current_done == target_done:
            if target_done:
                conn.execute(
                    "UPDATE shopping_list_items SET purchased_at = COALESCE(purchased_at, datetime('now')) WHERE id = ?",
                    (item_id,),
                )
            conn.commit()
            return

        if target_done:
            conn.execute(
                "UPDATE products SET stock = stock + ? WHERE id = ?",
                (quantity, int(row["product_id"])),
            )
            conn.execute(
                """
                UPDATE shopping_list_items
                SET is_done = 1,
                    purchased_at = datetime('now')
                WHERE id = ?
                """,
                (item_id,),
            )
        else:
            stock_value = int(row["stock"] or 0)
            if stock_value < quantity:
                raise ValueError("Insufficient stock to mark item as pending")
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (quantity, int(row["product_id"])),
            )
            conn.execute(
                """
                UPDATE shopping_list_items
                SET is_done = 0,
                    purchased_at = NULL
                WHERE id = ?
                """,
                (item_id,),
            )

        conn.commit()


def delete_shopping_list_item(item_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM shopping_list_items WHERE id = ?", (item_id,))
        conn.commit()


def clear_done_shopping_list_items() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM shopping_list_items WHERE is_done = 1")
        conn.commit()


def clear_all_shopping_list_items() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM shopping_list_items")
        conn.commit()