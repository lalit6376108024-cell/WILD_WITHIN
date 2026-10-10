# WILD WITHIN — VS Code test project

## Run on Windows
1. Extract the ZIP.
2. Open the extracted folder in VS Code (**File → Open Folder**).
3. Open **Terminal → New Terminal**. The terminal must be in the folder containing `app.py`.
4. Run each command separately:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

5. Open http://127.0.0.1:5055. Keep the terminal open; stop with Ctrl+C.
6. If `py` isn't recognized, use `python`. If port 5055 is busy, run `$env:PORT=5056` before starting, then open http://127.0.0.1:5056.

You can also double-click `install.bat` once and then `run_local.bat`.

## Let people test on the same trusted Wi-Fi
1. Run `install.bat`.
2. Double-click `run_lan_test.bat`.
3. Run `ipconfig` and find the IPv4 address of your active Wi-Fi adapter.
4. Testers on the same Wi-Fi open `http://YOUR-IP:5055` using your actual IPv4 address.
5. If Windows Firewall asks, allow only on a trusted Private network.
6. Stop the app with Ctrl+C. Never expose Flask's development server directly to the public internet.

## What this prototype includes
- Responsive nature-inspired dashboard
- Browser GPS distance tracking while page is open
- 1:1 distance matching for the virtual journey
- Manual demo entries marked as not GPS verified
- SQLite persistence for local runs, activities and demo posts
- Custom activities and completion
- 2 km Riverstone Crossing / Glacier Lookout mission

## Limitations
- The community feed is local to the machine and is not a real multi-user cloud feed.
- No accounts, authentication, cloud sync, push notifications, live video or moderation yet.
- Browser GPS can pause when the tab is backgrounded or phone locks, and GPS can drift.
- The virtual landscape is an interactive illustration, not a 3D game.
- Before public internet testing, add authentication, cloud storage, server-side authorization, privacy controls, reporting/blocking and secure hosting. Do not store sensitive data in this prototype.

## Folder contents
`app.py`, `requirements.txt`, `templates/index.html`, `static/app.js`, `static/style.css`, `install.bat`, `run_local.bat`, `run_lan_test.bat`.
