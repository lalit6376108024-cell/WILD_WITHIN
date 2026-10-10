@echo off
cd /d "%~dp0"
py -m venv .venv
if errorlevel 1 (echo Could not create environment. See README.md. & pause & exit /b 1)
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (echo Install failed. Read the error above. & pause & exit /b 1)
echo Installed successfully.
pause
