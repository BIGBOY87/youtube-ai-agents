@echo off
chcp 65001 >nul
if not exist client_secret.json (
  echo ERROR: Missing client_secret.json
  echo Put the Google OAuth Desktop JSON file in this folder and rename it to client_secret.json
  pause
  exit /b 1
)
python main.py setup
pause
