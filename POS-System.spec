# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

project = Path(SPECPATH)
a = Analysis(
    [str(project / 'main.py')],
    pathex=[str(project)],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['readline'],
    noarchive=False,
    optimize=0,
)
# Checkout uses pygame.mixer and Tk fonts; its bundled default font is unused.
a.datas = [entry for entry in a.datas if Path(entry[0]).name.casefold() != 'freesansbold.ttf']
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='POS-System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='POS-System')
