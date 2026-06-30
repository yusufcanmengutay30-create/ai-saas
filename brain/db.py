import sqlite3
from datetime import datetime

DB_PATH = "factory.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        output TEXT,
        mode TEXT,
        model TEXT,
        viral_score INTEGER,
        viral_level TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_content(prompt, output, mode, model, viral_score, viral_level):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO contents (prompt, output, mode, model, viral_score, viral_level, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        prompt,
        output,
        mode,
        model,
        viral_score,
        viral_level,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_all(limit=50):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM contents
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return rows
