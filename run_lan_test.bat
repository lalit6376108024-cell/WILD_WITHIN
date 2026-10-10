@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (echo Run install.bat first. & pause & exit /b 1)
echo WARNING: Local-network testing only on trusted private Wi-Fi. Not for public internet.
set WILD_WITHIN_HOST=0.0.0.0
set PORT=5055
.\.venv\Scripts\python.exe app.py
pause
