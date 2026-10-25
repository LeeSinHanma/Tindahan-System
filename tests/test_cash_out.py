"""Cash-out ledger rules; these checks do not require a graphical display."""

import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import date
from pathlib import Path
from unittest.mock import patch

from core import cash_out, inventory
from db import database


class CashOutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cash-out-test-")
        self.db_patch = patch.object(
            database, "DB_FILE", Path(self.temp.name) / "test.db"
        )
        self.db_patch.start()
        # Retain connections made by the existing database initializer until cleanup.
        self.connections = []
        original_connect = database.sqlite3.connect

        def connect(*args, **kwargs):
            connection = original_connect(*args, **kwargs)
            self.connections.append(connection)
            return connection

        self.connection_patch = patch.object(
            database.sqlite3, "connect", side_effect=connect
        )
        self.connection_patch.start()
        database.init_database()
        self.account_id = cash_out.save_account("GCash 1", "00123456789")

    def tearDown(self):
        for connection in self.connections:
            # Worker threads close their own connections through the core's closing context.
            try:
                connection.close()
            except database.sqlite3.ProgrammingError:
                continue
        self.connection_patch.stop()
        self.db_patch.stop()
        self.temp.cleanup()

    def record(self, **overrides):
        payload = dict(
            transferred_at="2026-10-24 09:15",
            receiving_account_id=self.account_id,
            sender_account="Juan · Maya · 09123456789",
            amount="1500",
            reference_last5="07890",
        )
        payload.update(overrides)
        return cash_out.create_transaction(**payload)

    def test_default_stacking_fees_and_boundaries(self):
        for amount, fee in [
            ("1", 500),
            ("499", 500),
            ("499.99", 500),
            ("500", 1000),
            ("750", 1000),
            ("999.99", 1000),
            ("1000", 1500),
            ("1001", 2000),
            ("1499.99", 2000),
            ("1500", 2500),
            ("1999.99", 2500),
            ("2000", 3000),
            ("2750", 4000),
        ]:
            with self.subTest(amount=amount):
                self.assertEqual(cash_out.calculate_fee(amount), fee)

    def test_decimal_validation(self):
        for value in (
            "",
            "no",
            "NaN",
            "Infinity",
            "-1",
            "0",
            "1.001",
            "1e9999999",
            "1e-9999999",
        ):
            with self.subTest(amount=value), self.assertRaises(ValueError):
                cash_out.calculate_fee(value)
        self.assertEqual(cash_out.money_to_cents("1,500.25"), 150025)

    def test_editable_rules_and_new_block_boundaries(self):
        cash_out.save_fee_rules("2000", "750", "30", "7", "12")
        for amount, fee in [
            (749, 700),
            (750, 1200),
            (2000, 3000),
            (2500, 3700),
            (2750, 4200),
        ]:
            self.assertEqual(cash_out.calculate_fee(amount), fee)
        for block, split in [(0, 500), (1000, 1000), (1000, 1500)]:
            with self.assertRaises(ValueError):
                cash_out.save_fee_rules(block, split, 15, 5, 10)

    def test_saved_custom_and_zero_fees_survive_rule_changes_and_restart(self):
        automatic = self.record()
        custom = self.record(reference_last5="00002", fee="12.50")
        free = self.record(reference_last5="00003", fee="0")
        cash_out.save_fee_rules(1000, 500, 20, 7, 12)
        database.init_database()
        self.assertEqual(cash_out.get_transaction(automatic)["fee_cents"], 2500)
        self.assertEqual(cash_out.get_transaction(custom)["fee_cents"], 1250)
        self.assertEqual(cash_out.get_transaction(custom)["suggested_fee_cents"], 2500)
        self.assertEqual(cash_out.get_transaction(free)["fee_cents"], 0)
        self.assertEqual(cash_out.calculate_fee(1500), 3200)

    def test_accounts_accept_custom_names_numbers_and_preserve_transfer_history(self):
        other = cash_out.save_account("GCash 2", "00987654321")
        bank = cash_out.save_account("My GoTyme account", "00012345678901234")
        self.assertNotEqual(other, self.account_id)
        self.assertEqual(len(cash_out.list_accounts()), 3)
        transaction_id = self.record()
        cash_out.save_account("GCash Main", "00000000001", self.account_id)
        row = cash_out.get_transaction(transaction_id)
        self.assertEqual(row["receiving_account_name"], "GCash 1")
        self.assertEqual(row["receiving_account_number"], "00123456789")
        self.assertTrue(any(a["id"] == bank for a in cash_out.list_accounts()))
        with self.assertRaises(ValueError):
            cash_out.save_account("gcash 2", "11111")
        with self.assertRaises(ValueError):
            cash_out.save_account(None, None)

    def test_duplicate_warning_includes_claimed_entries_and_can_be_acknowledged(self):
        first = self.record()
        cash_out.claim_transaction(first)
        with self.assertRaises(cash_out.DuplicateTransactionError) as caught:
            self.record(transferred_at="2026-10-24 18:30", fee=40)
        self.assertEqual(caught.exception.matches[0]["id"], first)
        self.assertEqual(caught.exception.matches[0]["status"], "claimed")
        self.assertEqual(len(cash_out.list_transactions()), 1)
        second = self.record(allow_duplicate=True)
        self.assertNotEqual(first, second)
        self.assertEqual(cash_out.get_transaction(second)["status"], "unclaimed")

    def test_repeated_reference_is_allowed_for_other_accounts_amounts_and_dates(self):
        self.record()
        other = cash_out.save_account("BDO", "00000001")
        self.record(receiving_account_id=other)
        self.record(amount=2000)
        self.record(transferred_at="2026-10-25 09:15")
        self.assertEqual(len(cash_out.list_transactions("7890")), 4)

    def test_partial_search_leading_zeros_and_all_history(self):
        first = self.record(reference_last5="00079", transferred_at="2020-01-01 10:00")
        self.record(reference_last5="17890")
        cash_out.claim_transaction(first)
        self.assertEqual(
            cash_out.list_transactions("0007")[0]["reference_last5"], "00079"
        )
        self.assertEqual(
            cash_out.list_transactions("7890")[0]["reference_last5"], "17890"
        )
        self.assertEqual(len(cash_out.list_transactions(status="claimed")), 1)
        self.assertEqual(cash_out.list_transactions("99999"), [])
        for reference in ("1234", "123456", "12abc", "１２３４５"):
            with self.assertRaises(ValueError):
                self.record(reference_last5=reference)
        with self.assertRaises(ValueError):
            cash_out.list_transactions("7%")

    def test_claim_is_persistent_and_cannot_be_repeated(self):
        transaction_id = self.record()
        cash_out.claim_transaction(transaction_id)
        row = cash_out.get_transaction(transaction_id)
        self.assertEqual(row["status"], "claimed")
        self.assertIsNotNone(row["claimed_at"])
        with self.assertRaisesRegex(ValueError, "already claimed"):
            cash_out.claim_transaction(transaction_id)

    def test_concurrent_claims_allow_only_one_handover(self):
        transaction_id = self.record()

        def claim():
            try:
                cash_out.claim_transaction(transaction_id)
                return True
            except ValueError:
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: claim(), range(2)))
        self.assertEqual(sorted(results), [False, True])

    def test_invalid_transfer_values_do_not_create_records(self):
        for override in [
            dict(sender_account=""),
            dict(sender_account=None),
            dict(receiving_account_id=12345),
            dict(transferred_at="2026-02-30 15:00"),
            dict(fee="-5"),
            dict(fee="0.001"),
        ]:
            with self.subTest(override=override), self.assertRaises(ValueError):
                self.record(**override)
        self.assertEqual(cash_out.list_transactions(), [])

    def test_service_fees_never_change_product_sales_or_stock(self):
        product_id = inventory.create_product(
            dict(
                name="Coffee",
                barcode="101",
                original_price=8,
                sell_price=10,
                stock=30,
                stock_tracked=True,
            )
        )
        initial_summary = database.get_sales_summary(1)
        transaction_id = self.record(fee=100)
        cash_out.claim_transaction(transaction_id)
        self.assertEqual(database.get_sales_summary(1), initial_summary)
        self.assertEqual(inventory.get_product_by_id(product_id)["stock"], 30)
        with closing(database.get_connection()) as conn:
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0], 0
            )
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM sale_items").fetchone()[0], 0
            )

    def test_fee_totals_use_calendar_periods_and_preserve_custom_fees(self):
        # Saturday: week starts Monday Oct 19; exclude later dates, even this month.
        entries = [
            ("2025-12-31 23:59:59", "100", False),
            ("2026-01-01 00:00:00", "1", False),
            ("2026-09-30 23:59:59", "2", False),
            ("2026-10-01 00:00:00", "3", False),
            ("2026-10-18 23:59:59", "4", False),
            ("2026-10-19 00:00:00", "5", False),
            ("2026-10-23 23:59:59", "6", False),
            ("2026-10-24 00:00:00", "7.25", True),
            ("2026-10-24 23:59:59", "8.50", False),
            ("2026-10-24 12:30:00", "0", False),
            ("2026-10-25 00:00:00", "200", False),
        ]
        for index, (timestamp, fee, claimed) in enumerate(entries):
            transaction_id = self.record(
                transferred_at=timestamp, reference_last5=f"{index:05d}", fee=fee
            )
            if claimed:
                cash_out.claim_transaction(transaction_id)
        cash_out.save_fee_rules(1000, 500, 50, 30, 40)
        totals = cash_out.get_fee_totals(date(2026, 10, 24))
        self.assertEqual(totals["day"]["total_fee_cents"], 1575)
        self.assertEqual(totals["day"]["claimed_fee_cents"], 725)
        self.assertEqual(totals["day"]["unclaimed_fee_cents"], 850)
        self.assertEqual(totals["day"]["transaction_count"], 3)
        self.assertEqual(totals["week"]["total_fee_cents"], 2675)
        self.assertEqual(totals["month"]["total_fee_cents"], 3375)
        self.assertEqual(totals["year"]["total_fee_cents"], 3675)
        self.assertEqual(totals["week"]["start_date"], "2026-10-19")

    def test_fee_totals_are_zero_without_matching_records(self):
        self.record(transferred_at="2025-12-31 12:30")
        totals = cash_out.get_fee_totals(date(2026, 10, 24))
        for period in totals.values():
            self.assertEqual(period["total_fee_cents"], 0)
            self.assertEqual(period["claimed_fee_cents"], 0)
            self.assertEqual(period["unclaimed_fee_cents"], 0)
            self.assertEqual(period["transaction_count"], 0)

    def test_fee_totals_week_can_cross_the_calendar_year(self):
        self.record(
            transferred_at="2025-12-28 23:59:59", reference_last5="00001", fee=100
        )
        self.record(
            transferred_at="2025-12-29 00:00:00", reference_last5="00002", fee=5
        )
        self.record(
            transferred_at="2026-01-01 00:00:00", reference_last5="00003", fee=10
        )
        self.record(
            transferred_at="2026-01-02 00:00:00", reference_last5="00004", fee=200
        )
        totals = cash_out.get_fee_totals(date(2026, 1, 1))
        self.assertEqual(totals["week"]["start_date"], "2025-12-29")
        self.assertEqual(totals["week"]["total_fee_cents"], 1500)
        self.assertEqual(totals["month"]["total_fee_cents"], 1000)
        self.assertEqual(totals["year"]["total_fee_cents"], 1000)

    def test_fee_totals_include_leap_day_and_all_accounts(self):
        other = cash_out.save_account("Maya", "00987654321")
        self.record(
            transferred_at="2024-02-29 23:59:59", reference_last5="00001", fee=5
        )
        self.record(
            transferred_at="2024-03-01 00:00:00",
            reference_last5="00002",
            fee=10,
            receiving_account_id=other,
        )
        self.record(
            transferred_at="2024-03-02 00:00:00", reference_last5="00003", fee=100
        )
        totals = cash_out.get_fee_totals(date(2024, 3, 1))
        self.assertEqual(totals["day"]["total_fee_cents"], 1000)
        self.assertEqual(totals["week"]["total_fee_cents"], 1500)
        self.assertEqual(totals["month"]["total_fee_cents"], 1000)
        self.assertEqual(totals["year"]["total_fee_cents"], 1500)

    def test_cash_in_shares_accounts_rules_and_type_specific_duplicate_protection(self):
        outgoing = self.record()
        incoming = self.record(transaction_type="cash_in")
        self.assertEqual(
            cash_out.get_transaction(outgoing)["transaction_type"], "cash_out"
        )
        self.assertEqual(
            cash_out.get_transaction(incoming)["transaction_type"], "cash_in"
        )
        self.assertEqual(cash_out.get_transaction(incoming)["fee_cents"], 2500)
        self.assertEqual(len(cash_out.list_accounts()), 1)
        with self.assertRaises(cash_out.DuplicateTransactionError):
            self.record(transaction_type="cash_in")
        self.assertEqual(
            len(cash_out.list_transactions("7890", transaction_type="cash_in")), 1
        )
        self.assertEqual(
            len(cash_out.list_transactions("7890", transaction_type="cash_out")), 1
        )
        cash_out.complete_transaction(incoming)
        with self.assertRaisesRegex(ValueError, "already completed"):
            cash_out.complete_transaction(incoming)
        cash_out.save_fee_rules(1000, 500, 20, 7, 12)
        new_incoming = self.record(transaction_type="cash_in", reference_last5="12345")
        self.assertEqual(cash_out.get_transaction(new_incoming)["fee_cents"], 3200)

    def test_combined_fee_totals_keep_both_service_types_and_statuses(self):
        for index, (service, fee, completed) in enumerate(
            [
                ("cash_in", 5, True),
                ("cash_out", 10, True),
                ("cash_in", 15, False),
                ("cash_out", 20, False),
            ]
        ):
            transaction_id = self.record(
                transaction_type=service, reference_last5=f"{index:05d}", fee=fee
            )
            if completed:
                cash_out.complete_transaction(transaction_id)
        today = date(2026, 10, 24)
        for totals in cash_out.get_fee_totals(today).values():
            self.assertEqual(totals["total_fee_cents"], 5000)
            self.assertEqual(totals["claimed_fee_cents"], 1500)
            self.assertEqual(totals["unclaimed_fee_cents"], 3500)
            self.assertEqual(totals["cash_in_fee_cents"], 2000)
            self.assertEqual(totals["cash_out_fee_cents"], 3000)
        incoming = cash_out.get_fee_totals(today, transaction_type="cash_in")["day"]
        self.assertEqual(incoming["total_fee_cents"], 2000)
        self.assertEqual(incoming["transaction_count"], 2)
        self.assertEqual(incoming["cash_out_fee_cents"], 0)

    def test_invalid_service_type_is_rejected(self):
        with self.assertRaises(ValueError):
            self.record(transaction_type="other")
        with self.assertRaises(ValueError):
            cash_out.list_transactions(transaction_type="other")
        with self.assertRaises(ValueError):
            cash_out.get_fee_totals(transaction_type="other")

    def test_existing_cash_out_database_migrates_without_changing_its_records(self):
        legacy_path = Path(self.temp.name) / "legacy.db"
        with patch.object(database, "DB_FILE", legacy_path):
            with closing(database.get_connection()) as conn, conn:
                conn.executescript("""
                    CREATE TABLE cash_out_accounts (id INTEGER PRIMARY KEY, name TEXT NOT NULL COLLATE NOCASE UNIQUE, account_number TEXT NOT NULL);
                    INSERT INTO cash_out_accounts VALUES (1, 'GCash old', '00123456789');
                    CREATE TABLE cash_out_transactions (
                        id INTEGER PRIMARY KEY, transferred_at TEXT NOT NULL,
                        receiving_account_id INTEGER NOT NULL, receiving_account_name TEXT NOT NULL,
                        receiving_account_number TEXT NOT NULL, sender_account TEXT NOT NULL,
                        amount_cents INTEGER NOT NULL, fee_cents INTEGER NOT NULL,
                        suggested_fee_cents INTEGER NOT NULL, reference_last5 TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'unclaimed', created_at TEXT NOT NULL, claimed_at TEXT
                    );
                    INSERT INTO cash_out_transactions VALUES
                        (47, '2026-10-24 09:15:00', 1, 'GCash old', '00123456789', 'Customer wallet',
                         150000, 777, 2500, '00079', 'claimed', '2026-10-24 09:15:00', '2026-10-24 09:30:00');
                """)
            database.init_database()
            row = cash_out.get_transaction(47)
            self.assertEqual(row["transaction_type"], "cash_out")
            self.assertEqual(row["reference_last5"], "00079")
            self.assertEqual(row["fee_cents"], 777)
            self.assertEqual(row["claimed_at"], "2026-10-24 09:30:00")
            incoming = self.record(transaction_type="cash_in", reference_last5="00079")
            database.init_database()
            self.assertEqual(
                cash_out.get_transaction(incoming)["transaction_type"], "cash_in"
            )
            self.assertEqual(cash_out.get_transaction(47), row)


if __name__ == "__main__":
    unittest.main()
