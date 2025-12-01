import sqlite3
import os

# 資料庫路徑：放在 database 資料夾旁邊
DB_PATH = os.path.join(os.path.dirname(__file__), "attendance.db")


def get_connection():
    """取得 SQLite 連線"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # 查詢時可以用欄位名稱
    return conn


def init_db():
    """初始化資料庫與資料表"""
    conn = get_connection()
    cur = conn.cursor()

    # 員工基本資料
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT
        )
    """)

    # 打卡紀錄
    cur.execute("""
        CREATE TABLE IF NOT EXISTS punch_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            timestamp INTEGER,
            gps_lat REAL,
            gps_lng REAL,
            cid TEXT,
            tx_hash TEXT
        )
    """)

    # GPS 軌跡紀錄（背景上傳用）
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gps_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            timestamp INTEGER,
            gps_lat REAL,
            gps_lng REAL
        )
    """)

    conn.commit()
    conn.close()


# ======= 寫入函式 =======

def insert_employee(employee_id: str, name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO employees (employee_id, name)
        VALUES (?, ?)
    """, (employee_id, name))
    conn.commit()
    conn.close()


def insert_record(employee_id, timestamp, gps_lat, gps_lng, cid, tx_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO punch_logs (employee_id, timestamp, gps_lat, gps_lng, cid, tx_hash)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (employee_id, timestamp, gps_lat, gps_lng, cid, tx_hash))
    conn.commit()
    conn.close()


def insert_gps_log(employee_id, timestamp, gps_lat, gps_lng):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO gps_logs (employee_id, timestamp, gps_lat, gps_lng)
        VALUES (?, ?, ?, ?)
    """, (employee_id, timestamp, gps_lat, gps_lng))
    conn.commit()
    conn.close()


# ======= 查詢函式 =======

def get_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, name FROM employees")
    rows = cur.fetchall()
    conn.close()

    return [
        {"employee_id": r["employee_id"], "name": r["name"]}
        for r in rows
    ]


def get_records():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT employee_id, timestamp, gps_lat, gps_lng, cid, tx_hash
        FROM punch_logs
        ORDER BY timestamp DESC
    """)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "employee_id": r["employee_id"],
            "timestamp": r["timestamp"],
            "gps_lat": r["gps_lat"],
            "gps_lng": r["gps_lng"],
            "cid": r["cid"],
            "tx_hash": r["tx_hash"],
        }
        for r in rows
    ]
