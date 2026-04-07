
import sqlite3

def list_waec_math_subjects():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM subjects WHERE name LIKE '%Mathematics%' AND exam_id = 2")
    res = cursor.fetchall()
    for row in res:
        cursor.execute("SELECT COUNT(*) FROM questions WHERE subject_id = ?", (row[0],))
        count = cursor.fetchone()[0]
        print(f"ID: {row[0]} | Name: {row[1]} | Questions: {count}")
        
    conn.close()

if __name__ == "__main__":
    list_waec_math_subjects()
