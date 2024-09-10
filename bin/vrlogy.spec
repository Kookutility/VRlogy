# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Requirements 파일을 읽고 패키지 이름을 추출
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

# pythonosc의 하위 모듈 명시적으로 추가
hiddenimports = required_packages + [
    'pythonosc.osc_bundle_builder',
    'pythonosc.osc_message_builder',
    'pythonosc.udp_client',
    'helpers', 
    'init_gui',
    'launch_setting_gui',
    'parameters',
    'tracking',
    'vrlogy_auth',
    'backends',
    'walking_detect',
    'bug_report_gui',
]

a = Analysis(
    ['vrlogy.py'],
    pathex=['bin/'],
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
        ('walking_detect.py', '.'),
        ('bug_report_gui.py', '.'),
        ('saved_params.json', '.'),
        ('C:\\Users\\kook\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\mediapipe\\modules', 'mediapipe/modules')
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,  # 데이터 파일과 바이너리를 포함하기 위해 False로 설정
    name='vrlogy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='assets/icon/VRlogy_icon.ico'
)

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
