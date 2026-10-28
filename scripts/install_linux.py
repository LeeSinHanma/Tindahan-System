"""Install a source checkout as a Linux desktop application for the current user."""

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL_NAME = "tindahan-system-source"


def data_root() -> Path:
    directory = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    return directory if directory.is_absolute() else Path.home() / ".local/share"


def desktop_quote(value: str) -> str:
    # Desktop Exec fields have their own escaping rules, separate from the shell.
    for character in ('\\', '"', '`', '$'):
        value = value.replace(character, '\\' + character)
    return '"' + value.replace('\\', '\\\\').replace("%", "%%") + '"'


def install() -> None:
    import sqlite3  # noqa: F401
    import tkinter  # noqa: F401
    import venv  # noqa: F401

    target = Path.home() / ".local/opt" / INSTALL_NAME
    marker = target / ".tindahan-source-install"
    if target.exists() and not marker.is_file():
        raise RuntimeError(f"Refusing to replace an unrecognized folder: {target}")
    if ROOT == target:
        raise RuntimeError("Run installation from a fresh project checkout to update.")
    target.mkdir(parents=True, exist_ok=True)
    marker.touch()

    python = target / ".venv/bin/python"
    if not python.is_file():
        subprocess.run([sys.executable, "-m", "venv", str(target / ".venv")], check=True)
    subprocess.run(
        [str(python), "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")],
        check=True,
    )
    for filename in ("main.py", "requirements.txt", "LICENSE", "THIRD_PARTY_NOTICES.md"):
        shutil.copy2(ROOT / filename, target / filename)
    for directory in ("core", "db", "ui", "scripts"):
        (target / directory).mkdir(exist_ok=True)
        paths = (
            [ROOT / "scripts/install_linux.py"]
            if directory == "scripts"
            else (ROOT / directory).glob("*.py")
        )
        for path in paths:
            shutil.copy2(path, target / directory / path.name)
    shutil.copy2(ROOT / "packaging/third_party/SOURCE_CODE.md", target / "SOURCE_CODE.md")

    # Use SQLite's backup API so committed WAL records are also imported.
    # An existing installed database is never replaced.
    sys.path.insert(0, str(ROOT))
    from core.app_paths import prepare_database

    database_directory = data_root() / "tindahan-system"
    prepare_database(database_directory / "pos.db", ROOT / "pos.db")

    launcher = target / "Tindahan-System"
    launcher.write_text(
        "#!/bin/sh\n"
        f"export TINDAHAN_DATA_DIR={shlex.quote(str(database_directory))}\n"
        f"exec {shlex.quote(str(python))} {shlex.quote(str(target / 'main.py'))} \"$@\"\n",
        encoding="utf-8",
    )
    launcher.chmod(0o755)
    applications = data_root() / "applications"
    applications.mkdir(parents=True, exist_ok=True)
    entry = applications / f"{INSTALL_NAME}.desktop"
    entry.write_text(
        "[Desktop Entry]\nType=Application\nName=Tindahan System\n"
        "Comment=POS, inventory, and cash services\n"
        f"Exec={desktop_quote(str(launcher))}\n"
        "Icon=accessories-calculator\nTerminal=false\nCategories=Office;Finance;\n",
        encoding="utf-8",
    )
    entry.chmod(0o755)
    if shutil.which("update-desktop-database"):
        subprocess.run(["update-desktop-database", str(applications)], check=False)
    print(f"Installed in {target}")
    print("Open Tindahan System from your application menu.")
    print(f"Store records: {database_directory / 'pos.db'}")


def uninstall() -> None:
    target = Path.home() / ".local/opt" / INSTALL_NAME
    if not (target / ".tindahan-source-install").is_file():
        raise RuntimeError(f"No recognized source installation at {target}")
    (data_root() / "applications" / f"{INSTALL_NAME}.desktop").unlink(missing_ok=True)
    shutil.rmtree(target)
    print("Tindahan System removed. Store records and selected sounds were kept.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uninstall", action="store_true", help="remove the source installation")
    args = parser.parse_args()
    if not sys.platform.startswith("linux") or sys.version_info < (3, 10):
        parser.error("Linux with Python 3.10 or newer is required")
    if os.geteuid() == 0:
        parser.error("Run without sudo; this installs for your user account")
    try:
        if args.uninstall:
            uninstall()
        else:
            install()
    except ImportError as exc:
        parser.exit(1, f"Missing Python support: {exc}. Install python3-venv and python3-tk.\n")
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Installation failed: {exc}\n")


if __name__ == "__main__":
    main()
