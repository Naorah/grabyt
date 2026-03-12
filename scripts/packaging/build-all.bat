@echo off
REM Genere les exe FULL et SLIM puis cree pour chaque langue (fr, en, de, es)
REM un dossier dist\full-{lang} et dist\slim-{lang} avec l'exe et config\config.yaml.
REM Usage: scripts\packaging\build-all.bat [--zip]
REM   --zip : lance scripts\packaging\zipversion.bat a la fin pour creer un zip par dossier dans dist\

REM Se placer a la racine du projet
cd /d "%~dp0..\.."

set DOZIP=0
if "%~1"=="--zip" set DOZIP=1

if not exist "venv\Scripts\activate.bat" (
    echo Activez d'abord l'environnement virtuel ou installez PyInstaller: pip install pyinstaller
    exit /b 1
)

call venv\Scripts\activate.bat
pip install pyinstaller pillow -q

echo Generation de l'icone...
python scripts\build\build_icon.py
if not exist "assets\icon.ico" (
    echo Attention: assets\icon.ico absent, exe sans icone.
)

echo.
echo === Build FULL ===
pip install imageio-ffmpeg -q
pyinstaller scripts\build\build_full.spec --noconfirm
if errorlevel 1 (
    echo Echec build full.
    pause
    exit /b 1
)

echo.
echo === Build SLIM ===
pyinstaller scripts\build\build_slim.spec --noconfirm
if errorlevel 1 (
    echo Echec build slim.
    pause
    exit /b 1
)

echo.
echo === Packs par langue (fr, en, de, es) ===
python scripts\packaging\prepare_lang_builds.py
if errorlevel 1 (
    pause
    exit /b 1
)

if %DOZIP%==1 (
    echo.
    echo === Creation des zip ===
    call scripts\packaging\zipversion.bat
)
echo.
echo Termine: dist\GrabYT-full.exe, dist\GrabYT-slim.exe
echo Packs: dist\full-fr, dist\full-en, dist\full-de, dist\full-es
echo       dist\slim-fr, dist\slim-en, dist\slim-de, dist\slim-es
if %DOZIP%==1 echo Zip: dist\*.zip
pause

