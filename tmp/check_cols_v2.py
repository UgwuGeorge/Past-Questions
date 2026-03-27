import sqlite3
import os

db_path = 'past_questions_v2.db'
def check_cols():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(exams)")
    cols = [row[1] for row in cursor.fetchall()]
    print(f"Exams columns: {cols}")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables: {tables}")
    conn.close()

if __name__ == '__main__':
    check_cols()
