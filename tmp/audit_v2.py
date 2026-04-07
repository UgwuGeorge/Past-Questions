
import sqlite3

def audit_v2_db():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_core/past_questions_v2.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check all subjects in v2
    cursor.execute("""
        SELECT s.id, s.name, (SELECT COUNT(*) FROM questions WHERE subject_id = s.id) as q_count
        FROM subjects s
        ORDER BY q_count DESC
    """)
    res = cursor.fetchall()
    print("V2 DB SUBJECTS:")
    for row in res[:20]:
        print(f"ID: {row[0]} | Name: {row[1]} | Count: {row[2]}")
        
    conn.close()

if __name__ == "__main__":
    audit_v2_db()
