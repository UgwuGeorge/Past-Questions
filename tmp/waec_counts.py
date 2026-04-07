
import sqlite3

def list_waec_subjects_counts():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.id, s.name, (SELECT COUNT(*) FROM questions WHERE subject_id = s.id) as q_count
        FROM subjects s
        WHERE s.exam_id = 2
        ORDER BY q_count DESC
    """)
    res = cursor.fetchall()
    for row in res:
        print(f"ID: {row[0]} | Name: {row[1]} | Count: {row[2]}")
        
    conn.close()

if __name__ == "__main__":
    list_waec_subjects_counts()
