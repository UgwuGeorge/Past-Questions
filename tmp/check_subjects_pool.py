
import sqlite3

def check_subjects_pool():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check WAEC Mathematics subject question counts
    cursor.execute("""
        SELECT s.id, s.name, COUNT(q.id) as q_count
        FROM subjects s
        JOIN questions q ON s.id = q.subject_id
        WHERE s.name LIKE '%Mathematics%'
        GROUP BY s.id
    """)
    res = cursor.fetchall()
    for row in res:
        print(f"Subject ID {row[0]}: {row[1]} has {row[2]} questions.")
        
    conn.close()

if __name__ == "__main__":
    check_subjects_pool()
