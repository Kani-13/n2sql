import sqlite3
from models import Feedback, ImplicitLog

def init_db():
    with sqlite3.connect("logs.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                sql TEXT,
                rating INTEGER,
                comments TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interaction_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                generated_sql TEXT
            )
        """)

def save_feedback(fb: Feedback):
    with sqlite3.connect("logs.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (question, sql, rating, comments) VALUES (?, ?, ?, ?)",
            (fb.question, fb.sql, fb.rating, fb.comments)
        )
        conn.commit()

def log_interaction(log: ImplicitLog):
    with sqlite3.connect("logs.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO interaction_log (question, generated_sql) VALUES (?, ?)",
            (log.question, log.generated_sql)
        )
        conn.commit()
