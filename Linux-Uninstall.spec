# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

project = Path(SPECPATH)
a = Analysis(
    [str(project / 'packaging/linux/setup.py')], pathex=[str(project)], binaries=[],
    datas=[
        (str(project / 'build/linux-installer/version.txt'), '.'),
        (str(project / 'packaging/linux/uninstall-mode'), '.'),
        (str(project / 'LICENSE'), '.'),
        (str(project / 'build/redistribution/THIRD_PARTY_NOTICES.md'), '.'),
        (str(project / 'build/redistribution/third-party-manifest.json'), '.'),
        (str(project / 'build/redistribution/SOURCE_CODE.md'), '.'),
        (str(project / 'build/redistribution/licenses'), 'licenses'),
    ],
    hiddenimports=[], hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=['readline'],
    noarchive=False, optimize=0,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [], name='Tindahan-Uninstall',
    debug=False, bootloader_ignore_signals=False, strip=False, upx=False,
    console=False, disable_windowed_traceback=False,
)
