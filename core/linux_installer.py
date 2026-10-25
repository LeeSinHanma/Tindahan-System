"""Install the Linux bundle transactionally without administrative privileges."""

import os
import shutil
import sqlite3
import subprocess
import tarfile
import tempfile
import uuid
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

from core.app_paths import prepare_database, user_data_directory


@dataclass(frozen=True)
class InstallLocations:
    application: Path
    data: Path
    applications_menu: Path
    desktop: Path

    @classmethod
    def for_current_user(cls):
        home = Path.home()
        data_root = Path(os.environ.get("XDG_DATA_HOME") or home / ".local/share")
        if not data_root.is_absolute():
            data_root = home / ".local/share"
        desktop = home / "Desktop"
        config_root = Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config")
        if not config_root.is_absolute():
            config_root = home / ".config"
        try:
            for line in (config_root / "user-dirs.dirs").read_text().splitlines():
                if line.startswith('XDG_DESKTOP_DIR="') and line.endswith('"'):
                    candidate = Path(line.split('"', 2)[1].replace("$HOME", str(home)))
                    if candidate.is_absolute():
                        desktop = candidate
        except OSError:
            pass
        return cls(
            home / ".local/opt/tindahan-system",
            user_data_directory(),
            data_root / "applications",
            desktop,
        )


def child_environment() -> dict:
    environment = os.environ.copy()
    original = environment.pop("LD_LIBRARY_PATH_ORIG", None)
    environment.pop("LD_LIBRARY_PATH", None)
    if original:
        environment["LD_LIBRARY_PATH"] = original
    environment["PYINSTALLER_RESET_ENVIRONMENT"] = "1"
    return environment


def launch_application(locations: InstallLocations) -> subprocess.Popen:
    return subprocess.Popen(
        [str(locations.application / "POS-System")],
        cwd=locations.application,
        env=child_environment(),
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _desktop_entry(executable: Path, *, uninstall: bool = False) -> str:
    quoted = (
        str(executable)
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("`", "\\`")
        .replace("$", "\\$")
    )
    quoted = quoted.replace("\\", "\\\\").replace("%", "%%")
    name = "Uninstall Tindahan System" if uninstall else "Tindahan System"
    icon = "edit-delete" if uninstall else "accessories-calculator"
    return (
        f"[Desktop Entry]\nType=Application\nName={name}\n"
        "Comment=POS, inventory, and cash services\n"
        f'Exec="{quoted}"\nIcon={icon}\nTerminal=false\nCategories=Office;Finance;\n'
    )


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".tindahan-shortcut-", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(content)
        temporary.chmod(0o644)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _store_snapshot(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise ValueError("The selected database could not be found. Choose it again.")
    prepare_database(destination, source)
    with closing(sqlite3.connect(destination)) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        if not {"products", "sales", "users", "settings"}.issubset(tables):
            raise ValueError("Choose a Tindahan System store database (pos.db).")


def install_payload(
    payload: Path,
    locations: InstallLocations,
    *,
    version: str,
    import_database: Path | None = None,
    desktop_shortcut: bool = False,
    progress=lambda percent, message: None,
) -> None:
    import fcntl

    application = locations.application
    application.parent.mkdir(parents=True, exist_ok=True)
    lock_path = application.parent / ".tindahan-setup.lock"
    with lock_path.open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(
                "Another Tindahan installer is open. Finish it first."
            ) from exc
        if application.is_symlink() or (
            application.exists() and not (application / ".tindahan-install").is_file()
        ):
            raise ValueError(
                "The installation folder contains other files. Move it aside before installing."
            )
        database = locations.data / "pos.db"
        if import_database is not None and database.exists():
            raise ValueError(
                "A store database already exists. Setup will keep it and cannot replace it."
            )
        progress(5, "Preparing installation…")
        with tempfile.TemporaryDirectory(
            prefix=".tindahan-setup-", dir=application.parent
        ) as temporary:
            staging = Path(temporary)
            with tarfile.open(payload, "r:gz") as archive:
                members = archive.getmembers()
                if not members or any(
                    Path(member.name).parts[0] != "Tindahan-System"
                    for member in members
                ):
                    raise ValueError(
                        "The installer package is invalid. Download it again."
                    )
                required = sum(member.size for member in members if member.isfile())
                if (
                    shutil.disk_usage(application.parent).free
                    < required + 20 * 1024 * 1024
                ):
                    raise OSError(
                        "There is not enough free space to install Tindahan System."
                    )
                archive.extractall(staging, filter="data")
            bundle = staging / "Tindahan-System"
            executable = bundle / "POS-System"
            if not executable.is_file() or not (bundle / "LICENSE").is_file():
                raise ValueError("The installer is incomplete. Download it again.")
            executable.chmod(executable.stat().st_mode | 0o111)
            (bundle / ".tindahan-install").write_text(version + "\n")
            progress(55, "Preparing store records…")
            legacy = application / "pos.db"
            if legacy.is_file():
                _store_snapshot(legacy, bundle / "pos.db")
            snapshot = staging / "store-import.db"
            source = import_database
            if source is None and legacy.is_file() and not database.exists():
                source = legacy
            if source is not None:
                _store_snapshot(source, snapshot)

            menu = locations.applications_menu / "tindahan-system.desktop"
            uninstall_menu = (
                locations.applications_menu / "tindahan-system-uninstall.desktop"
            )
            uninstaller = bundle / "Tindahan-Uninstall.run"
            desktop = locations.desktop / "tindahan-system.desktop"
            if desktop_shortcut or desktop.is_file():
                (bundle / ".tindahan-desktop-path").write_text(str(desktop) + "\n")
            shortcut_paths = [menu] + ([desktop] if desktop_shortcut else [])
            if uninstaller.is_file():
                shortcut_paths.append(uninstall_menu)
            previous_shortcuts = {
                path: path.read_bytes() if path.exists() else None
                for path in shortcut_paths
            }
            previous_application = staging / "previous-installation"
            replaced = False
            installed = False
            try:
                progress(70, "Installing Tindahan System…")
                if application.exists():
                    application.rename(previous_application)
                    replaced = True
                bundle.rename(application)
                installed = True
                if source is not None:
                    locations.data.mkdir(parents=True, exist_ok=True)
                    try:
                        os.link(snapshot, database)
                    except FileExistsError as exc:
                        raise ValueError(
                            "A store database was created while setup was running. It has been kept. Run setup again without importing."
                        ) from exc
                    except OSError:
                        # The data directory may be on a different filesystem.
                        prepare_database(database, snapshot)
                progress(85, "Adding application shortcuts…")
                content = _desktop_entry(executable=application / "POS-System").encode()
                for path in shortcut_paths:
                    _atomic_write(
                        path,
                        _desktop_entry(
                            application / "Tindahan-Uninstall.run", uninstall=True
                        ).encode()
                        if path == uninstall_menu
                        else content,
                    )
                if desktop_shortcut:
                    desktop.chmod(0o755)
            except Exception:
                if installed:
                    shutil.rmtree(application)
                if replaced:
                    previous_application.rename(application)
                for path, previous in previous_shortcuts.items():
                    if previous is None:
                        path.unlink(missing_ok=True)
                    elif path.exists() and path.read_bytes() != previous:
                        _atomic_write(path, previous)
                raise
        progress(100, "Installation complete.")


def uninstall_application(
    locations: InstallLocations, *, progress=lambda percent, message: None
) -> None:
    """Remove program files and shortcuts, retaining all store data and sounds."""
    import fcntl

    application = locations.application
    if application.is_symlink() or not (application / ".tindahan-install").is_file():
        raise ValueError("No recognized Tindahan System installation was found.")
    if locations.data.resolve().is_relative_to(application.resolve()):
        raise ValueError(
            "Your store data is inside the application folder. Move or back it up outside that folder before uninstalling."
        )
    with (application.parent / ".tindahan-setup.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(
                "Another Tindahan setup is running. Finish it first."
            ) from exc
        progress(10, "Checking store records…")
        legacy = application / "pos.db"
        if legacy.is_file():
            destination = locations.data / "pos.db"
            if destination.exists():
                destination = (
                    locations.data / "legacy-backups" / f"pos-{uuid.uuid4().hex}.db"
                )
            _store_snapshot(legacy, destination)
        shortcuts = [
            locations.applications_menu / "tindahan-system.desktop",
            locations.applications_menu / "tindahan-system-uninstall.desktop",
        ]
        marker = application / ".tindahan-desktop-path"
        if marker.is_file():
            desktop = Path(marker.read_text().strip())
            if desktop.is_absolute() and desktop.name == "tindahan-system.desktop":
                shortcuts.append(desktop)
        progress(40, "Removing Tindahan System…")
        shutil.rmtree(application)
        progress(85, "Removing application shortcuts…")
        for path in shortcuts:
            path.unlink(missing_ok=True)
        progress(
            100,
            "Tindahan System has been uninstalled. Your store records and sounds have been kept.",
        )
