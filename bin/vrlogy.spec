# vrlogy.spec

from PyInstaller.utils.hooks import collect_submodules
import os

# Base path to the mediapipe resources
mediapipe_base_path = "C:/Users/kook/anaconda3/mediapipe/modules"

# Collecting necessary submodules from the required libraries
hidden_imports = collect_submodules('numpy.f2py') + \
                 collect_submodules('scipy') + \
                 collect_submodules('pythonosc') + \
                 collect_submodules('PIL') + \
                 collect_submodules('mediapipe')

# Defining the Analysis class, which is responsible for finding
# and analyzing all the Python scripts, modules, and data files
a = Analysis(
    ['vrlogy.py'],  # The main script
    pathex=['.'],  # Path to the current directory
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('helpers.py', '.'),
        ('init_gui.py', '.'),
        ('launch_setting_gui.py', '.'),
        ('parameters.py', '.'),
        ('tracking.py', '.'),
        ('vrlogy_auth.py', '.'),
        ('backends.py', '.'),
        ('vrlogy.py', '.'),
        ('saved_params.json', '.'),
        (mediapipe_base_path, 'mediapipe/modules')
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None
)

# Creating a PYZ file, which is a PyInstaller archive format
# containing all the pure Python modules in a single file
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Creating the EXE class, which is responsible for generating
# the final executable file from the analyzed data and modules
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
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
    icon='assets/icon/VRlogy_icon.ico'  # Adding the icon file
)

# Collecting all the elements together to be included in the build
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='vrlogy'
)
