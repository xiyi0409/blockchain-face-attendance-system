import sqlite3

DB_NAME = "attendance.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS punch_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            timestamp TEXT,
            gps_lat REAL,
            gps_lng REAL,
            cid TEXT,
            tx_hash TEXT
        )
    """)

    conn.commit()
    conn.close()
