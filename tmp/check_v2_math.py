
import sqlite3

def check_v2_math():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_core/past_questions_v2.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, exam_id FROM subjects WHERE id = 138")
    res = cursor.fetchone()
    print(f"Subject in V2: {res}")
    
    # Check other subjects in V2 with 'Mathematics' in name
    cursor.execute("SELECT id, name, exam_id FROM subjects WHERE name LIKE '%Mathematics%'")
    res = cursor.fetchall()
    for row in res:
        cursor.execute("SELECT COUNT(*) FROM questions WHERE subject_id = ?", (row[0],))
        count = cursor.fetchone()[0]
        print(f"ID: {row[0]} | Name: {row[1]} | Exam ID: {row[2]} | Count: {count}")
        
    conn.close()

if __name__ == "__main__":
    check_v2_math()
