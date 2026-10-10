@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (echo Run install.bat first. & pause & exit /b 1)
set WILD_WITHIN_HOST=127.0.0.1
set PORT=5055
.\.venv\Scripts\python.exe app.py
pause
