from flask import Flask, render_template, request, jsonify
from datetime import date, datetime
from pathlib import Path
import os, sqlite3

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "wild_within.db"
app = Flask(__name__)

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS runs(
            id INTEGER PRIMARY KEY AUTOINCREMENT, activity_date TEXT NOT NULL,
            distance REAL NOT NULL, seconds INTEGER NOT NULL, source TEXT NOT NULL,
            created_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS activities(
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
            category TEXT NOT NULL, minutes INTEGER NOT NULL, completed_date TEXT)""")
        con.execute("""CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,
            body TEXT NOT NULL, distance REAL NOT NULL DEFAULT 0, created_at TEXT NOT NULL)""")
        if con.execute("SELECT COUNT(*) FROM activities").fetchone()[0] == 0:
            con.executemany("INSERT INTO activities(title,category,minutes) VALUES(?,?,?)", [
                ("Morning run", "Fitness", 20), ("Stretch and recover", "Wellness", 10),
                ("Mindful breathing", "Mindfulness", 5)])
        if con.execute("SELECT COUNT(*) FROM posts").fetchone()[0] == 0:
            con.execute("INSERT INTO posts(username,body,distance,created_at) VALUES(?,?,?,?)",
                ("TrailFriend", "Small steps make strong journeys. Who is joining this week's trail?", 1.5,
                 datetime.now().strftime("%Y-%m-%d %H:%M")))

@app.get("/")
def index():
    today = date.today().isoformat()
    month = date.today().strftime("%Y-%m")
    with connect() as con:
        today_km = con.execute("SELECT COALESCE(SUM(distance),0) FROM runs WHERE activity_date=?", (today,)).fetchone()[0]
        month_km = con.execute("SELECT COALESCE(SUM(distance),0) FROM runs WHERE substr(activity_date,1,7)=?", (month,)).fetchone()[0]
        activities = con.execute("SELECT * FROM activities ORDER BY id DESC").fetchall()
        posts = con.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 30").fetchall()
    return render_template("index.html", today=today, today_km=round(today_km,2),
                           month_km=round(month_km,2), activities=activities, posts=posts)

@app.post("/api/run")
def add_run():
    data = request.get_json(silent=True) or {}
    try:
        km, seconds = float(data.get("distance_km", 0)), int(data.get("duration_seconds", 0))
        source = str(data.get("source", "manual"))[:20]
    except (ValueError, TypeError):
        return jsonify(error="Enter a valid distance and duration."), 400
    if not 0.01 <= km <= 200 or not 0 <= seconds <= 86400:
        return jsonify(error="Distance must be 0.01–200 km and duration 0–1440 minutes."), 400
    with connect() as con:
        con.execute("INSERT INTO runs(activity_date,distance,seconds,source,created_at) VALUES(?,?,?,?,?)",
                    (date.today().isoformat(), km, seconds, source, datetime.now().isoformat(timespec="seconds")))
    return jsonify(ok=True, distance_km=round(km,2), virtual_distance_km=round(km,2))

@app.post("/api/activity")
def add_activity():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title","")).strip()[:80]
    category = str(data.get("category","Custom")).strip()[:30] or "Custom"
    try: minutes = int(data.get("minutes",10))
    except (ValueError,TypeError): return jsonify(error="Duration must be a number."),400
    if not title or not 1 <= minutes <= 1440:
        return jsonify(error="Add a title and duration between 1 and 1440 minutes."),400
    with connect() as con:
        con.execute("INSERT INTO activities(title,category,minutes) VALUES(?,?,?)",(title,category,minutes))
    return jsonify(ok=True)

@app.post("/api/activity/<int:aid>/complete")
def complete_activity(aid):
    with connect() as con:
        cur = con.execute("UPDATE activities SET completed_date=? WHERE id=?", (date.today().isoformat(),aid))
        if cur.rowcount == 0: return jsonify(error="Activity not found."),404
    return jsonify(ok=True)

@app.post("/api/post")
def add_post():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username","TrailSeeker")).strip()[:30] or "TrailSeeker"
    body = str(data.get("body","")).strip()[:500]
    try: distance = max(0,min(200,float(data.get("distance_km",0))))
    except (ValueError,TypeError): distance=0
    if not body: return jsonify(error="Write a message before sharing."),400
    with connect() as con:
        con.execute("INSERT INTO posts(username,body,distance,created_at) VALUES(?,?,?,?)",
                    (username,body,distance,datetime.now().strftime("%Y-%m-%d %H:%M")))
    return jsonify(ok=True)

@app.get("/health")
def health(): return jsonify(status="ok",app="WILD WITHIN")

if __name__ == "__main__":
    init_db()
    app.run(host=os.environ.get("WILD_WITHIN_HOST","127.0.0.1"),
            port=int(os.environ.get("PORT","5055")), debug=False)
