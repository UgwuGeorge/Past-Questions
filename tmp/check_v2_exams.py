
import sqlite3

def check_v2_exams():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_core/past_questions_v2.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM exams")
    res = cursor.fetchall()
    for row in res:
        print(f"Exam ID: {row[0]} | Name: {row[1]}")
        
    conn.close()

if __name__ == "__main__":
    check_v2_exams()
