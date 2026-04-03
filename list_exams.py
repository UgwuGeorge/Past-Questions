import sqlite3
import os

db_path = 'past_questions_v2.db'

def check_exams():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, name, category, sub_category, required_tier FROM exams")
        exams = cursor.fetchall()
        print(f"Exams in DB ({len(exams)}):")
        for e in exams:
            print(f"  ID: {e[0]}, Name: {e[1]}, Cat: {e[2]}, SubCat: {e[3]}, Tier: {e[4]}")
        
        cursor.execute("SELECT count(*) FROM subjects")
        print(f"\nTotal Subjects: {cursor.fetchone()[0]}")
        
    except Exception as ex:
        print(f"Error: {ex}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_exams()
