import sqlite3
from datetime import datetime

DB_PATH = "history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temp TEXT,
            desc TEXT,
            activity TEXT,
            ai_result TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_record(city, temp, desc, activity="", ai_result=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (city, temp, desc, activity, ai_result, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (city, temp, desc, activity, ai_result, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_history(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT city, temp, desc, activity, ai_result, created_at FROM history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"city": r[0], "temp": r[1], "desc": r[2], "activity": r[3], "ai_result": r[4], "created_at": r[5]} for r in rows]