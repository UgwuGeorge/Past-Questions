
import sqlite3

def fix_choice_labels():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all questions
    cursor.execute("SELECT id FROM questions")
    q_ids = [row[0] for row in cursor.fetchall()]
    
    label_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}
    
    total_fixed = 0
    for qid in q_ids:
        # Get choices for this question
        cursor.execute("SELECT id, label FROM choices WHERE question_id = ? ORDER BY id", (qid,))
        choices = cursor.fetchall()
        
        # Check if they need fixing (either duplicate or non-standard)
        labels = [c[1] for c in choices]
        if len(set(labels)) != len(labels) or any(l not in ['A', 'B', 'C', 'D', 'E'] for l in labels):
            for i, (cid, old_label) in enumerate(choices):
                new_label = label_map.get(i, f"Z{i}")
                cursor.execute("UPDATE choices SET label = ? WHERE id = ?", (new_label, cid))
            total_fixed += 1
            
    conn.commit()
    conn.close()
    print(f"Fixed labels for {total_fixed} questions.")

if __name__ == "__main__":
    fix_choice_labels()
