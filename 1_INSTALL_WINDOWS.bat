@echo off
chcp 65001 >nul
echo Installing BANG IT UP MUSIC YouTube AI Agent...
python --version
if errorlevel 1 (
  echo Python is not installed. Install Python 3.10+ from https://www.python.org/downloads/ and tick "Add Python to PATH".
  pause
  exit /b 1
)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Done. Next: put client_secret.json in this folder, then run 2_CONNECT_YOUTUBE_WINDOWS.bat
pause
