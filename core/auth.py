"""Account setup and sign-in using hashed passwords."""

import sqlite3
from contextlib import closing

from core.passwords import hash_password, password_error, verify_password
from db.database import get_connection

USER_COLUMNS = "id, username, is_admin, created_at, must_change_password"


def _user(row: sqlite3.Row) -> dict:
    return {
        "id": int(row["id"]),
        "username": row["username"],
        "is_admin": bool(row["is_admin"]),
        "created_at": row["created_at"],
        "must_change_password": bool(row["must_change_password"]),
    }


def needs_initial_setup() -> bool:
    with closing(get_connection()) as connection:
        return connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0


def create_initial_admin(username: str, password: str) -> dict:
    username = username.strip()
    if not username:
        raise ValueError("Enter a username for the store owner.")
    if error := password_error(password):
        raise ValueError(error)
    encoded = hash_password(password)
    with closing(get_connection()) as connection, connection:
        # Two app instances must not both create a first administrator.
        connection.execute("BEGIN IMMEDIATE")
        if connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
            raise ValueError("Account setup is already complete. Sign in instead.")
        cursor = connection.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, 1)",
            (username, encoded),
        )
        row = connection.execute(
            f"SELECT {USER_COLUMNS} FROM users WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        connection.execute(
            "DELETE FROM settings WHERE key IN ('persistent_login_enabled', 'persistent_login_username')"
        )
        return _user(row)


def add_user(username: str, password: str, is_admin: bool = False) -> bool:
    username = username.strip()
    if not username or password_error(password):
        return False
    try:
        with closing(get_connection()) as connection, connection:
            connection.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                (username, hash_password(password), int(is_admin)),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def verify_user(username: str, password: str) -> dict | None:
    if not username or not password:
        return None
    with closing(get_connection()) as connection:
        row = connection.execute(
            f"SELECT {USER_COLUMNS}, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None or not verify_password(password, row["password"]):
        return None
    return _user(row)


def get_user_by_username(username: str) -> dict | None:
    with closing(get_connection()) as connection:
        row = connection.execute(
            f"SELECT {USER_COLUMNS} FROM users WHERE username = ?", (username,)
        ).fetchone()
    return _user(row) if row else None


def get_users() -> list[dict]:
    with closing(get_connection()) as connection:
        rows = connection.execute(
            f"SELECT {USER_COLUMNS} FROM users ORDER BY username COLLATE NOCASE"
        ).fetchall()
    return [_user(row) for row in rows]


def change_password(username: str, old_password: str, new_password: str) -> bool:
    if not username or not old_password or password_error(new_password):
        return False
    with closing(get_connection()) as connection, connection:
        row = connection.execute(
            "SELECT id, password, must_change_password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if row is None or not verify_password(old_password, row["password"]):
            return False
        if row["must_change_password"] and old_password == new_password:
            return False
        cursor = connection.execute(
            "UPDATE users SET password = ?, must_change_password = 0 WHERE id = ? AND password = ?",
            (hash_password(new_password), row["id"], row["password"]),
        )
        if cursor.rowcount != 1:
            return False
        remembered = connection.execute(
            "SELECT value FROM settings WHERE key = 'persistent_login_username'"
        ).fetchone()
        if remembered and remembered["value"] == username:
            connection.execute(
                "DELETE FROM settings WHERE key IN ('persistent_login_enabled', 'persistent_login_username')"
            )
    return True
