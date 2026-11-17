@echo off
cd /d "%~dp0"
python -m pip install -r requirements-build.txt
if errorlevel 1 goto chyba
python -m unittest discover -s tests -v
if errorlevel 1 goto chyba
python -m PyInstaller --noconfirm --clean --onefile --windowed --name Jeste_jedno_razitko main.py
if errorlevel 1 goto chyba
echo Hotovo: dist\Jeste_jedno_razitko.exe
pause
exit /b 0
:chyba
echo Sestaveni se nepodarilo. Podivej se na chybu vyse.
pause
exit /b 1
