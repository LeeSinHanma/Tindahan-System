"""Desktop regression checks. Run with a working Tk display and a temporary database."""

import tempfile
import tkinter as tk
import traceback
import unittest
import wave
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import ttk
from unittest.mock import patch

from core import auth, cash_out, checkout_audio, debt_tracker, inventory, shopping_list
from db import database
from ui.app import App
from ui.widgets import DataTable


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


class DesktopTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"A Tk display is required: {exc}")
        self.root.overrideredirect(True)
        self.root.geometry("1024x768+2000+0")
        self.temp = tempfile.TemporaryDirectory(prefix="tindahan-ui-test-")
        self.db_patch = patch.object(
            database, "DB_FILE", Path(self.temp.name) / "test.db"
        )
        self.db_patch.start()
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
        self.errors = []
        self.root.report_callback_exception = lambda kind, value, tb: (
            self.errors.append("".join(traceback.format_exception(kind, value, tb)))
        )
        self.app = App(self.root)
        self.root.geometry("1024x768+2000+0")
        auth.add_user("tester", "test-password", True)
        self.app.frames["login"].clear_fields()
        self.ids = []
        for name, barcode, cost, price, stock, tracked in [
            ("Coffee", "1001", 8, 10, 30, True),
            ("Rice", "1002", 40, 50, 50, False),
            ("Low stock", "1003", 16, 20, 3, True),
            ("Out of stock", "1004", 20, 25, 0, True),
        ]:
            self.ids.append(
                inventory.create_product(
                    dict(
                        name=name,
                        barcode=barcode,
                        original_price=cost,
                        sell_price=price,
                        stock=stock,
                        stock_tracked=tracked,
                    )
                )
            )
        self.pump()

    def tearDown(self):
        if hasattr(self, "app"):
            for timer in self.root.tk.call("after", "info"):
                # Let each widget delete its own registered callback during destruction.
                self.root.tk.call("after", "cancel", timer)
            self.root.destroy()
            for connection in self.connections:
                connection.close()
            self.connection_patch.stop()
            self.db_patch.stop()
            self.temp.cleanup()
            self.assertEqual(self.errors, [], "\n".join(self.errors))

    def pump(self):
        for _ in range(3):
            self.root.update_idletasks()
            self.root.update()

    def sign_in(self):
        login = self.app.frames["login"]
        login.username_var.set("tester")
        login.password_var.set("test-password")
        login._submit()
        self.pump()

    def button(self, parent, text):
        return next(
            w
            for w in descendants(parent)
            if isinstance(w, ttk.Button) and w.cget("text") == text
        )

    def modal(self):
        return next(w for w in descendants(self.root) if isinstance(w, tk.Toplevel))

    def assert_inside(self, widget):
        self.assertTrue(widget.winfo_ismapped(), str(widget))
        x = widget.winfo_rootx() - self.root.winfo_rootx()
        y = widget.winfo_rooty() - self.root.winfo_rooty()
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLessEqual(x + widget.winfo_width(), self.root.winfo_width())
        self.assertLessEqual(y + widget.winfo_height(), self.root.winfo_height())

    def run_blocking_dialog(self, open_dialog, callback):
        failures = []

        def interact():
            try:
                callback(self.modal())
            except Exception as exc:
                failures.append(exc)
            finally:
                for widget in list(descendants(self.root)):
                    if isinstance(widget, tk.Toplevel) and widget.winfo_exists():
                        widget.destroy()

        self.root.after(150, interact)
        open_dialog()
        if failures:
            raise failures[0]

    def test_sign_in_sign_out_and_staff_navigation(self):
        self.assertFalse(self.app.sidebar.winfo_ismapped())
        self.sign_in()
        self.assertEqual(self.app.active_screen, "dashboard")
        self.assertIn("users", self.app.frames)
        self.assertTrue(self.app.sidebar.winfo_ismapped())
        with patch("ui.app.messagebox.askyesno", return_value=True):
            self.app._handle_logout()
        self.pump()
        self.assertEqual(self.app.active_screen, "login")
        self.assertFalse(self.app.sidebar.winfo_ismapped())
        auth.add_user("staff", "staff-password", False)
        self.app._on_login_success(auth.get_user_by_username("staff"))
        self.assertNotIn("users", self.app.nav_buttons)
        self.assertNotIn("users", self.app.frames)

    def test_layout_and_navigation_survive_resizing(self):
        self.sign_in()
        for width, height in [
            (1920, 1000),
            (1366, 768),
            (1024, 768),
            (960, 640),
            (1366, 768),
        ]:
            self.root.geometry(f"{width}x{height}+2000+0")
            for screen in (
                "dashboard",
                "pos",
                "cash_out",
                "inventory",
                "shopping_list",
                "debt_tracker",
                "finance",
                "account",
                "users",
            ):
                with self.subTest(size=(width, height), screen=screen):
                    self.app._show_screen(screen)
                    self.pump()
                    self.assert_inside(self.app.logout_btn)
                    frame = self.app.frames[screen]
                    for widget in descendants(frame):
                        if (
                            isinstance(
                                widget,
                                (ttk.Button, ttk.Entry, ttk.Combobox, ttk.Menubutton),
                            )
                            and widget.winfo_ismapped()
                        ):
                            self.assert_inside(widget)
                    if screen == "pos":
                        self.assert_inside(frame.checkout_button)
                        self.assert_inside(frame.qty_entry)
                        frame._toggle_catalog()
                        self.pump()
                        self.assert_inside(frame.search_entry)
                        self.assert_inside(frame.checkout_button)
                        frame.workspace.show(frame.cart_panel)
                    elif screen == "debt_tracker":
                        frame.panels.show(frame.detail_panel)
                        self.pump()
                        self.assert_inside(frame.pay_button)
        self.app._toggle_sidebar()
        self.pump()
        self.assertEqual(self.app.sidebar.winfo_width(), 76)
        self.assert_inside(self.app.logout_btn)
        self.app._toggle_sidebar()
        self.pump()
        self.assertEqual(self.app.sidebar.winfo_width(), 220)

    def test_inventory_filters_and_legacy_untracked_navigation(self):
        self.sign_in()
        self.app._show_screen("inventory")
        frame = self.app.frames["inventory"]
        for label, expected in [
            ("All products", 4),
            ("Low stock", 1),
            ("Out of stock", 1),
            ("Untracked", 1),
        ]:
            frame.filter_var.set(label)
            frame._apply_filter()
            self.assertEqual(len(frame.product_table.get_children()), expected)
        self.app._show_screen("untracked")
        self.assertEqual(self.app.active_screen, "inventory")
        self.assertEqual(frame.filter_var.get(), "Untracked")

    def test_remembered_login_accepts_the_stored_numeric_setting(self):
        database.set_setting("persistent_login_enabled", "1")
        database.set_setting("persistent_login_username", "tester")
        self.app._attempt_persistent_login()
        self.assertEqual(self.app.active_screen, "dashboard")
        self.assertEqual(self.app.current_user["username"], "tester")

    def test_first_run_creates_owner_only_after_matching_valid_passwords(self):
        with database.get_connection() as connection:
            connection.execute("DELETE FROM users")
        login = self.app.frames["login"]
        login.clear_fields()
        self.pump()
        self.assertEqual(login.mode, "setup")
        self.root.geometry("960x640+2000+0")
        self.pump()
        self.assert_inside(login.signin_button)
        self.assert_inside(self.button(login, "Close application"))
        login.username_var.set("store-owner")
        login.password_var.set("a long owner passphrase")
        login.confirm_var.set("different passphrase")
        login._submit()
        self.assertTrue(auth.needs_initial_setup())
        self.assertIn("do not match", login.error_var.get())
        self.pump()
        close_button = self.button(login, "Close application")
        self.assertLessEqual(
            close_button.winfo_rooty() + close_button.winfo_height(),
            login.winfo_rooty() + login.winfo_height(),
        )
        login.confirm_var.set("a long owner passphrase")
        login._submit()
        self.pump()
        self.assertEqual(self.app.active_screen, "dashboard")
        self.assertTrue(self.app.current_user["is_admin"])
        self.assertEqual(self.app.current_user["username"], "store-owner")
        with patch("ui.app.messagebox.askyesno", return_value=True):
            self.app._handle_logout()
        self.assertEqual(login.mode, "login")
        self.assertEqual(login.password_var.get(), "")
        self.assertEqual(login.confirm_var.get(), "")

    def test_stale_setup_window_cannot_create_another_admin(self):
        login = self.app.frames["login"]
        login._set_mode("setup")
        login.username_var.set("unexpected-admin")
        login.password_var.set("another long passphrase")
        login.confirm_var.set("another long passphrase")
        login._submit()
        self.assertEqual(login.mode, "login")
        self.assertIsNone(auth.get_user_by_username("unexpected-admin"))
        self.assertIsNone(self.app.current_user)

    def test_default_password_change_blocks_workspace_and_remembered_login(self):
        with database.get_connection() as connection:
            connection.execute(
                "UPDATE users SET must_change_password = 1 WHERE username = 'tester'"
            )
        database.set_setting("persistent_login_enabled", "1")
        database.set_setting("persistent_login_username", "tester")
        self.app._attempt_persistent_login()
        self.assertIsNone(self.app.current_user)
        self.app._on_login_success(auth.get_user_by_username("tester"))
        self.assertIsNone(self.app.current_user)
        login = self.app.frames["login"]
        login.keep_signed_in_var.set(True)
        login.username_var.set("tester")
        login.password_var.set("test-password")
        login._submit()
        self.pump()
        self.assertEqual(login.mode, "password_change")
        self.assertIsNone(self.app.current_user)
        self.assertEqual(int(database.get_setting("persistent_login_enabled")), 0)
        self.root.geometry("960x640+2000+0")
        self.pump()
        self.assert_inside(login.signin_button)
        self.assert_inside(self.button(login, "Close application"))
        login.password_var.set("abc")
        login.confirm_var.set("abc")
        login._submit()
        self.assertIn("4 characters", login.error_var.get())
        self.pump()
        close_button = self.button(login, "Close application")
        self.assertLessEqual(
            close_button.winfo_rooty() + close_button.winfo_height(),
            login.winfo_rooty() + login.winfo_height(),
        )
        self.assertIsNone(self.app.current_user)
        login.password_var.set("a replacement passphrase")
        login.confirm_var.set("a replacement passphrase")
        login._submit()
        self.assertEqual(self.app.active_screen, "dashboard")
        self.assertIsNone(auth.verify_user("tester", "test-password"))
        self.assertFalse(self.app.current_user["must_change_password"])
        self.assertEqual(login.password_var.get(), "")
        self.assertIsNone(login._pending_credentials)

    def test_login_preserves_password_spaces(self):
        self.assertTrue(auth.add_user("spaces", "  a spaced passphrase  "))
        login = self.app.frames["login"]
        login.username_var.set("spaces")
        login.password_var.set("  a spaced passphrase  ")
        login._submit()
        self.assertEqual(self.app.current_user["username"], "spaces")

    def test_product_editor_validation_create_and_update(self):
        self.sign_in()
        self.app._show_screen("inventory")
        frame = self.app.frames["inventory"]
        frame._open_create_modal()
        modal = self.modal()
        self.pump()
        save = self.button(modal, "Add product")
        save.invoke()
        self.assertTrue(modal.winfo_exists())
        for key, value in dict(
            name="New product",
            barcode="9999",
            original_price="12",
            sell_price="15",
            stock="8",
            stock_tracked=True,
        ).items():
            frame._create_vars[key].set(value)
        save.invoke()
        product = inventory.get_product_by_barcode("9999")
        self.assertEqual(product["stock"], 8)
        frame.product_table.selection_set(str(product["id"]))
        frame._on_row_select()
        frame._open_update_modal()
        frame._update_vars["sell_price"].set("18")
        self.button(self.modal(), "Save changes").invoke()
        self.assertEqual(inventory.get_product_by_id(product["id"])["sell_price"], 18)

    def test_settings_save_quick_access_and_zero_threshold(self):
        self.sign_in()
        frame = self.app.frames["inventory"]
        frame._open_settings_modal()
        modal = self.modal()
        tree = next(w for w in descendants(modal) if isinstance(w, DataTable))
        tree.selection_set(str(self.ids[0]))
        self.button(modal, "Toggle quick access").invoke()
        entry = next(w for w in descendants(modal) if isinstance(w, ttk.Entry))
        entry.delete(0, "end")
        entry.insert(0, "0")
        self.button(modal, "Save settings").invoke()
        self.assertEqual(inventory.get_low_stock_threshold(), 0)
        self.assertEqual(inventory.get_quick_access_product_ids(), [self.ids[0]])

    def test_pos_search_quantity_and_checkout(self):
        self.sign_in()
        self.app._show_screen("pos")
        pos = self.app.frames["pos"]
        pos.search_var.set("Coffee")
        pos._search_products()
        pos.search_table.selection_set(str(self.ids[0]))
        pos._add_selected_search_product()
        pos.cart_table.selection_set(str(self.ids[0]))
        pos._on_table_select(None)
        pos.qty_var.set("2")
        pos._set_selected_quantity()
        self.assertEqual(pos.cart.get_total(), 20)
        self.assertFalse(pos.checkout_button.instate(["disabled"]))

        def pay(modal):
            entries = [w for w in descendants(modal) if isinstance(w, ttk.Entry)]
            entries[-1].insert(0, "100")
            self.button(modal, "Complete sale").invoke()

        self.run_blocking_dialog(pos._checkout, pay)
        self.assertEqual(pos.cart.get_total(), 0)
        self.assertEqual(inventory.get_product_by_id(self.ids[0])["stock"], 28)
        self.assertEqual(database.get_sales_summary(1)["total_sales"], 20)
        self.assertTrue(pos.checkout_button.instate(["disabled"]))

    def test_quick_access_adds_to_cart(self):
        self.sign_in()
        inventory.set_quick_access_product_ids([self.ids[0]])
        pos = self.app.frames["pos"]

        def add(modal):
            tree = next(w for w in descendants(modal) if isinstance(w, DataTable))
            tree.selection_set(str(self.ids[0]))
            tree.event_generate("<<TreeviewSelect>>")
            self.pump()
            self.button(modal, "Add to cart").invoke()
            self.button(modal, "Done").invoke()

        self.run_blocking_dialog(pos._open_quick_access_modal, add)
        self.assertEqual(pos.cart.get_total(), 10)

    def test_checkout_sound_choose_preview_mute_and_remove(self):
        self.sign_in()
        self.app._show_screen("pos")
        pos = self.app.frames["pos"]
        source = Path(self.temp.name) / "my sound.wav"
        with wave.open(str(source), "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(22050)
            output.writeframes(b"\x00\x00\x10\x00" * 2205)
        with (
            patch.object(
                checkout_audio,
                "user_data_directory",
                return_value=Path(self.temp.name) / "sounds data",
            ),
            patch.dict(
                "os.environ",
                {"SDL_AUDIODRIVER": "dummy", "PYGAME_HIDE_SUPPORT_PROMPT": "1"},
            ),
        ):
            pos._open_sound_settings()
            modal = self.modal()
            self.pump()
            self.assertTrue(self.button(modal, "Preview").instate(["disabled"]))
            with patch(
                "ui.pos_ui.filedialog.askopenfilename", return_value=str(source)
            ):
                self.button(modal, "Choose file").invoke()
            self.assertTrue(checkout_audio.sound_info()["enabled"])
            self.button(modal, "Preview").invoke()
            mute = next(w for w in descendants(modal) if isinstance(w, ttk.Checkbutton))
            mute.invoke()
            self.assertFalse(checkout_audio.sound_info()["enabled"])
            self.button(modal, "Remove").invoke()
            self.assertTrue(source.exists())
            self.assertFalse(checkout_audio.sound_info()["available"])
            self.button(modal, "Done").invoke()
            self.assertFalse(modal.winfo_exists())

    def test_restock_dialog_updates_the_selected_product(self):
        self.sign_in()
        frame = self.app.frames["inventory"]
        frame._open_restock_modal()
        modal = self.modal()
        entries = [w for w in descendants(modal) if isinstance(w, ttk.Entry)]
        entries[0].insert(0, "1001")
        self.button(modal, "Search").invoke()
        entries[1].delete(0, "end")
        entries[1].insert(0, "5")
        with patch("ui.inventory_ui.messagebox.askyesno", return_value=True):
            self.button(modal, "Restock").invoke()
        self.assertEqual(inventory.get_product_by_id(self.ids[0])["stock"], 35)
        modal.destroy()

    def test_restock_name_search_lists_matches_and_changes_only_the_selected_item(self):
        self.sign_in()
        dark = inventory.create_product(
            dict(
                name="Coffee Dark Roast",
                barcode="1005",
                original_price=8,
                sell_price=10,
                stock=8,
                stock_tracked=True,
            )
        )
        milk = inventory.create_product(
            dict(
                name="Coffee with Milk",
                barcode="1006",
                original_price=10,
                sell_price=12,
                stock=11,
                stock_tracked=True,
            )
        )
        self.app.frames["inventory"]._open_restock_modal()
        modal = self.modal()
        entries = [w for w in descendants(modal) if isinstance(w, ttk.Entry)]
        results = next(w for w in descendants(modal) if isinstance(w, DataTable))
        entries[0].insert(0, "coFF")
        self.button(modal, "Search").invoke()
        self.assertEqual(
            set(results.get_children()), {str(self.ids[0]), str(dark), str(milk)}
        )
        self.assertTrue(self.button(modal, "Restock").instate(["disabled"]))
        results.selection_set(str(milk))
        results.event_generate("<<TreeviewSelect>>")
        self.pump()
        entries[1].delete(0, "end")
        entries[1].insert(0, "7")
        with patch("ui.inventory_ui.messagebox.askyesno", return_value=True):
            self.button(modal, "Restock").invoke()
        self.assertEqual(inventory.get_product_by_id(milk)["stock"], 18)
        self.assertEqual(inventory.get_product_by_id(dark)["stock"], 8)
        self.assertEqual(inventory.get_product_by_id(self.ids[0])["stock"], 30)
        self.assertEqual(results.set(str(milk), "stock"), "18")
        self.assertTrue(self.button(modal, "Restock").instate(["disabled"]))
        modal.destroy()

    def test_restock_search_edit_and_no_matches_clear_the_previous_selection(self):
        self.sign_in()
        self.app.frames["inventory"]._open_restock_modal()
        modal = self.modal()
        query = next(w for w in descendants(modal) if isinstance(w, ttk.Entry))
        results = next(w for w in descendants(modal) if isinstance(w, DataTable))
        query.insert(0, "1001")
        self.button(modal, "Search").invoke()
        self.assertFalse(self.button(modal, "Restock").instate(["disabled"]))
        query.delete(0, "end")
        query.insert(0, "Nonexistent product")
        self.assertTrue(self.button(modal, "Restock").instate(["disabled"]))
        self.button(modal, "Search").invoke()
        self.assertEqual(results.get_children(), ())
        self.assertIn("No matching products", results.empty_text)
        self.button(modal, "Restock").invoke()
        self.assertEqual(inventory.get_product_by_id(self.ids[0])["stock"], 30)
        modal.destroy()

    def test_restock_live_name_search_and_invalid_quantity_leave_stock_unchanged(self):
        self.sign_in()
        self.app.frames["inventory"]._open_restock_modal()
        modal = self.modal()
        entries = [w for w in descendants(modal) if isinstance(w, ttk.Entry)]
        results = next(w for w in descendants(modal) if isinstance(w, DataTable))
        entries[0].insert(0, "Coffee")
        self.root.after(240, self.root.quit)
        self.root.mainloop()
        self.assertEqual(results.get_children(), (str(self.ids[0]),))
        results.selection_set(str(self.ids[0]))
        results.event_generate("<<TreeviewSelect>>")
        self.pump()
        entries[1].delete(0, "end")
        entries[1].insert(0, "0")
        with patch("ui.inventory_ui.messagebox.askyesno") as confirm:
            self.button(modal, "Restock").invoke()
        confirm.assert_not_called()
        self.assertEqual(inventory.get_product_by_id(self.ids[0])["stock"], 30)
        entries[0].insert("end", " another query")
        modal.destroy()
        self.root.after(240, self.root.quit)
        self.root.mainloop()

    def test_charge_to_customer_keeps_checkout_stock_and_debt_in_sync(self):
        self.sign_in()
        debt_tracker.add_customer("Maria")
        pos = self.app.frames["pos"]
        pos._add_product_to_cart(inventory.get_product_by_id(self.ids[0]))

        def charge(modal):
            customers = next(w for w in descendants(modal) if isinstance(w, DataTable))
            customers.selection_set(customers.get_children()[0])
            customers.event_generate("<<TreeviewSelect>>")
            self.pump()
            self.button(modal, "Submit as Debt").invoke()

        self.run_blocking_dialog(pos._checkout_debt, charge)
        self.assertEqual(debt_tracker.get_customer_total_debt("Maria"), 10)
        self.assertEqual(inventory.get_product_by_id(self.ids[0])["stock"], 29)
        self.assertEqual(pos.cart.get_items(), [])

    def test_pdf_exports_still_work_with_inventory_and_list_data(self):
        shopping_list.add_item(self.ids[0], "3")
        for name, export in [
            ("inventory.pdf", inventory.save_pdf),
            ("shopping.pdf", shopping_list.save_pdf),
        ]:
            path = Path(self.temp.name) / name
            export(str(path))
            self.assertTrue(path.read_bytes().startswith(b"%PDF"))

    def test_shopping_list_add_and_mark_purchased(self):
        self.sign_in()
        frame = self.app.frames["shopping_list"]
        frame.refresh()
        frame.product_table.selection_set(f"p{self.ids[0]}")
        frame._on_product_select(None)
        frame.qty_var.set("3")
        frame._add_checked_to_list()
        item = shopping_list.list_items()[0]
        self.assertEqual(item["quantity"], 3)
        frame.checked_list_item_ids = {item["id"]}
        frame._mark_selected_done(True)
        self.assertTrue(shopping_list.list_items()[0]["is_done"])

    def test_customer_payment_updates_balance_and_buttons(self):
        self.sign_in()
        debt_tracker.add_customer("Maria")
        debt_tracker.add_debt("Maria", 100, "Groceries")
        frame = self.app.frames["debt_tracker"]
        frame.refresh()
        frame.customer_table.selection_set(frame.customer_table.get_children()[0])
        frame._on_customer_select(None)
        frame.pay_amount_var.set("30")
        self.assertFalse(frame.pay_button.instate(["disabled"]))
        with patch("ui.debt_tracker_ui.messagebox.askyesno", return_value=True):
            frame._pay_amount_for_customer()
        self.assertEqual(debt_tracker.get_customer_total_debt("Maria"), 70)
        self.assertTrue(frame.pay_button.instate(["disabled"]))

    def test_finance_period_totals_do_not_duplicate_multi_item_sales(self):
        now = datetime.now()
        with database.get_connection() as conn:
            for date, total in [(now, 100), (now - timedelta(days=5), 50)]:
                sale_id = conn.execute(
                    "INSERT INTO sales (date,total) VALUES (?,?)",
                    (date.isoformat(" "), total),
                ).lastrowid
                for product_id, quantity, price in [
                    (self.ids[0], 2, 10),
                    (self.ids[1], 1, 50),
                ]:
                    conn.execute(
                        "INSERT INTO sale_items (sale_id,product_id,quantity,price) VALUES (?,?,?,?)",
                        (sale_id, product_id, quantity, price),
                    )
        finance = self.app.frames["finance"]
        finance.refresh()
        self.assertEqual(finance.metrics["sales"].cget("text"), "PHP 100.00")
        self.assertEqual(finance.metrics["profit"].cget("text"), "PHP 44.00")
        finance.period_var.set("Last 7 days")
        finance.refresh()
        self.assertEqual(finance.metrics["sales"].cget("text"), "PHP 150.00")
        self.assertEqual(len(finance.details_table.get_children()), 2)

    def test_numeric_table_sort_preserves_ids_and_selection(self):
        self.app.frames["inventory"].refresh_products()
        tree = self.app.frames["inventory"].product_table
        tree.sort_column("sell_price")
        values = [float(tree.set(item, "sell_price")) for item in tree.get_children()]
        self.assertEqual(values, sorted(values))
        tree.selection_set(str(self.ids[0]))
        tree.sort_column("sell_price", reverse=True)
        self.assertEqual(tree.selection(), (str(self.ids[0]),))
        self.assertEqual(set(tree.get_children()), {str(i) for i in self.ids})

    def cash_out_form(self):
        self.sign_in()
        self.app._show_screen("cash_out")
        frame = self.app.frames["cash_out"]
        account_id = cash_out.save_account("GCash 1", "00123456789")
        frame._open_transfer()
        fields = frame.transfer_vars
        fields["sender"].set("Juan · Maya · 09123456789")
        fields["date"].set("2026-10-24")
        fields["time"].set("10:15")
        fields["reference"].set("07890")
        return frame, account_id, self.modal()

    def test_cash_out_account_creation_and_no_account_guidance(self):
        self.sign_in()
        self.app._show_screen("cash_out")
        frame = self.app.frames["cash_out"]
        frame._open_transfer()
        self.assertEqual(frame.notebook.select(), str(frame.accounts_panel))
        frame._open_account()
        frame.account_vars["name"].set("My Maya")
        frame.account_vars["number"].set("00001234567")
        self.button(self.modal(), "Save account").invoke()
        self.assertEqual(cash_out.list_accounts()[0]["account_number"], "00001234567")
        self.assertEqual(len(frame.accounts_table.get_children()), 1)

    def test_cash_out_automatic_fee_custom_override_and_reset(self):
        frame, _, modal = self.cash_out_form()
        fields = frame.transfer_vars
        for amount, fee in [
            (499, "5.00"),
            (750, "10.00"),
            (1000, "15.00"),
            (1500, "25.00"),
            (2000, "30.00"),
        ]:
            fields["amount"].set(str(amount))
            self.assertEqual(fields["fee"].get(), fee)
        fields["fee"].set("12.50")
        fields["amount"].set("1500")
        self.assertEqual(fields["fee"].get(), "12.50")
        self.button(modal, "Use suggested fee").invoke()
        self.assertEqual(fields["fee"].get(), "25.00")
        fields["fee"].set("0")
        self.button(modal, "Save transfer").invoke()
        row = cash_out.list_transactions()[0]
        self.assertEqual(row["fee_cents"], 0)
        self.assertEqual(row["suggested_fee_cents"], 2500)
        self.assertEqual(row["reference_last5"], "07890")
        self.assertEqual(row["status"], "unclaimed")
        self.app.frames["finance"].refresh()
        self.assertEqual(
            self.app.frames["finance"].metrics["sales"].cget("text"), "PHP 0.00"
        )

    def test_cash_out_duplicate_warning_accept_decline_and_claim_search(self):
        frame, account_id, modal = self.cash_out_form()
        first = cash_out.create_transaction(
            transferred_at="2026-10-24 09:30",
            receiving_account_id=account_id,
            sender_account="Another sender",
            amount=1500,
            reference_last5="07890",
        )
        cash_out.claim_transaction(first)
        frame.transfer_vars["amount"].set("1500")
        with patch("ui.cash_out_ui.messagebox.askyesno", return_value=False) as warning:
            self.button(modal, "Save transfer").invoke()
        self.assertEqual(warning.call_args.args[0], "Possible duplicate cash-out")
        self.assertIn("CLAIMED", warning.call_args.args[1])
        self.assertEqual(len(cash_out.list_transactions()), 1)
        with patch("ui.cash_out_ui.messagebox.askyesno", return_value=True):
            self.button(modal, "Save transfer").invoke()
        self.assertEqual(len(cash_out.list_transactions()), 2)
        frame.reference_var.set("7890")
        frame._load_transactions()
        self.assertEqual(len(frame.transactions_table.get_children()), 2)
        with patch("ui.cash_out_ui.messagebox.askyesno", return_value=False):
            frame._claim_selected()
        self.assertEqual(len(cash_out.list_transactions(status="unclaimed")), 1)
        with patch("ui.cash_out_ui.messagebox.askyesno", return_value=True):
            frame._claim_selected()
        self.assertEqual(len(cash_out.list_transactions(status="claimed")), 2)
        self.assertTrue(frame.claim_button.instate(["disabled"]))
        frame.reference_var.set("99999")
        frame._load_transactions()
        self.assertEqual(frame.transactions_table.get_children(), ())
        self.assertEqual(
            frame.transactions_table.empty_text, "No matching transfer found."
        )

    def test_cash_out_editable_rules_prefill_future_forms(self):
        frame, _, modal = self.cash_out_form()
        frame.transfer_vars["amount"].set("1500")
        self.button(modal, "Save transfer").invoke()
        frame.rule_vars["block_fee_cents"].set("20")
        frame.rule_vars["lower_fee_cents"].set("7")
        frame.rule_vars["upper_fee_cents"].set("12")
        frame._save_rules()
        frame._open_transfer()
        frame.transfer_vars["amount"].set("1500")
        self.assertEqual(frame.transfer_vars["fee"].get(), "32.00")
        self.assertEqual(cash_out.list_transactions()[0]["fee_cents"], 2500)
        self.modal().destroy()

    def test_cash_out_tabs_and_transfer_footer_fit_small_windows(self):
        frame, _, modal = self.cash_out_form()
        self.pump()
        for label in ("Save transfer", "Cancel"):
            button = self.button(modal, label)
            self.assertTrue(button.winfo_ismapped())
            self.assertLessEqual(
                button.winfo_rooty() + button.winfo_height(),
                modal.winfo_rooty() + modal.winfo_height(),
            )
        modal.destroy()
        for width, height in [(960, 640), (1024, 768), (1366, 768)]:
            self.root.geometry(f"{width}x{height}+2000+0")
            for panel in (
                frame.transactions_panel,
                frame.accounts_panel,
                frame.rules_panel,
                frame.totals_panel,
            ):
                frame.notebook.select(panel)
                self.pump()
                self.assert_inside(self.app.logout_btn)
                for widget in descendants(panel):
                    if (
                        isinstance(widget, (ttk.Button, ttk.Entry, ttk.Combobox))
                        and widget.winfo_ismapped()
                    ):
                        # Scrollable rules may extend below the visible canvas by design.
                        if panel not in (frame.rules_panel, frame.totals_panel):
                            self.assert_inside(widget)
                if panel is frame.totals_panel:
                    self.assert_inside(self.button(panel, "Refresh fee totals"))

    def test_cash_out_fee_totals_refresh_after_recording_and_claiming(self):
        frame, _, modal = self.cash_out_form()
        frame.transfer_vars["date"].set(datetime.now().date().isoformat())
        frame.transfer_vars["amount"].set("1500")
        self.button(modal, "Save transfer").invoke()
        self.assertEqual(frame.fee_totals["day"].cget("text"), "PHP 25.00")
        self.assertIn("Claimed: PHP 0.00", frame.fee_breakdowns["day"].get())
        self.assertIn("Unclaimed: PHP 25.00", frame.fee_breakdowns["day"].get())
        frame.reference_var.set("99999")
        frame._load_transactions()
        frame.notebook.select(frame.totals_panel)
        self.pump()
        self.assertEqual(frame.fee_totals["day"].cget("text"), "PHP 25.00")
        frame._clear_search()
        transaction_id = cash_out.list_transactions()[0]["id"]
        frame.transactions_table.selection_set(str(transaction_id))
        with patch("ui.cash_out_ui.messagebox.askyesno", return_value=True):
            frame._claim_selected()
        self.assertEqual(frame.fee_totals["day"].cget("text"), "PHP 25.00")
        self.assertIn("Claimed: PHP 25.00", frame.fee_breakdowns["day"].get())
        self.assertIn("Unclaimed: PHP 0.00", frame.fee_breakdowns["day"].get())
        self.app.frames["finance"].refresh()
        self.assertEqual(
            self.app.frames["finance"].metrics["sales"].cget("text"), "PHP 0.00"
        )

    def test_cash_in_uses_shared_form_accounts_fees_and_direction_labels(self):
        frame, _, modal = self.cash_out_form()
        fields = frame.transfer_vars
        fields["type"].set("Cash-In")
        self.assertEqual(
            frame.transfer_labels["account"].cget("text"), "Shop sending account"
        )
        self.assertEqual(
            frame.transfer_labels["sender"].cget("text"), "Customer receiving account"
        )
        fields["amount"].set("1500")
        self.assertEqual(fields["fee"].get(), "25.00")
        fields["fee"].set("12.50")
        self.button(modal, "Save transfer").invoke()
        row = cash_out.list_transactions()[0]
        self.assertEqual(row["transaction_type"], "cash_in")
        self.assertEqual(row["fee_cents"], 1250)
        self.assertEqual(
            frame.transactions_table.set(str(row["id"]), "type"), "Cash-In"
        )
        self.assertEqual(
            frame.transactions_table.set(str(row["id"]), "status"), "Pending"
        )
        self.assertEqual(frame.claim_button.cget("text"), "Confirm transfer completed")
        with patch("ui.cash_out_ui.messagebox.askyesno", return_value=True) as confirm:
            frame._claim_selected()
        self.assertEqual(confirm.call_args.args[0], "Confirm transfer completed")
        self.assertIn("sent to the customer's account", confirm.call_args.args[1])
        self.assertEqual(
            frame.transactions_table.set(str(row["id"]), "status"), "Completed"
        )
        self.assertTrue(frame.claim_button.instate(["disabled"]))
        frame._open_details()
        details = self.modal()
        labels = [
            str(w.cget("text"))
            for w in descendants(details)
            if isinstance(w, ttk.Label)
        ]
        self.assertIn("Cash-In", labels)
        self.assertIn("Shop sending account", labels)
        self.assertIn("Customer receiving account", labels)
        self.assertIn("Completed at", labels)
        details.destroy()
        self.app.frames["finance"].refresh()
        self.assertEqual(
            self.app.frames["finance"].metrics["sales"].cget("text"), "PHP 0.00"
        )

    def test_cash_in_out_search_and_fee_totals_can_filter_by_service(self):
        frame, account_id, modal = self.cash_out_form()
        modal.destroy()
        today = datetime.now().date().isoformat()
        common = dict(
            transferred_at=f"{today} 10:30",
            receiving_account_id=account_id,
            sender_account="Customer wallet",
            amount=1500,
            reference_last5="07890",
        )
        cash_out.create_transaction(**common, fee=25)
        cash_out.create_transaction(**common, fee=10, transaction_type="cash_in")
        frame.refresh()
        frame.reference_var.set("7890")
        frame._load_transactions()
        self.assertEqual(len(frame.transactions_table.get_children()), 2)
        frame.type_filter.set("Cash-In")
        frame._load_transactions()
        self.assertEqual(len(frame.transactions_table.get_children()), 1)
        self.assertEqual(
            frame.transactions_table.set(
                frame.transactions_table.get_children()[0], "type"
            ),
            "Cash-In",
        )
        frame.fee_service_var.set("Both services")
        frame._refresh_fee_totals()
        self.assertEqual(frame.fee_totals["day"].cget("text"), "PHP 35.00")
        self.assertIn("Cash-Out: PHP 25.00", frame.fee_breakdowns["day"].get())
        self.assertIn("Cash-In: PHP 10.00", frame.fee_breakdowns["day"].get())
        frame.fee_service_var.set("Cash-In")
        frame._refresh_fee_totals()
        self.assertEqual(frame.fee_totals["day"].cget("text"), "PHP 10.00")
        frame.fee_service_var.set("Cash-Out")
        frame._refresh_fee_totals()
        self.assertEqual(frame.fee_totals["day"].cget("text"), "PHP 25.00")

    def test_cash_in_duplicate_warning_is_specific_to_direction(self):
        frame, account_id, modal = self.cash_out_form()
        cash_out.create_transaction(
            transferred_at="2026-10-24 10:15",
            receiving_account_id=account_id,
            sender_account="Customer wallet",
            amount=1500,
            reference_last5="07890",
            transaction_type="cash_in",
        )
        frame.transfer_vars["type"].set("Cash-In")
        frame.transfer_vars["amount"].set("1500")
        with patch("ui.cash_out_ui.messagebox.askyesno", return_value=False) as warning:
            self.button(modal, "Save transfer").invoke()
        self.assertEqual(warning.call_args.args[0], "Possible duplicate cash-in")
        self.assertEqual(len(cash_out.list_transactions()), 1)
        frame.transfer_vars["type"].set("Cash-Out")
        self.assertEqual(
            frame.transfer_labels["account"].cget("text"), "Shop receiving account"
        )
        with patch("ui.cash_out_ui.messagebox.askyesno") as warning:
            self.button(modal, "Save transfer").invoke()
        warning.assert_not_called()
        self.assertEqual(len(cash_out.list_transactions()), 2)


if __name__ == "__main__":
    unittest.main()
