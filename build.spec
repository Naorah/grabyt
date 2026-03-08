# PyInstaller spec pour generer l'exe.
# Lancer: pyinstaller build.spec
# Generer l'icone avant: python scripts/build_icon.py

import os

block_cipher = None

# Icone de l'exe: chemin absolu par rapport au dossier du .spec
_spec_dir = os.path.dirname(os.path.abspath(SPEC))
icon_path = os.path.normpath(os.path.join(_spec_dir, 'assets', 'icon.ico'))

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        "yaml",
        "PyQt6.QtSvg",
        "imageio_ffmpeg",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name="GrabYT",
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
