import sqlite3
import os

db_path = 'past_questions_v2.db'
if not os.path.exists(db_path):
    print(f"File {db_path} does not exist in current directory.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, category FROM exams LIMIT 10")
        rows = cursor.fetchall()
        print("Raw data from 'exams' table:")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
