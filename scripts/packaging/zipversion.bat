@echo off
REM Cree un zip par dossier dans dist\ (full-fr.zip, full-en.zip, slim-fr.zip, etc.).
REM A lancer apres build-all.bat. Requiert PowerShell.

set DIST=dist
if not exist "%DIST%" (
    echo Dossier %DIST% introuvable. Lancez d'abord le build.
    exit /b 1
)

echo Creation des archives dans %DIST%\...
for /d %%D in ("%DIST%\*") do (
    powershell -NoProfile -Command "Compress-Archive -Path '%%D' -DestinationPath '%%D.zip' -Force"
    if errorlevel 1 (echo   Echec: %%~nxD) else (echo   %%~nxD.zip)
)
echo Termine.
pause

