# Library source and rebuilding

Tindahan System uses Pygame for optional checkout audio. Pygame and its use are
covered by the GNU Lesser General Public License, version 2.1 or later. See
`licenses/python-pygame/LGPL.txt` and the incorporated helper notices. Tindahan's
own code remains MIT licensed.

The installed application folder includes
`sources/Tindahan-System-<version>-sources.tar.gz`. The same archive is a separate
release download. The graphical setup carries it inside its application payload;
installing or unpacking that payload gives access to it without another download.
The standalone uninstaller has its runtime notices but does not use Pygame.

The archive contains:

- `application/`: this release's application, build scripts, specifications,
  installer code, tests, dependency notices and reviewed inventory profiles.
- `pygame-2.6.1-tindahan-source.tar.gz`: all retained Pygame source code, headers,
  build machinery and original copyright/license notices. The unused FreeSans
  font and its `setup.py` data-file entry are removed. The dated changes are
  documented inside the library source; retained library code is unchanged.
- `requirements-release.txt`, `environment.json` and `SHA256.json`: dependency
  versions, build environment information, and hashes of the supplied materials.

The source delivery accompanies the binaries, using the source-accompanying
route in LGPL sections 4 and 6(a). There is no promise that you must depend on a
future written source offer. Keep this archive with copies you redistribute.

## Modify and run with a rebuilt library

Unpack the source archive and work inside `Tindahan-System-sources`. Use Python
with Tk support, a C compiler and SDL2 development headers/libraries. For checkout
audio, SDL2_mixer headers/libraries are needed too. The reviewed local Linux
build uses Python 3.14.8, GCC 16, SDL2 compatibility 2.32.74 and SDL2_mixer 2.8.2;
the full system package versions are recorded in the reviewed profile. An
equivalent development environment can be used for a modified build.

On Arch/CachyOS, the core development packages are `base-devel`, `python`, `tk`,
`sdl2-compat`, `sdl2_mixer` and `freetype2`. On Debian/Ubuntu, the corresponding
development packages include `build-essential`, `python3-dev`, `python3-venv`,
`python3-tk`, `libsdl2-dev`, `libsdl2-mixer-dev` and `libfreetype6-dev`.
Optional SDL image/font features may need their own development packages;
Tindahan checkout requires the mixer.

```sh
python3 -m venv rebuild-env
rebuild-env/bin/python -m pip install setuptools wheel
tar -xzf pygame-2.6.1-tindahan-source.tar.gz
# Edit the retained pygame-2.6.1 source here if desired.
rebuild-env/bin/python -m pip install --no-deps --no-build-isolation --no-cache-dir --force-reinstall ./pygame-2.6.1
rebuild-env/bin/python -m pip install -r requirements-release.txt
rebuild-env/bin/python -c "import pygame.mixer; print(pygame.mixer.get_sdl_mixer_version())"
cd application
TINDAHAN_DATA_DIR=/tmp/tindahan-rebuild-check ../rebuild-env/bin/python main.py
```

On Windows use `py -m venv rebuild-env` and `rebuild-env\Scripts\python.exe` in
place of the Unix interpreter paths; extract the tar archives with an archive
tool. A Windows-compatible C toolchain and SDL development libraries are needed
to compile Pygame. Windows-specific binary/notices review is a separate release
step; these materials describe the verified Linux distribution.

## Produce a modified executable

After installing your rebuilt Pygame in that environment, from `application/`:

```sh
../rebuild-env/bin/python -m PyInstaller --noconfirm --clean POS-System.spec
```

The resulting on-directory executable loads that environment's rebuilt Pygame.
Copy `THIRD_PARTY_NOTICES.md`, `licenses/`, `third-party-manifest.json`,
`SOURCE_CODE.md`, and `sources/` from the original installation into the modified
app folder if you want its original notices available there. For redistribution
of your changes, update the source archive, notices and provenance accordingly.

The release command `scripts/build.py` checks a reviewed inventory before making
publishable packages. Changing a dependency intentionally changes its hashes;
this check does not prevent local modifications using the direct PyInstaller
command above. For a new release, review the generated
`build/third-party-inventory-*.json`, collect any new notices/source requirements,
and update `packaging/third_party/profiles/` to describe the actual dependencies.
Do not reuse approval for different binaries or simply remove the check.

You may modify this application for your own use and reverse engineer it for
debugging those modifications. No signing key, online activation, or permission
from Saiken Studio is required to run your rebuilt copy. These instructions
describe a functional rebuild, not a promise of byte-identical compiler output.
