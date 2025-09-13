import sqlite3
from datetime import datetime

def create_tables():
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bmi REAL,
        category TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

def get_or_create_user(username):
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if user:
        conn.close()
        return user[0]
    c.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

def save_bmi_record(user_id, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO bmi_records (user_id, bmi, category, date) VALUES (?, ?, ?, ?)",
              (user_id, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_bmi_history(user_id):
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute("SELECT date, bmi FROM bmi_records WHERE user_id = ? ORDER BY date", (user_id,))
    records = c.fetchall()
    conn.close()
    return records
