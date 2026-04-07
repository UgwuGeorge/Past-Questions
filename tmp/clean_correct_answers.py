
import sqlite3

def clean_correct_answers():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Fix questions with multiple correct answers
    cursor.execute("SELECT question_id FROM choices WHERE is_correct = 1 GROUP BY question_id HAVING count(*) > 1")
    multi_qs = [row[0] for row in cursor.fetchall()]
    
    for qid in multi_qs:
        cursor.execute("SELECT id FROM choices WHERE question_id = ? AND is_correct = 1 ORDER BY id", (qid,))
        choice_ids = [row[0] for row in cursor.fetchall()]
        # Keep the first one, unmark the rest
        for cid in choice_ids[1:]:
            cursor.execute("UPDATE choices SET is_correct = 0 WHERE id = ?", (cid,))
            
    # 2. Fix questions with zero correct answers (if they have choices)
    cursor.execute("""
        SELECT q.id 
        FROM questions q 
        JOIN choices c ON q.id = c.question_id 
        GROUP BY q.id 
        HAVING SUM(c.is_correct) = 0
    """)
    zero_qs = [row[0] for row in cursor.fetchall()]
    
    for qid in zero_qs:
        # Mark the first choice as correct as a fallback
        cursor.execute("SELECT id FROM choices WHERE question_id = ? ORDER BY id LIMIT 1", (qid,))
        cid = cursor.fetchone()
        if cid:
            cursor.execute("UPDATE choices SET is_correct = 1 WHERE id = ?", (cid[0],))
            
    conn.commit()
    conn.close()
    print(f"Cleaned up {len(multi_qs)} questions with multi-correct and {len(zero_qs)} with zero-correct.")

if __name__ == "__main__":
    clean_correct_answers()
