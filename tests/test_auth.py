"""First-run ownership, password migration, and credential replacement."""

import hashlib
import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from core import auth, passwords
from db import database


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="tindahan-auth-")
        self.addCleanup(self.temporary.cleanup)
        self.database_patch = patch.object(
            database, "DB_FILE", Path(self.temporary.name) / "pos.db"
        )
        self.database_patch.start()
        self.addCleanup(self.database_patch.stop)
        self.connections = []
        original_connect = sqlite3.connect

        def connect(*args, **kwargs):
            connection = original_connect(*args, **kwargs)
            self.connections.append(connection)
            return connection

        self.connect_patch = patch.object(
            database.sqlite3, "connect", side_effect=connect
        )
        self.connect_patch.start()
        self.addCleanup(self.connect_patch.stop)
        self.addCleanup(self.close_connections)
        database.init_database()

    def close_connections(self):
        for connection in self.connections:
            try:
                connection.close()
            except sqlite3.ProgrammingError:
                # Thread-owned connections are closed by their worker's context.
                pass

    def stored_password(self, username):
        with closing(database.get_connection()) as connection:
            return connection.execute(
                "SELECT password FROM users WHERE username = ?", (username,)
            ).fetchone()[0]

    def test_empty_database_has_no_default_account(self):
        self.assertTrue(auth.needs_initial_setup())
        self.assertEqual(auth.get_users(), [])
        database.init_database()
        self.assertEqual(auth.get_users(), [])

    def test_owner_is_created_with_admin_access_and_no_plaintext_secret(self):
        user = auth.create_initial_admin("  owner  ", "1234")
        self.assertEqual(user["username"], "owner")
        self.assertTrue(user["is_admin"])
        self.assertNotIn("password", user)
        self.assertFalse(auth.needs_initial_setup())
        self.assertEqual(auth.verify_user("owner", "1234"), user)
        self.assertIsNone(auth.verify_user("owner", "wrong password"))
        self.assertNotEqual(self.stored_password("owner"), "1234")

    def test_setup_rejects_invalid_username_and_password(self):
        for username, password in (
            (" ", "a long owner passphrase"),
            ("owner", "abc"),
            ("owner", " " * 20),
        ):
            with self.subTest(username=username), self.assertRaises(ValueError):
                auth.create_initial_admin(username, password)
        self.assertTrue(auth.needs_initial_setup())

    def test_setup_cannot_run_when_any_user_already_exists(self):
        auth.add_user("staff", "a staff passphrase", False)
        with self.assertRaisesRegex(ValueError, "already complete"):
            auth.create_initial_admin("owner", "a long owner passphrase")
        self.assertEqual([user["username"] for user in auth.get_users()], ["staff"])

    def test_two_instances_can_create_only_one_initial_owner(self):
        def create(index):
            try:
                return auth.create_initial_admin(
                    f"owner-{index}", "a long owner passphrase"
                )
            except ValueError:
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(create, range(2)))
        self.assertEqual(sum(user is not None for user in results), 1)
        self.assertEqual(len(auth.get_users()), 1)

    def test_equal_passwords_have_different_hashes(self):
        auth.add_user("first", "same long passphrase")
        auth.add_user("second", "same long passphrase")
        self.assertNotEqual(
            self.stored_password("first"), self.stored_password("second")
        )
        self.assertIsNotNone(auth.verify_user("first", "same long passphrase"))
        self.assertIsNotNone(auth.verify_user("second", "same long passphrase"))

    def test_duplicate_username_does_not_replace_existing_credentials(self):
        self.assertTrue(auth.add_user("owner", "original passphrase"))
        self.assertFalse(auth.add_user("owner", "replacement passphrase", True))
        self.assertIsNotNone(auth.verify_user("owner", "original passphrase"))
        self.assertIsNone(auth.verify_user("owner", "replacement passphrase"))

    def test_legacy_accounts_migrate_without_losing_identity_or_records(self):
        with closing(database.get_connection()) as connection, connection:
            connection.execute("DROP TABLE users")
            connection.execute(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, is_admin INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT (datetime('now')))"
            )
            connection.execute(
                "INSERT INTO users (id, username, password, is_admin) VALUES (7, 'owner', 'old-short', 1)"
            )
            connection.execute(
                "INSERT INTO products (name, barcode, stock) VALUES ('Existing stock', 'legacy-001', 17)"
            )
        database.init_database()
        user = auth.verify_user("owner", "old-short")
        self.assertEqual(user["id"], 7)
        self.assertTrue(user["is_admin"])
        self.assertFalse(user["must_change_password"])
        encoded = self.stored_password("owner")
        self.assertNotEqual(encoded, "old-short")
        database.init_database()
        self.assertEqual(self.stored_password("owner"), encoded)
        with closing(database.get_connection()) as connection:
            self.assertEqual(
                connection.execute(
                    "SELECT stock FROM products WHERE barcode='legacy-001'"
                ).fetchone()[0],
                17,
            )

    def test_retired_default_requires_change_after_migration(self):
        retired = "retired test credential"
        with closing(database.get_connection()) as connection, connection:
            connection.execute(
                "INSERT INTO users (username, password, is_admin) VALUES ('owner', ?, 1)",
                (retired,),
            )
        with patch.object(
            passwords,
            "RETIRED_PASSWORD_DIGEST",
            hashlib.sha256(retired.encode()).hexdigest(),
        ):
            database.init_database()
            self.assertTrue(auth.verify_user("owner", retired)["must_change_password"])
            self.assertFalse(auth.add_user("second", retired))
            self.assertFalse(auth.change_password("owner", retired, retired))
            self.assertTrue(
                auth.change_password("owner", retired, "a replacement passphrase")
            )
        self.assertIsNone(auth.verify_user("owner", retired))
        self.assertFalse(
            auth.verify_user("owner", "a replacement passphrase")[
                "must_change_password"
            ]
        )

    def test_password_change_needs_old_password_and_revokes_remembered_login(self):
        auth.create_initial_admin("owner", "original passphrase")
        database.set_setting("persistent_login_enabled", "1")
        database.set_setting("persistent_login_username", "owner")
        self.assertFalse(
            auth.change_password(
                "owner", "incorrect password", "replacement passphrase"
            )
        )
        self.assertTrue(
            auth.change_password(
                "owner", "original passphrase", "replacement passphrase"
            )
        )
        self.assertIsNone(auth.verify_user("owner", "original passphrase"))
        self.assertIsNotNone(auth.verify_user("owner", "replacement passphrase"))
        self.assertEqual(database.get_setting("persistent_login_enabled", "0"), "0")

    def test_spaces_and_unicode_in_passwords_are_preserved(self):
        password = "  tindahan café 密碼  "
        auth.create_initial_admin("owner", password)
        self.assertIsNotNone(auth.verify_user("owner", password))
        self.assertIsNone(auth.verify_user("owner", password.strip()))

    def test_malformed_hashes_do_not_authenticate(self):
        for encoded in (
            "plaintext",
            "pbkdf2_sha256$600000$wrong$hash",
            "pbkdf2_sha256$999999999$00$00",
        ):
            self.assertFalse(passwords.verify_password("a long passphrase", encoded))


if __name__ == "__main__":
    unittest.main()
