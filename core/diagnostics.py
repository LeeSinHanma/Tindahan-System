"""End-to-end checks used by native package builds, isolated from shop records."""

import json
import os
import secrets
import tempfile
import tkinter as tk
import traceback
import wave
from pathlib import Path


def smoke_test(report_path: Path) -> None:
    from core import checkout_audio, inventory, shopping_list
    from db import database
    from ui.app import App

    report_path = report_path.resolve()
    report = {"ok": False}
    root = None
    original_database = database.DB_FILE
    original_connect = database.sqlite3.connect
    connections = []
    temporary = tempfile.TemporaryDirectory(prefix="tindahan-smoke-")
    saved_environment = {
        key: os.environ.get(key)
        for key in (
            "TINDAHAN_DATA_DIR",
            "SDL_AUDIODRIVER",
            "PYGAME_HIDE_SUPPORT_PROMPT",
        )
    }

    def tracked_connect(*args, **kwargs):
        connection = original_connect(*args, **kwargs)
        connections.append(connection)
        return connection

    database.sqlite3.connect = tracked_connect
    try:
        # Set directly before App creates the database; never open shop records.
        database.DB_FILE = Path(temporary.name) / "pos.db"
        os.environ["TINDAHAN_DATA_DIR"] = temporary.name
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
        root = tk.Tk()
        root.withdraw()
        errors = []
        root.report_callback_exception = lambda kind, value, tb: errors.append(
            "".join(traceback.format_exception(kind, value, tb))
        )
        app = App(root)
        root.update()
        login = app.frames["login"]
        if login.mode != "setup":
            raise RuntimeError("A fresh database must require owner account setup")
        password = secrets.token_urlsafe(24)
        login.username_var.set("bundle-check-owner")
        login.password_var.set(password)
        login.confirm_var.set(password)
        login._submit()
        root.update()
        if not (app.current_user or {}).get("is_admin"):
            raise RuntimeError("Owner account setup failed")
        if errors:
            raise RuntimeError("\n".join(errors))

        import pygame

        if checkout_audio.play_checkout_sound() is not None:
            raise RuntimeError("Checkout audio must be optional on a fresh install")
        # A temporary generated tone exercises audio without redistributing a recording.
        sound_path = Path(temporary.name) / "test-tone.wav"
        with wave.open(str(sound_path), "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(22050)
            output.writeframes(b"\x00\x00\x10\x00" * 2205)
        try:
            checkout_audio.choose_sound(sound_path)
            checkout_audio.preview_sound()
            if not checkout_audio.sound_info()["enabled"]:
                raise RuntimeError("User-selected checkout audio did not persist")
            checkout_audio.remove_sound()
        finally:
            pygame.mixer.quit()
        product_id = inventory.create_product(
            dict(
                name="Package check",
                barcode="test-001",
                original_price=5,
                sell_price=10,
                stock=2,
                stock_tracked=True,
            )
        )
        shopping_list.add_item(product_id, 1)
        for name, export in (
            ("inventory", inventory.save_pdf),
            ("shopping", shopping_list.save_pdf),
        ):
            pdf_path = Path(temporary.name) / f"{name}.pdf"
            export(str(pdf_path))
            if not pdf_path.read_bytes().startswith(b"%PDF-"):
                raise RuntimeError(f"{name} PDF export failed")
        report.update(
            ok=True, screens=list(app.frames), owner_setup=True, audio=True, pdf=True
        )
    except Exception:
        report["error"] = traceback.format_exc()
        raise
    finally:
        database.DB_FILE = original_database
        database.sqlite3.connect = original_connect
        if root is not None:
            for timer in root.tk.call("after", "info"):
                root.tk.call("after", "cancel", timer)
            root.destroy()
        for connection in connections:
            connection.close()
        temporary.cleanup()
        for key, value in saved_environment.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
