@echo off
REM Skrypt do automatycznej instalacji i pobrania narzędzi chemicznych

REM Tworzenie wirtualnego środowiska (jeśli jeszcze nie istnieje)
if not exist env (
    python -m venv env
)

REM Aktywacja środowiska
call env\Scripts\activate.bat

:: 1. Instalacja biblioteki openbabel-wheel
echo Instalowanie openbabel-wheel...
pip install openbabel-wheel

:: 2. Pobranie i rozpakowanie MOPAC
echo Pobieranie MOPAC...
powershell -Command "Invoke-WebRequest -Uri 'http://openmopac.net/mopac-23.1.2-win.zip' -OutFile '..\mopac-23.1.2-win.zip'"
powershell -Command "Expand-Archive -Path '..\mopac-23.1.2-win.zip' -DestinationPath '..\mopac'"
del "..\mopac-23.1.2-win.zip"

:: 3. Pobranie i rozpakowanie JSME
echo Pobieranie JSME...
powershell -Command "Invoke-WebRequest -Uri 'https://jsme-editor.github.io/downloads/JSME_2024-04-29.zip' -OutFile '..\JSME_2024-04-29.zip'"
powershell -Command "Expand-Archive -Path '..\JSME_2024-04-29.zip' -DestinationPath '..\JSME_2024-04-29'"
del "..\JSME_2024-04-29.zip"

:: 4 JMOL
echo Rozpakowywanie gzip do tar w katalogu nadrzednym...
powershell -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [IO.Compression.GzipStream]::new([IO.File]::OpenRead('..\\Jmol-14.0.13-binary.tar.gz'), [IO.Compression.CompressionMode]::Decompress).CopyTo([IO.File]::Create('..\\Jmol-14.0.13-binary.tar'))"

echo Rozpakowywanie tar w katalogu nadrzednym...
tar -xf ..\Jmol-14.0.13-binary.tar -C ..

echo Rozpakowywanie jsmol.zip w katalogu nadrzednym...
powershell -Command "Expand-Archive -Path '..\\jmol-14.0.13/jsmol.zip' -DestinationPath '..\\jmol-14.0.13/jsmol'"

echo Usuwanie archiwów w katalogu nadrzędnym...
del ..\Jmol-14.0.13-binary.tar.gz
del ..\Jmol-14.0.13-binary.tar

echo Instalacja requirements...
pip install -r mopac_portal/requirements.txt 

echo Przenoszenie jmol
cd mopac_portal/
move ../../jmol-14.0.13 media

echo Przenoszenie jsme...
move "..\..\JSME_2024-04-29\jsme" "..\programming_project_WCh_2025\mopac_portal\static"


echo.
echo =============================
echo Wszystko gotowe!
echo =============================
pause
