"""Entry point for the standalone Linux setup executable."""

import argparse
import json
import sqlite3
import subprocess
import sys
import tempfile
import tkinter as tk
from contextlib import closing
from pathlib import Path

from core.linux_installer import InstallLocations, child_environment, install_payload
from ui.linux_setup_ui import SetupWizard, UninstallWizard


def smoke_test(payload: Path, version: str, report_path: Path):
    report = {"ok": False}
    try:
        with tempfile.TemporaryDirectory(
            prefix="tindahan-installer-check-"
        ) as temporary:
            directory = Path(temporary)
            locations = InstallLocations(
                directory / "app",
                directory / "data",
                directory / "menu",
                directory / "desktop",
            )
            root = tk.Tk()
            root.withdraw()
            finished = []

            def on_complete(ok, error):
                finished.append((ok, error))
                root.after(0, wizard.close)

            wizard = SetupWizard(
                root, payload, version, locations=locations, on_complete=on_complete
            )
            wizard.desktop_var.set(True)
            root.after(50, wizard.start_install)
            root.after(
                90000,
                lambda: (
                    finished.append((False, "Installer timed out")),
                    root.destroy(),
                ),
            )
            root.mainloop()
            if not finished or not finished[0][0]:
                raise RuntimeError(
                    finished[0][1] if finished else "Installer did not complete"
                )
            app_report = directory / "app-check.json"
            environment = child_environment()
            environment["TINDAHAN_DATA_DIR"] = str(locations.data)
            subprocess.run(
                [
                    str(locations.application / "POS-System"),
                    "--smoke-test",
                    str(app_report),
                ],
                env=environment,
                cwd=directory,
                check=True,
                timeout=90,
            )
            if not json.loads(app_report.read_text())["ok"]:
                raise RuntimeError("Installed application checks failed")
            locations.data.mkdir(parents=True, exist_ok=True)
            with (
                closing(sqlite3.connect(locations.data / "pos.db")) as connection,
                connection,
            ):
                connection.execute("CREATE TABLE installer_check (value TEXT)")
                connection.execute(
                    "INSERT INTO installer_check VALUES ('keep records')"
                )
            install_payload(payload, locations, version=version, desktop_shortcut=True)
            with closing(sqlite3.connect(locations.data / "pos.db")) as connection:
                if (
                    connection.execute("SELECT value FROM installer_check").fetchone()[
                        0
                    ]
                    != "keep records"
                ):
                    raise RuntimeError("Update did not preserve records")
            if not (locations.applications_menu / "tindahan-system.desktop").is_file():
                raise RuntimeError("Application shortcut missing")
            if not (locations.application / "Tindahan-Uninstall.run").is_file():
                raise RuntimeError("Graphical uninstaller missing")
            if not (
                locations.applications_menu / "tindahan-system-uninstall.desktop"
            ).is_file():
                raise RuntimeError("Uninstall menu entry missing")
            for name in (
                "THIRD_PARTY_NOTICES.md",
                "third-party-manifest.json",
                "SOURCE_CODE.md",
                "licenses/python-pygame/LGPL.txt",
                f"sources/Tindahan-System-{version}-sources.tar.gz",
            ):
                if not (locations.application / name).is_file():
                    raise RuntimeError(
                        f"Installed redistribution material missing: {name}"
                    )
            report.update(
                ok=True,
                wizard=True,
                installed_app=True,
                update_preserves_data=True,
                redistribution_materials=True,
            )
    except Exception as exc:
        report["error"] = str(exc)
        raise
    finally:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2))


def uninstall_smoke_test(report_path: Path):
    report = {"ok": False}
    try:
        with tempfile.TemporaryDirectory(
            prefix="tindahan-uninstall-check-"
        ) as temporary:
            directory = Path(temporary)
            locations = InstallLocations(
                directory / "app",
                directory / "data",
                directory / "menu",
                directory / "desktop",
            )
            locations.application.mkdir()
            (locations.application / ".tindahan-install").write_text("test\n")
            for name in (
                "tindahan-system.desktop",
                "tindahan-system-uninstall.desktop",
            ):
                locations.applications_menu.mkdir(exist_ok=True)
                (locations.applications_menu / name).write_text("[Desktop Entry]\n")
            locations.data.mkdir()
            with (
                closing(sqlite3.connect(locations.data / "pos.db")) as connection,
                connection,
            ):
                connection.execute("CREATE TABLE retained (value TEXT)")
                connection.execute("INSERT INTO retained VALUES ('shop records')")
            sounds = locations.data / "sounds"
            sounds.mkdir()
            (sounds / "personal.wav").write_bytes(b"private user sound")
            original = (locations.data / "pos.db").read_bytes()
            root = tk.Tk()
            root.withdraw()
            finished = []

            def on_complete(ok, error):
                finished.append((ok, error))
                root.after(0, wizard.close)

            wizard = UninstallWizard(root, locations=locations, on_complete=on_complete)
            root.after(50, wizard.start_uninstall)
            root.after(
                60000,
                lambda: (
                    finished.append((False, "Uninstall timed out")),
                    root.destroy(),
                ),
            )
            root.mainloop()
            if not finished or not finished[0][0]:
                raise RuntimeError(
                    finished[0][1] if finished else "Uninstall did not finish"
                )
            if locations.application.exists() or any(
                locations.applications_menu.glob("tindahan-system*.desktop")
            ):
                raise RuntimeError("Program files or shortcuts remained")
            if (locations.data / "pos.db").read_bytes() != original or not (
                sounds / "personal.wav"
            ).is_file():
                raise RuntimeError("Uninstall changed store data")
            report.update(
                ok=True,
                wizard=True,
                removes_application=True,
                preserves_data=True,
                preserves_sounds=True,
            )
    except Exception as exc:
        report["error"] = str(exc)
        raise
    finally:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Tindahan System Setup")
    parser.add_argument("--smoke-test", type=Path, metavar="REPORT")
    parser.add_argument(
        "--uninstall", action="store_true", help="open the graphical uninstaller"
    )
    args = parser.parse_args()
    base = (
        Path(sys._MEIPASS)
        if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parents[2] / "build/linux-installer"
    )
    payload = base / "payload.tar.gz"
    version = (base / "version.txt").read_text().strip()
    uninstall = (
        args.uninstall
        or (base / "uninstall-mode").is_file()
        or "uninstall" in Path(sys.executable).name.casefold()
    )
    if args.smoke_test:
        if uninstall:
            uninstall_smoke_test(args.smoke_test.resolve())
        else:
            smoke_test(payload, version, args.smoke_test.resolve())
        return
    root = tk.Tk()
    if uninstall:
        UninstallWizard(root)
    else:
        SetupWizard(root, payload, version)
    root.mainloop()


if __name__ == "__main__":
    main()
