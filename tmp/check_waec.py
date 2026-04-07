
import sqlite3
import os

def check_waec_exams():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if exams table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='exams'")
        if not cursor.fetchone():
            print("Table 'exams' does not exist.")
            return

        # List WAEC exams and their status
        print("WAEC Exams found in database:")
        query = "SELECT id, name, category FROM exams WHERE category LIKE '%WAEC%'"
        cursor.execute(query)
        waec_exams = cursor.fetchall()
        
        if not waec_exams:
            print("No WAEC exams found in the 'exams' table.")
            # Let's try searching by name if category is empty
            query = "SELECT id, name, category FROM exams WHERE name LIKE '%WAEC%'"
            cursor.execute(query)
            waec_exams = cursor.fetchall()
        
        for exam_id, name, category in waec_exams:
            # Count questions for this exam
            cursor.execute("SELECT count(*) FROM questions WHERE exam_id = ?", (exam_id,))
            q_count = cursor.fetchone()[0]
            print(f"ID: {exam_id} | Name: {name} | Category: {category} | Question Count: {q_count}")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_waec_exams()
