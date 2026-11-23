@echo off
cd /d "%~dp0"
py -3.12 -m venv .venv-build
if errorlevel 1 goto python_chybi
.venv-build\Scripts\python.exe -m pip install --only-binary=pygame -r requirements-build.txt
if errorlevel 1 goto chyba
.venv-build\Scripts\python.exe -m unittest discover -s tests -v
if errorlevel 1 goto chyba
.venv-build\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name Jeste_jedno_razitko main.py
if errorlevel 1 goto chyba
echo Hotovo: dist\Jeste_jedno_razitko.exe
pause
exit /b 0
:python_chybi
echo Je potreba Python 3.12 s prikazem py. Nainstaluj jej a spust skript znovu.
pause
exit /b 1
:chyba
echo Sestaveni se nepodarilo. Podivej se na chybu vyse.
pause
exit /b 1
