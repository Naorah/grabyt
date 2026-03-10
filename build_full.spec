# PyInstaller spec: version FULL (avec imageio-ffmpeg, exe portable).
# Lancer: pyinstaller build_full.spec
# Generer l'icone avant: python scripts/build_icon.py

import os

block_cipher = None

_spec_dir = os.path.dirname(os.path.abspath(SPEC))
icon_path = os.path.normpath(os.path.join(_spec_dir, 'assets', 'icon.ico'))
_assets_dir = os.path.join(_spec_dir, 'assets')
datas_assets = [(_assets_dir, 'assets')] if os.path.isdir(_assets_dir) else []

# Modules PyQt6 non utilises (on garde Core, Gui, Widgets, Svg)
_excludes_qt = [
    'PyQt6.QtWebEngine', 'PyQt6.QtWebEngineCore', 'PyQt6.QtWebEngineWidgets',
    'PyQt6.QtMultimedia', 'PyQt6.QtMultimediaWidgets',
    'PyQt6.QtBluetooth', 'PyQt6.QtDBus', 'PyQt6.QtDesigner', 'PyQt6.QtHelp',
    'PyQt6.QtLocation', 'PyQt6.QtNetworkAuth', 'PyQt6.QtNfc',
    'PyQt6.QtOpenGL', 'PyQt6.QtOpenGLWidgets', 'PyQt6.QtPositioning',
    'PyQt6.QtPrintSupport', 'PyQt6.QtQml', 'PyQt6.QtQuick', 'PyQt6.QtQuickWidgets',
    'PyQt6.QtRemoteObjects', 'PyQt6.QtSensors', 'PyQt6.QtSerialPort',
    'PyQt6.QtSql', 'PyQt6.QtTest', 'PyQt6.QtWebChannel', 'PyQt6.QtWebSockets',
    'PyQt6.QtXml',
]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas_assets,
    hiddenimports=[
        "yaml",
        "PyQt6.QtSvg",
        "imageio_ffmpeg",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=_excludes_qt,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="GrabYT-full",
    icon=icon_path if os.path.isfile(icon_path) else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
