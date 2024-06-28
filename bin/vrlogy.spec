# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules('numpy.f2py')
hiddenimports += collect_submodules('scipy')
hiddenimports += collect_submodules('pythonosc')
hiddenimports += collect_submodules('OpenSSL')


a = Analysis(
    ['vrlogy.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('helpers.py', '.'), ('init_gui.py', '.'), ('launch_setting_gui.py', '.'), ('parameters.py', '.'), ('params.p', '.'), ('tracking.py', '.'), ('vrlogy_auth.py', '.'), ('backends.py', '.'), ('__init__.py', '.')],
    hiddenimports=hiddenimports,
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
    name='vrlogy',
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
)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='vrlogy')
