"""Password hashing and migration helpers shared by account setup and login."""

import hashlib
import hmac
import secrets
import sqlite3

ITERATIONS = 600_000
MIN_PASSWORD_LENGTH = 4
PREFIX = "pbkdf2_sha256$"
# Fingerprint of the retired public credential, used only to require replacement.
# The credential itself is never included in current source or generated accounts.
RETIRED_PASSWORD_DIGEST = (
    "d626a8e2ea51cee2c34cfdd8b88fdbf64bbfa34122a200cb93e70c2e14b389a4"
)


def is_retired_password(password: str) -> bool:
    return hmac.compare_digest(
        hashlib.sha256(password.encode("utf-8")).hexdigest(), RETIRED_PASSWORD_DIGEST
    )


def password_error(password: str) -> str | None:
    if len(password) < MIN_PASSWORD_LENGTH or not password.strip():
        return f"Use a password with at least {MIN_PASSWORD_LENGTH} characters."
    if len(password) > 1024:
        return "Use a password with at most 1024 characters."
    if is_retired_password(password):
        return "Choose a new password; the old default password is no longer allowed."
    return None


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"{PREFIX}{ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt, expected = encoded.split("$")
        count = int(iterations)
        if algorithm != "pbkdf2_sha256" or not 1 <= count <= 2_000_000:
            return False
        salt_bytes, expected_bytes = bytes.fromhex(salt), bytes.fromhex(expected)
        if len(salt_bytes) != 16 or len(expected_bytes) != 32:
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt_bytes, count
        )
        return hmac.compare_digest(actual, expected_bytes)
    except (ValueError, TypeError):
        return False


def migrate_passwords(connection: sqlite3.Connection) -> None:
    """Preserve account identities while replacing legacy plaintext storage."""
    for row in connection.execute("SELECT id, password FROM users").fetchall():
        stored = row["password"]
        if stored.startswith(PREFIX):
            continue
        requires_change = int(is_retired_password(stored))
        connection.execute(
            "UPDATE users SET password = ?, must_change_password = MAX(must_change_password, ?) WHERE id = ?",
            (hash_password(stored), requires_change, row["id"]),
        )
