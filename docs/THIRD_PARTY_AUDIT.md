# Third-party redistribution audit

Updated 2026-10-25. The reviewed local Linux distribution now packages its
third-party notices and accompanying source materials. Tindahan's own code
remains MIT; incorporated dependencies retain their respective terms.

## Packaged materials

- `THIRD_PARTY_NOTICES.md`: prominent Pygame LGPL notice, FreeType/IJG credits,
  selected alternative licenses, and the full collected copyright/license texts.
- `packaging/third_party/licenses/`: 81 preserved notice, license, patent and
  attribution files covering 47 catalog entries. Some helper-tree notices are
  retained conservatively even where the upstream library uses them only in tools.
- `packaging/third_party/catalog.json`: component versions, origins, selected terms
  and SHA-256 hashes. Each app gets this as `third-party-manifest.json`.
- `SOURCE_CODE.md`: permission to modify/debug, library source locations and
  practical source rebuild/repackaging instructions.
- `sources/Tindahan-System-<version>-sources.tar.gz`: the matching application
  source, build scripts, packaging recipes, tests, notices, release dependency
  versions, reviewed inventory, Pygame source and a SHA-256 file manifest. This
  archive also has a separate release download and checksum.

The app folder and portable package include all these materials. The Linux setup
embeds the app payload, including its source archive, and also carries its own
readable notices. The standalone uninstaller carries the notices for its runtime;
its code does not use Pygame. The app, setup and uninstaller have a **Licenses**
viewer with a save-copy option and source/rebuild instructions.

## Pygame source delivery

Pygame 2.6.1 is retained for optional checkout audio. Its library source and the
application source accompany each app copy, using the source-accompanying route
in LGPL sections 4 and 6(a). No future source-offer service is relied on.
See the [actual LGPL text](https://www.pygame.org/docs/LGPL.txt).

The original source archive is pinned in `packaging/third_party/sources.json`:

- Origin: the Pygame 2.6.1 source distribution on PyPI.
- SHA-256: `56fb02ead529cee00d415c3e007f75e0780c655909aaa8e8bf616ee09c9feb1f`.
- Local pip wheel-cache origin metadata matches that archive and checksum.
- All retained library code, headers and build machinery remain available.
- The source-delivery archive omits the unused `freesansbold.ttf` and removes its
  `setup.py` data-file entry. The packaging change is dated and documented in
  `TINDAHAN-CHANGES.txt`; retained library code is unchanged.
- The supplied source was rebuilt into a Python 3.14 wheel. It contains no
  FreeSans font. Running the application against that rebuilt library passed
  the temporary-store screen, audio and PDF smoke checks.

The source snapshot uses an explicit allowlist. It excludes store databases,
Git history, virtual environments, environment files, build outputs and personal
checkout recordings. The original Pygame source archive is a download cache,
not a published release file; only the documented font-excluded source is shipped.

## Other retained components

The [component checklist](third-party-requirements.csv) retains the audited
versions, terms and provenance. The machine-readable catalog and preserved texts
are the distribution materials; a checklist entry is not a substitute for them.

- Python, Tcl/Tk, ReportLab, Pillow, charset-normalizer, PyInstaller and the system
  libraries have their collected notices. Apache runtime-hook copyright headers
  are preserved along with the Apache terms. PyInstaller's bootloader exception
  permits a separate application license; see its [license documentation](https://pyinstaller.org/en/stable/license.html).
- Pillow codec notices include libavif, libaom, dav1d, libyuv, libwebp/sharpyuv,
  libjpeg-turbo/IJG, Little CMS, libtiff, OpenJPEG, libxcb, libXau, liblzma and Zstd,
  with the wheel SBOMs. Optional components listed in an upstream SBOM are not
  automatically described as shipped. libimagequant and Pillow's optional
  FreeType/HarfBuzz/FriBiDi runtime libraries are absent from this frozen app.
- libavif 1.4.2's libyuv pin is
  `644251f252a84bf8ce91ff0aca86a9b16b069ab8`, matching runtime version 1924.
  LICENSE, AUTHORS and PATENTS are preserved. Pinned libaom helper notices and
  dav1d's ISC-licensed assembly helper notice are also collected.
- FreeType uses FTL, Zstd uses BSD, libuuid uses its BSD terms, and the shipped
  liblzma uses 0BSD. Generic distro source-package labels that include unrelated
  GPL utilities are not substituted for those component terms. libuuid's actual
  source copyright notices accompany the BSD text.
- GCC runtime terms include GPLv3 and GCC Runtime Library Exception 3.1, alongside
  their recorded distro versions. The reviewed independently compiled application
  uses the runtime exception; it is not described as distributing plain GPL-only
  libraries. See the [GCC runtime terms](https://gcc.gnu.org/onlinedocs/libstdc++/manual/license.html).
- SDL2_mixer 2.8.2's actual Zlib-style notice is preserved despite the distro's
  broader MIT metadata label.

Pillow/ReportLab source archives collected during the original audit are retained
locally as evidence. Their selected permissive terms do not require shipping
those entire source trees. The Pygame source delivery is packaged separately as
explained above.

## Exclusions and release checks

GNU Readline's extension/library and the unused Pygame FreeSans font remain
excluded. ncurses is also absent after removing Readline. The build inspects the
frozen executables and Python module archives, and refuses to ship either
excluded component. The nested source archive excludes the font as well.

`scripts/third_party.py` hashes the third-party files recorded in the final
PyInstaller PKG/COLLECT manifests, plus imported Python sources in Analysis.
Discarded Analysis data candidates are not treated as shipped files. Hashes and
runtime versions must match a reviewed profile before release packaging proceeds.
The profile also binds the notice catalog's checksum, so removing or replacing
component notices cannot silently reuse an earlier review. Git attributes preserve
the collected notice bytes across Windows and Linux checkouts.
New or changed dependencies stop the release and leave candidate evidence in
`build/third-party-inventory-*.json`; an old profile is not reused as approval for
different binaries. The current profile covers CachyOS x86-64/Python 3.14.8.

Build checks verify the actual app's materials and the texts embedded in both
one-file wrappers. The graphical installer smoke check also checks notices and
source delivery after install/update. Reports include:

- `build/third-party-checks.json`
- `build/exclusion-checks.json`
- `build/bundle-smoke.json`
- `build/installer-smoke.json`
- `build/uninstaller-smoke.json`

The source and notice regression tests also check private-data exclusion,
discarded-font handling, changed libraries, tampered notices and missing package
materials. These checks document packaging evidence; they do not certify every
possible future build or assign MIT to third-party components.

## Remaining platform review

Windows has not been built here. The first Windows and Ubuntu CI inventories must
be reviewed against their own DLLs/libraries, wheel licenses/SBOMs, Python runtime
and installer compiler components before publishable packages are generated.
The build writes candidate inventory evidence and CI uploads it with the
PyInstaller manifests. The current Linux notices/profile are not Windows or
Ubuntu approval. Inno Setup's actual version and applicable embedded notices are
part of that Windows step.
