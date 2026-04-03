import sqlite3
import os

db_path = 'past_questions_v2.db'

def check_empty_exams():
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT e.id, e.name, COUNT(s.id) as subject_count 
            FROM exams e 
            LEFT JOIN subjects s ON e.id = s.exam_id 
            GROUP BY e.id
        """)
        exams = cursor.fetchall()
        print("Exam Subject Counts:")
        for e in exams:
            if e[2] == 0:
                print(f"  [EMPTY] ID: {e[0]}, Name: {e[1]}")
            else:
                print(f"  ID: {e[0]}, Name: {e[1]}, Subjects: {e[2]}")
        
    except Exception as ex:
        print(f"Error: {ex}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_empty_exams()
