
import sqlite3

def deep_sync_subjects():
    local_db = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    v2_db = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_core/past_questions_v2.db'
    
    conn_local = sqlite3.connect(local_db)
    cur_local = conn_local.cursor()
    
    conn_v2 = sqlite3.connect(v2_db)
    cur_v2 = conn_v2.cursor()
    
    # Core subjects to boost
    core_subjects = {
        'Mathematics': 2,
        'English Language': 118,
        'Biology': 109,
        'Chemistry': 111,
        'Physics': 134,
        'Economics': 117,
        'Government': 124
    }
    
    total_added = 0
    for sub_name, target_sid in core_subjects.items():
        print(f"Boosting {sub_name} (Target ID: {target_sid})...")
        
        # Find all matching subjects in V2 (e.g. 'Mathematics', 'Mathematics Past Questions', 'JAMB Mathematics')
        cur_v2.execute("SELECT id, name FROM subjects WHERE name LIKE ?", (f"%{sub_name}%",))
        v2_subs = cur_v2.fetchall()
        
        for v2_sid, v2_sname in v2_subs:
            # Get all questions for this V2 subject
            cur_v2.execute("SELECT id, text, topic, year, explanation, section FROM questions WHERE subject_id = ?", (v2_sid,))
            questions = cur_v2.fetchall()
            
            for q_id, text, topic, year, expl, sect in questions:
                # Check if question already exists in local (by text)
                cur_local.execute("SELECT id FROM questions WHERE text = ? AND subject_id = ?", (text, target_sid))
                if cur_local.fetchone():
                    continue
                    
                # Insert question
                cur_local.execute("""
                    INSERT INTO questions (text, topic, year, subject_id, explanation, section, difficulty)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (text, topic or "General", year, target_sid, expl, sect, "medium"))
                new_qid = cur_local.lastrowid
                
                # Get choices from V2
                cur_v2.execute("SELECT label, text, is_correct, image_url FROM choices WHERE question_id = ?", (q_id,))
                choices = cur_v2.fetchall()
                for lbl, ctext, is_corr, img in choices:
                    cur_local.execute("""
                        INSERT INTO choices (question_id, label, text, is_correct, image_url)
                        VALUES (?, ?, ?, ?, ?)
                    """, (new_qid, lbl, ctext, is_corr, img))
                
                total_added += 1
                if total_added % 100 == 0:
                    conn_local.commit()
                    print(f"  Added {total_added} questions total...")

    conn_local.commit()
    conn_local.close()
    conn_v2.close()
    print(f"DEEP SYNC COMPLETE: Added {total_added} core questions across subjects.")

if __name__ == "__main__":
    deep_sync_subjects()
