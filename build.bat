@echo off
REM Genere l'exe Windows dans dist\
REM Usage: build.bat [--build full|slim]
REM   full = avec imageio-ffmpeg (exe plus lourd, portable)
REM   slim = sans ffmpeg inclus (exe leger, ffmpeg requis sur le systeme)
REM Defaut: full

set BUILD=full
if "%~1"=="--build" if not "%~2"=="" set BUILD=%~2

if not exist "venv\Scripts\activate.bat" (
    echo Activez d'abord l'environnement virtuel ou installez PyInstaller: pip install pyinstaller
    exit /b 1
)

call venv\Scripts\activate.bat
pip install pyinstaller pillow -q

echo Generation de l'icone...
python scripts\build_icon.py
if not exist "assets\icon.ico" (
    echo Attention: assets\icon.ico absent, exe sans icone.
)

if "%BUILD%"=="slim" (
    echo Build SLIM: sans imageio-ffmpeg. ffmpeg doit etre installe sur le systeme.
    pyinstaller build_slim.spec --noconfirm
) else (
    echo Build FULL: avec imageio-ffmpeg.
    pip install imageio-ffmpeg -q
    pyinstaller build_full.spec --noconfirm
)

echo.
if exist "dist\GrabYT.exe" (
    echo Exe genere: dist\GrabYT.exe
    echo Si l'icone ne s'affiche pas: renommer l'exe ou redemarrer l'explorateur.
) else (
    echo Echec du build.
)
pause
