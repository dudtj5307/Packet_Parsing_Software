# -*- mode: python ; coding: utf-8 -*-


import glob

png_files = [(f, 'GUI\\res') for f in glob.glob('GUI\\res\\*.png')]
ico_files  = [(f, 'GUI\\res') for f in glob.glob('GUI\\res\\*.ico')]

print(png_files, ico_files)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=png_files+ico_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PPS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['GUI\\res\\PPS.ico'],
)
