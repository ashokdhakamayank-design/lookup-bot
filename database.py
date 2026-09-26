import sqlite3
import os

DB_PATH = "data/bot.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS lookups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            number TEXT,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
              (user_id, username, first_name))
    conn.commit()
    conn.close()

def log_lookup(user_id, number, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO lookups (user_id, number, response) VALUES (?, ?, ?)",
              (user_id, number, response))
    conn.commit()
    conn.close()

def total_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    n = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return n

def total_lookups():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    n = c.execute("SELECT COUNT(*) FROM lookups").fetchone()[0]
    conn.close()
    return n

def recent_lookups(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute(
        "SELECT user_id, number, created_at FROM lookups ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return rows

def all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT user_id, username, first_name, joined_at FROM users").fetchall()
    conn.close()
    return rows