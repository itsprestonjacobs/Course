import sqlite3

conn = sqlite3.connect("economy.db")
conn.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0,
    last_daily TEXT
)""")
conn.commit()


def _ensure(user_id):
    conn.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))


def get(user_id):
    _ensure(user_id)
    row = conn.execute(
        "SELECT coins, xp, level, last_daily FROM users WHERE user_id=?", (user_id,)
    ).fetchone()
    return {"coins": row[0], "xp": row[1], "level": row[2], "last_daily": row[3]}


def add(user_id, coins=0, xp=0):
    _ensure(user_id)
    conn.execute("UPDATE users SET coins=coins+?, xp=xp+? WHERE user_id=?",
                 (coins, xp, user_id))
    conn.commit()


def set_level(user_id, level):
    conn.execute("UPDATE users SET level=? WHERE user_id=?", (level, user_id))
    conn.commit()


def set_daily(user_id, when):
    conn.execute("UPDATE users SET last_daily=? WHERE user_id=?", (when, user_id))
    conn.commit()


def top(limit=10):
    return conn.execute(
        "SELECT user_id, coins, level FROM users ORDER BY coins DESC LIMIT ?", (limit,)
    ).fetchall()
