"""Release materials must follow the binaries and exclude private store files."""

import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts import third_party


class RedistributionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.root = self.directory / "project"
        self.root.mkdir()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_source_snapshot_excludes_store_data_history_audio_and_environment(self):
        keep = [
            "main.py",
            "core/auth.py",
            "ui/license_ui.py",
            "scripts/build.py",
            "packaging/linux/setup.py",
            "packaging/third_party/licenses/example/LICENSE",
        ]
        private = [
            "pos.db",
            ".env",
            ".git/config",
            "assets/sounds/checkout.mp3",
            ".venv/example.py",
            "core/private.db",
            "packaging/private.sqlite",
            "build/old.py",
        ]
        for name in keep + private:
            self.write(name, "fixture")
        snapshot = {
            path.relative_to(self.root).as_posix()
            for path in third_party.application_files(self.root)
        }
        self.assertEqual(snapshot, set(keep))

    def test_notice_tampering_stops_material_assembly(self):
        body = self.write("packaging/third_party/licenses/example/LICENSE", "original")
        materials = body.parents[2]
        self.write(
            "packaging/third_party/catalog.json",
            json.dumps(
                {
                    "components": [
                        {
                            "id": "example",
                            "files": [
                                {
                                    "path": "licenses/example/LICENSE",
                                    "sha256": third_party.digest(body),
                                }
                            ],
                        }
                    ]
                }
            ),
        )
        self.assertEqual(len(list(third_party.catalog_files(materials))), 1)
        body.write_text("replaced")
        with self.assertRaisesRegex(RuntimeError, "missing or changed"):
            list(third_party.catalog_files(materials))

    def test_inventory_checks_final_data_and_binaries_not_discarded_candidates(self):
        library = self.directory / "native.so"
        library.write_bytes(b"retained library")
        font = self.directory / "freesansbold.ttf"
        font.write_bytes(b"excluded")
        self.write(
            "build/POS-System/Analysis-00.toc",
            repr([("freesansbold.ttf", str(font), "DATA")]),
        )
        self.write(
            "build/POS-System/COLLECT-00.toc",
            repr([("native.so", str(library), "BINARY")]),
        )
        files = third_party.inventory(self.root, "POS-System")
        self.assertEqual([file["destination"] for file in files], ["native.so"])

    def test_unreviewed_or_changed_library_stops_release_and_writes_evidence(self):
        library = self.directory / "native.so"
        library.write_bytes(b"reviewed")
        self.write(
            "build/POS-System/COLLECT-00.toc",
            repr([("native.so", str(library), "BINARY")]),
        )
        reviewed = third_party.inventory(self.root, "POS-System")
        catalog = self.write("packaging/third_party/catalog.json", "{}")
        self.write(
            "packaging/third_party/profiles/test.json",
            json.dumps(
                {
                    "environment": third_party.environment_versions(),
                    "catalog_sha256": third_party.digest(catalog),
                    "artifacts": {"POS-System": reviewed},
                }
            ),
        )
        self.assertEqual(
            third_party.check_inventory(self.root, "POS-System")["files_checked"], 1
        )
        library.write_bytes(b"different library with same filename")
        with self.assertRaisesRegex(RuntimeError, "license review needed"):
            third_party.check_inventory(self.root, "POS-System")
        report = self.root / "build/third-party-inventory-POS-System.json"
        self.assertEqual(
            json.loads(report.read_text())["files"][0]["sha256"],
            third_party.digest(library),
        )
        library.write_bytes(b"reviewed")
        catalog.write_text('{"components": []}')
        with self.assertRaisesRegex(RuntimeError, "license review needed"):
            third_party.check_inventory(self.root, "POS-System")

    def test_library_source_keeps_code_and_notices_and_omits_unused_font(self):
        archive = self.root / "build/license-audit/sources/pygame-2.6.1.tar.gz"
        archive.parent.mkdir(parents=True)
        code = b"/* original LGPL copyright */\nint example(void) { return 1; }\n"
        entries = {
            "pygame-2.6.1/src_c/mixer.c": code,
            "pygame-2.6.1/docs/LGPL.txt": b"library license text",
            "pygame-2.6.1/src_py/freesansbold.ttf": b"unused font",
            "pygame-2.6.1/setup.py": b'data_files=["src_py/freesansbold.ttf", "src_py/icon.bmp"]\n',
        }
        with tarfile.open(archive, "w:gz") as output:
            for name, body in entries.items():
                info = tarfile.TarInfo(name)
                info.size = len(body)
                output.addfile(info, io.BytesIO(body))
        self.write(
            "packaging/third_party/sources.json",
            json.dumps(
                {
                    "pygame": {
                        "filename": archive.name,
                        "url": "https://example.invalid/source",
                        "sha256": third_party.digest(archive),
                    }
                }
            ),
        )
        target = self.directory / "source.tar.gz"
        third_party.pygame_source(self.root, target)
        with tarfile.open(target) as result:
            self.assertEqual(
                result.extractfile("pygame-2.6.1/src_c/mixer.c").read(), code
            )
            self.assertNotIn("pygame-2.6.1/src_py/freesansbold.ttf", result.getnames())
            self.assertIn("pygame-2.6.1/TINDAHAN-CHANGES.txt", result.getnames())
            setup = result.extractfile("pygame-2.6.1/setup.py").read()
            self.assertNotIn(b"freesansbold.ttf", setup)
            compile(setup, "setup.py", "exec")

    def test_missing_packaged_notice_is_detected(self):
        stage = self.root / "stage"
        bundle = self.root / "bundle"
        stage.mkdir()
        bundle.mkdir()
        (stage / "THIRD_PARTY_NOTICES.md").write_text("notices")
        with self.assertRaisesRegex(RuntimeError, "missing/changed"):
            third_party.verify_directory(stage, bundle)

    def test_wrapper_verification_checks_notice_contents(self):
        self.write("stage/licenses/example/LICENSE", "correct")

        class Archive:
            toc = {"licenses/example/LICENSE": None}

            def extract(self, name):
                return b"incorrect"

        with self.assertRaisesRegex(RuntimeError, "lacks redistribution"):
            third_party.verify_wrapper(self.root / "stage", Archive())

    def test_vendored_release_notice_catalog_matches_its_hashes(self):
        self.assertGreater(
            len(list(third_party.catalog_files(third_party.MATERIALS))), 60
        )
