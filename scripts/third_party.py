"""Assemble reviewed redistribution materials and check frozen build inventories."""

import ast
import hashlib
import io
import json
import platform
import shutil
import sys
import tarfile
import urllib.request
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "packaging/third_party"
KINDS = {"PYMODULE", "PYSOURCE", "DATA", "BINARY", "EXTENSION"}
RUNTIME_DISTRIBUTIONS = (
    "pygame",
    "pillow",
    "reportlab",
    "charset-normalizer",
    "pyinstaller",
)


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def toc_entries(value, kinds):
    if isinstance(value, (tuple, list)):
        if (
            len(value) == 3
            and all(isinstance(item, str) for item in value)
            and value[2] in kinds
        ):
            yield value
        else:
            for item in value:
                yield from toc_entries(item, kinds)


def inventory(root: Path, artifact: str) -> list[dict]:
    """Hash incorporated third-party files, using final data/binary manifests."""
    records = {}
    environment = Path(sys.prefix).resolve()
    for name in ("Analysis-00.toc", "PKG-00.toc", "COLLECT-00.toc"):
        path = root / "build" / artifact / name
        if not path.is_file():
            continue
        kinds = {"PYMODULE", "PYSOURCE"} if name.startswith("Analysis") else KINDS
        for destination, source, kind in toc_entries(
            ast.literal_eval(path.read_text(encoding="utf-8")), kinds
        ):
            file = Path(source)
            if not file.is_file():
                if source == "-" and kind == "PYMODULE":  # namespace package
                    continue
                raise RuntimeError(f"Missing inventory input: {source}")
            file = file.resolve()
            if file.is_relative_to(root) and not file.is_relative_to(environment):
                continue  # application source and generated packaging materials
            key = (destination.replace("\\", "/"), kind)
            record = {"destination": key[0], "kind": kind, "sha256": digest(file)}
            if key in records and records[key] != record:
                raise RuntimeError(f"Conflicting frozen inventory entry: {destination}")
            records[key] = record
    if not records:
        raise RuntimeError(f"Frozen inventory is missing for {artifact}")
    return sorted(records.values(), key=lambda r: (r["destination"], r["kind"]))


def environment_versions() -> dict:
    return {
        "python": platform.python_version(),
        "platform": sys.platform,
        "machine": platform.machine().lower(),
        "distributions": {
            name: metadata.version(name) for name in RUNTIME_DISTRIBUTIONS
        },
    }


def check_inventory(root: Path, artifact: str) -> dict:
    """Fail before releasing binaries whose licenses have not been reviewed."""
    actual = inventory(root, artifact)
    versions = environment_versions()
    catalog_hash = digest(root / "packaging/third_party/catalog.json")
    report = {
        "artifact": artifact,
        "environment": versions,
        "catalog_sha256": catalog_hash,
        "files": actual,
    }
    report_path = root / "build" / f"third-party-inventory-{artifact}.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    profiles = root / "packaging/third_party/profiles"
    for path in sorted(profiles.glob("*.json")):
        profile = json.loads(path.read_text(encoding="utf-8"))
        if profile["environment"] != versions:
            continue
        if profile.get("catalog_sha256") != catalog_hash:
            continue
        reviewed = {
            (r["destination"], r["kind"], r["sha256"])
            for r in profile["artifacts"].get(artifact, [])
        }
        unexpected = [
            r
            for r in actual
            if (r["destination"], r["kind"], r["sha256"]) not in reviewed
        ]
        if not unexpected:
            return {
                "artifact": artifact,
                "profile": path.name,
                "files_checked": len(actual),
            }
    raise RuntimeError(
        f"Third-party license review needed for {artifact} in this build environment. "
        f"Inspect {report_path.relative_to(root)} and update the reviewed notices/profile "
        "before publishing packages. Existing notices are not approval for different binaries."
    )


def catalog_files(materials: Path):
    catalog = json.loads((materials / "catalog.json").read_text(encoding="utf-8"))
    seen = set()
    for component in catalog["components"]:
        if not component["files"]:
            raise RuntimeError(f"No notices collected for {component['id']}")
        for file in component["files"]:
            path = materials / file["path"]
            if not path.resolve().is_relative_to(materials.resolve()):
                raise RuntimeError("Notice path is outside the materials folder")
            if not path.is_file() or digest(path) != file["sha256"]:
                raise RuntimeError(f"Notice missing or changed: {file['path']}")
            if file["path"] not in seen:
                seen.add(file["path"])
                yield path, file["path"]


def render_notices(materials: Path) -> str:
    # Validate every licensed text before writing a distributable acknowledgement.
    list(catalog_files(materials))
    catalog = json.loads((materials / "catalog.json").read_text(encoding="utf-8"))
    parts = [
        "# Third-party notices\n\n",
        "Tindahan System's own code is licensed under MIT (see LICENSE). "
        "Dependencies retain their own copyrights and licenses. These notices cover "
        "the reviewed Linux desktop distribution; an individual setup/uninstall runtime "
        "uses a subset of these components. See third-party-manifest.json for versions, "
        "origins and SHA-256 hashes.\n\n",
        "Pygame is used for optional checkout audio and is covered by the GNU Lesser "
        "General Public License, version 2.1 or later. Copyright (C) 2000-2001 Pete Shinners, "
        "with additional contributors identified in the source. Its license and retained helper notices "
        "are reproduced below. The app includes the corresponding Pygame source and this "
        "application's source in sources/Tindahan-System-<version>-sources.tar.gz. "
        "See SOURCE_CODE.md for modification and rebuild instructions.\n\n",
        "You may modify the application for your own use and reverse engineer it to debug "
        "such modifications. Nothing in the application's terms restricts rights granted "
        "by the LGPL.\n\n",
        "This software is based in part on the work of the Independent JPEG Group.\n\n",
        "Portions of this software are copyright © 1996-2026 The FreeType Project "
        "(https://freetype.org). All rights reserved. FreeType is distributed here under "
        "the FreeType License (FTL), rather than its alternative GPL terms.\n\n",
        "Zstandard's BSD license and libuuid's BSD terms are selected. GCC runtime "
        "libraries retain the GPL with GCC Runtime Library Exception; the exception "
        "permits eligible independently compiled applications to use their own license. "
        "PyInstaller's bootloader exception is also preserved.\n\n",
        "The unused GNU Readline extension/library and Pygame FreeSans font are excluded "
        "from this distribution.\n\n",
    ]
    for component in catalog["components"]:
        parts.append(
            f"## {component['name']} — {component['version']}\n\n"
            f"License: {component['license']}\n\n"
            f"Upstream: {component['homepage']}\n\n"
        )
        if component["note"]:
            parts.append(component["note"] + "\n\n")
        for file in component["files"]:
            text = (materials / file["path"]).read_text(
                encoding="utf-8", errors="replace"
            )
            parts.append(f"### {file['path']}\n\n```text\n{text.rstrip()}\n```\n\n")
    return "".join(parts)


def pygame_source(root: Path, destination: Path) -> None:
    """Keep all corresponding library code; omit the unused font from source too."""
    lock = json.loads((root / "packaging/third_party/sources.json").read_text())
    entry = lock["pygame"]
    cache = root / "build/third-party-cache" / entry["filename"]
    cache.parent.mkdir(parents=True, exist_ok=True)
    if not cache.is_file():
        previous = root / "build/license-audit/sources" / entry["filename"]
        if previous.is_file() and digest(previous) == entry["sha256"]:
            shutil.copyfile(previous, cache)
        else:
            request = urllib.request.Request(
                entry["url"], headers={"User-Agent": "Tindahan-Source-Packager"}
            )
            with (
                urllib.request.urlopen(request, timeout=60) as response,
                cache.open("wb") as output,
            ):
                shutil.copyfileobj(response, output)
    if digest(cache) != entry["sha256"]:
        cache.unlink(missing_ok=True)
        raise RuntimeError("Pygame source archive checksum mismatch; build stopped")
    with tarfile.open(cache) as source, tarfile.open(destination, "w:gz") as output:
        for member in source:
            if Path(member.name).name.casefold() == "freesansbold.ttf":
                continue
            if member.isreg():
                body = source.extractfile(member).read()
                if member.name == "pygame-2.6.1/setup.py":
                    before = b'"src_py/freesansbold.ttf",'
                    if before not in body:
                        raise RuntimeError(
                            "Pygame source layout changed; review font exclusion"
                        )
                    body = body.replace(before, b"")
                    body = (
                        b"# Tindahan packaging change, 2026-10-25: omit unused FreeSans data file.\n"
                        + body
                    )
                member.size = len(body)
                output.addfile(member, io.BytesIO(body))
            else:
                output.addfile(member)
        body = (
            "Tindahan source packaging changes, 2026-10-25:\n"
            "Removed unused src_py/freesansbold.ttf and its setup.py data-file entry.\n"
            "No retained Pygame library code was changed for this packaging step.\n"
            "The compiled library uses upstream 2.6.1 code. Copyright notices remain intact.\n"
            f"Original source: {entry['url']}\nSHA-256: {entry['sha256']}\n"
        ).encode()
        info = tarfile.TarInfo("pygame-2.6.1/TINDAHAN-CHANGES.txt")
        info.size = len(body)
        output.addfile(info, io.BytesIO(body))


def application_files(root: Path):
    """Explicit source allowlist: never collect databases, user audio, .git or .env."""
    for name in (
        "main.py",
        ".gitattributes",
        ".gitignore",
        "LICENSE",
        "README.md",
        "THIRD_PARTY_NOTICES.md",
        "requirements.txt",
        "requirements-build.txt",
        "docs/THIRD_PARTY_AUDIT.md",
        "docs/third-party-requirements.csv",
    ):
        path = root / name
        if path.is_file():
            yield path
    yield from root.glob("*.spec")
    for directory in ("core", "db", "ui", "tests", "scripts"):
        yield from (root / directory).rglob("*.py")
    yield from (root / ".github/workflows").glob("*.yml")
    allowed = {".py", ".sh", ".iss", ".json", ".md", ".txt", ".rst"}
    for path in (root / "packaging").rglob("*"):
        if (
            path.is_file()
            and "__pycache__" not in path.parts
            and (path.suffix in allowed or not path.suffix)
        ):
            yield path


def prepare_materials(root: Path, version: str) -> tuple[Path, Path]:
    materials = root / "packaging/third_party"
    stage = root / "build/redistribution"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    notices = render_notices(materials)
    (stage / "THIRD_PARTY_NOTICES.md").write_text(notices, encoding="utf-8")
    shutil.copyfile(materials / "catalog.json", stage / "third-party-manifest.json")
    shutil.copyfile(materials / "SOURCE_CODE.md", stage / "SOURCE_CODE.md")
    for path, relative in catalog_files(materials):
        target = stage / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    work = root / "build/source-work"
    if work.exists():
        shutil.rmtree(work)
    app = work / "application"
    for path in application_files(root):
        if path.is_symlink():
            raise RuntimeError(f"Source snapshot refuses symlink: {path}")
        target = app / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    versions = environment_versions()
    lock = (
        "\n".join(
            f"{name}=={value}" for name, value in versions["distributions"].items()
        )
        + "\n"
    )
    (work / "requirements-release.txt").write_text(lock, encoding="utf-8")
    (work / "environment.json").write_text(
        json.dumps(versions, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copyfile(materials / "SOURCE_CODE.md", work / "SOURCE_CODE.md")
    pygame_source(root, work / "pygame-2.6.1-tindahan-source.tar.gz")
    hashes = {
        str(p.relative_to(work)): digest(p)
        for p in sorted(work.rglob("*"))
        if p.is_file()
    }
    (work / "SHA256.json").write_text(
        json.dumps(hashes, indent=2) + "\n", encoding="utf-8"
    )
    sources = stage / "sources"
    sources.mkdir()
    archive = sources / f"Tindahan-System-{version}-sources.tar.gz"
    with tarfile.open(archive, "w:gz") as output:
        output.add(work, arcname="Tindahan-System-sources")
    return stage, archive


def verify_directory(stage: Path, bundle: Path) -> None:
    for path in stage.rglob("*"):
        if path.is_file():
            target = bundle / path.relative_to(stage)
            if not target.is_file() or digest(target) != digest(path):
                raise RuntimeError(
                    f"Packaged redistribution file missing/changed: {target}"
                )


def verify_wrapper(stage: Path, archive) -> None:
    for path in stage.rglob("*"):
        # Library source travels inside setup's app payload. Uninstall does not use it.
        if path.is_file() and "sources" not in path.relative_to(stage).parts:
            name = path.relative_to(stage).as_posix()
            if name not in archive.toc or hashlib.sha256(
                archive.extract(name)
            ).hexdigest() != digest(path):
                raise RuntimeError(f"Wrapper lacks redistribution file: {name}")
