"""Build on the target OS: graphical installers and portable packages."""

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

from PyInstaller.archive.readers import CArchiveReader
from third_party import (
    check_inventory,
    prepare_materials,
    verify_directory,
    verify_wrapper,
)

ROOT = Path(__file__).resolve().parents[1]


def run(*command: str) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def verify_exclusions(executable: Path, *, bundle: Path | None = None) -> dict:
    """Inspect actual frozen contents so an upstream hook cannot restore exclusions."""

    def forbidden(name: str) -> bool:
        filename = name.replace("\\", "/").rsplit("/", 1)[-1].casefold()
        return (
            filename == "freesansbold.ttf"
            or filename == "readline"
            or filename.startswith("readline.")
            or filename.startswith("libreadline")
        )

    archive = CArchiveReader(str(executable))
    names = list(archive.toc)
    for name in archive.toc:
        if name.endswith(".pyz"):
            names.extend(archive.open_embedded_archive(name).toc)
    if bundle is not None:
        names.extend(str(path.relative_to(bundle)) for path in bundle.rglob("*"))
    unexpected = sorted({name for name in names if forbidden(name)})
    if unexpected:
        raise RuntimeError(
            "Excluded components are still bundled: " + ", ".join(unexpected)
        )
    return {
        "executable": executable.name,
        "readline_absent": True,
        "freesans_font_absent": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument(
        "--portable-only", action="store_true", help="skip Windows setup compiler"
    )
    args = parser.parse_args()
    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        parser.error("version must have three numeric parts, e.g. 1.0.0")
    if sys.platform not in {"win32", "linux"}:
        parser.error("build on Windows or Linux")
    if platform.machine().lower() not in {"amd64", "x86_64"}:
        parser.error("these installer recipes currently target x86-64")
    iscc = None
    if sys.platform == "win32" and not args.portable_only:
        iscc = shutil.which("ISCC.exe")
        if not iscc:
            candidate = Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe")
            if candidate.is_file():
                iscc = str(candidate)
        if not iscc:
            parser.error("install Inno Setup 6 or pass --portable-only")

    for filename in ("exclusion-checks.json", "third-party-checks.json"):
        (ROOT / "build" / filename).unlink(missing_ok=True)

    run(
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "POS-System.spec"
    )
    bundle = ROOT / "dist/POS-System"
    executable = bundle / (
        "POS-System.exe" if sys.platform == "win32" else "POS-System"
    )
    exclusion_checks = [verify_exclusions(executable, bundle=bundle)]
    license_checks = [check_inventory(ROOT, "POS-System")]
    redistribution, source_archive = prepare_materials(ROOT, args.version)
    shutil.copytree(redistribution, bundle, dirs_exist_ok=True)
    verify_directory(redistribution, bundle)
    report = ROOT / "build/bundle-smoke.json"
    report.unlink(missing_ok=True)
    # An absolute path and unrelated working directory catch missing bundled resources.
    subprocess.run(
        [str(executable), "--smoke-test", str(report)],
        cwd=bundle.parent,
        check=True,
        timeout=90,
    )
    if not report.is_file() or not json.loads(report.read_text(encoding="utf-8")).get(
        "ok"
    ):
        raise RuntimeError("The bundled app failed its smoke check")
    for filename in ("README.md", "LICENSE"):
        shutil.copy2(ROOT / filename, bundle / filename)

    releases = ROOT / "dist/releases"
    releases.mkdir(parents=True, exist_ok=True)
    artifacts = []
    release_source = releases / source_archive.name
    shutil.copyfile(source_archive, release_source)
    artifacts.append(release_source)
    if sys.platform == "win32":
        name = f"Tindahan-System-{args.version}-windows-x86_64-portable"
        artifacts.append(
            Path(
                shutil.make_archive(
                    str(releases / name), "zip", bundle.parent, bundle.name
                )
            )
        )
        if iscc:
            run(
                iscc,
                f"/DAppVersion={args.version}",
                str(ROOT / "packaging/windows/setup.iss"),
            )
            artifacts.append(
                releases / f"Tindahan-System-{args.version}-windows-x86_64-setup.exe"
            )
    else:
        installer_data = ROOT / "build/linux-installer"
        installer_data.mkdir(parents=True, exist_ok=True)
        (installer_data / "version.txt").write_text(args.version, encoding="utf-8")
        run(
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "Linux-Uninstall.spec",
        )
        license_checks.append(check_inventory(ROOT, "Linux-Uninstall"))
        verify_wrapper(
            redistribution, CArchiveReader(str(ROOT / "dist/Tindahan-Uninstall"))
        )
        uninstaller = (
            releases / f"Tindahan-System-{args.version}-linux-x86_64-uninstall.run"
        )
        shutil.move(ROOT / "dist/Tindahan-Uninstall", uninstaller)
        uninstaller.chmod(0o755)
        exclusion_checks.append(verify_exclusions(uninstaller))
        shutil.copy2(uninstaller, bundle / "Tindahan-Uninstall.run")
        uninstall_report = ROOT / "build/uninstaller-smoke.json"
        uninstall_report.unlink(missing_ok=True)
        subprocess.run(
            [str(uninstaller), "--smoke-test", str(uninstall_report)],
            check=True,
            timeout=90,
        )
        if not json.loads(uninstall_report.read_text())["ok"]:
            raise RuntimeError("Graphical uninstaller verification failed")
        artifacts.append(uninstaller)
        for filename in ("install.sh", "uninstall.sh"):
            target = bundle / filename
            shutil.copyfile(ROOT / "packaging/linux" / filename, target)
            target.chmod(0o755)
        archive = releases / f"Tindahan-System-{args.version}-linux-x86_64.tar.gz"
        with tarfile.open(archive, "w:gz") as output:
            output.add(bundle, arcname="Tindahan-System")
        artifacts.append(archive)
        shutil.copyfile(archive, installer_data / "payload.tar.gz")
        run(
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "Linux-Setup.spec",
        )
        license_checks.append(check_inventory(ROOT, "Linux-Setup"))
        verify_wrapper(
            redistribution, CArchiveReader(str(ROOT / "dist/Tindahan-Setup"))
        )
        installer = releases / f"Tindahan-System-{args.version}-linux-x86_64-setup.run"
        shutil.move(ROOT / "dist/Tindahan-Setup", installer)
        installer.chmod(0o755)
        exclusion_checks.append(verify_exclusions(installer))
        installer_report = ROOT / "build/installer-smoke.json"
        installer_report.unlink(missing_ok=True)
        subprocess.run(
            [str(installer), "--smoke-test", str(installer_report)],
            cwd=releases,
            check=True,
            timeout=180,
        )
        if not json.loads(installer_report.read_text())["ok"]:
            raise RuntimeError("Graphical installer verification failed")
        artifacts.append(installer)
    (ROOT / "build/exclusion-checks.json").write_text(
        json.dumps({"ok": True, "checks": exclusion_checks}, indent=2), encoding="utf-8"
    )
    (ROOT / "build/third-party-checks.json").write_text(
        json.dumps({"ok": True, "checks": license_checks}, indent=2), encoding="utf-8"
    )
    for artifact in artifacts:
        with artifact.open("rb") as package:
            digest = hashlib.file_digest(package, "sha256").hexdigest()
        artifact.with_name(artifact.name + ".sha256").write_text(
            f"{digest}  {artifact.name}\n", encoding="utf-8"
        )
        print(f"Built {artifact}")


if __name__ == "__main__":
    main()
