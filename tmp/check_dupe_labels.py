
import sqlite3

def check_duplicate_labels():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check WAEC Mathematics subjects
    cursor.execute("SELECT id FROM subjects WHERE name LIKE '%Mathematics%' AND exam_id = 2")
    subject_ids = [row[0] for row in cursor.fetchall()]
    
    for sid in subject_ids:
        cursor.execute("SELECT id FROM questions WHERE subject_id = ?", (sid,))
        question_ids = [row[0] for row in cursor.fetchall()]
        
        for qid in question_ids:
            cursor.execute("SELECT label, count(*) FROM choices WHERE question_id = ? GROUP BY label HAVING count(*) > 1", (qid,))
            dupes = cursor.fetchall()
            if dupes:
                print(f"Question ID {qid} has duplicate labels: {dupes}")
    
    conn.close()

if __name__ == "__main__":
    check_duplicate_labels()
