@echo off
REM Skrypt do automatycznej instalacji i pobrania narzędzi chemicznych

:: 1. Instalacja biblioteki openbabel-wheel
echo Instalowanie openbabel-wheel...
pip install openbabel-wheel

:: 2. Pobranie i rozpakowanie MOPAC
echo Pobieranie MOPAC...
powershell -Command "Invoke-WebRequest -Uri 'http://openmopac.net/mopac-23.1.2-win.zip' -OutFile 'mopac-23.1.2-win.zip'"
powershell -Command "Expand-Archive -Path 'mopac-23.1.2-win.zip' -DestinationPath 'mopac'"

:: 4. Pobranie i rozpakowanie JSME
echo Pobieranie JSME...
powershell -Command "Invoke-WebRequest -Uri 'https://jsme-editor.github.io/downloads/JSME_2024-04-29.zip' -OutFile 'JSME_2024-04-29.zip'"
powershell -Command "Expand-Archive -Path 'JSME_2024-04-29.zip' -DestinationPath 'JSME_2024-04-29'"
del "JSME_2024-04-29.zip"

echo.
echo =============================
echo Wszystko gotowe!
echo =============================
pause
