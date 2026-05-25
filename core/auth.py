from db.database import get_connection


def add_user(username: str, password: str, is_admin: bool = False) -> bool:
    if not username or not password:
        return False
    with get_connection() as conn:
        try:
            conn.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                (username, password, 1 if is_admin else 0),
            )
            conn.commit()
            return True
        except Exception:
            return False


def verify_user(username: str, password: str) -> dict | None:
    if not username or not password:
        return None
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, is_admin, created_at FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
    if row is None:
        return None
    return {"id": int(row["id"]), "username": row["username"], "is_admin": bool(int(row["is_admin"])), "created_at": row["created_at"]}


def get_user_by_username(username: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, is_admin, created_at FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None:
        return None
    return {"id": int(row["id"]), "username": row["username"], "is_admin": bool(int(row["is_admin"])), "created_at": row["created_at"]}


def get_users() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, username, is_admin, created_at FROM users ORDER BY username COLLATE NOCASE").fetchall()
    return [{"id": int(r["id"]), "username": r["username"], "is_admin": bool(int(r["is_admin"])), "created_at": r["created_at"]} for r in rows]


def change_password(username: str, old_password: str, new_password: str) -> bool:
    if not username or not old_password or not new_password:
        return False
    # verify old password
    if verify_user(username, old_password) is None:
        return False
    with get_connection() as conn:
        try:
            conn.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new_password, username),
            )
            conn.commit()
            return True
        except Exception:
            return False
from db.database import get_connection


def add_user(username: str, password: str, is_admin: bool = False) -> bool:
    if not username or not password:
        return False
    with get_connection() as conn:
        try:
            conn.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                (username, password, 1 if is_admin else 0),
            )
            conn.commit()
            return True
        except Exception:
            return False


def verify_user(username: str, password: str) -> dict | None:
    if not username or not password:
        return None
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, is_admin, created_at FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
    if row is None:
        return None
    return {"id": int(row["id"]), "username": row["username"], "is_admin": bool(int(row["is_admin"])), "created_at": row["created_at"]}


def get_users() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, username, is_admin, created_at FROM users ORDER BY username COLLATE NOCASE").fetchall()
    return [{"id": int(r["id"]), "username": r["username"], "is_admin": bool(int(r["is_admin"])), "created_at": r["created_at"]} for r in rows]
