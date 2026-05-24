@echo off
cd /d "%~dp0"
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install flask requests

echo.
echo PRO εγκατάσταση ολοκληρώθηκε.
echo Τώρα πάτα PRO_RUN_WINDOWS.bat
pause
