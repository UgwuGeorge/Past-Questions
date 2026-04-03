import sqlite3
import os

db_path = 'past_questions_v2.db'

def list_users():
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        print("Users in DB:")
        for u in users:
            print(f"  ID: {u[0]}, Username: {u[1]}, Email: {u[2]}")
        
    except Exception as ex:
        print(f"Error: {ex}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_users()
