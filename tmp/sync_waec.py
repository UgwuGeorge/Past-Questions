
import sqlite3

def sync_waec_data():
    local_db = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    v2_db = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/past_questions_v2.db'
    
    conn_local = sqlite3.connect(local_db)
    conn_v2 = sqlite3.connect(v2_db)
    
    cur_local = conn_local.cursor()
    cur_v2 = conn_v2.cursor()
    
    print("Starting WAEC data sync...")
    
    # WAEC ID in local is 2, in V2 is 10
    local_waec_id = 2
    v2_waec_id = 10
    
    # 1. Get all subjects for WAEC in V2
    cur_v2.execute("SELECT id, name FROM subjects WHERE exam_id = ?", (v2_waec_id,))
    v2_subjects = cur_v2.fetchall()
    
    for v2_sid, sname in v2_subjects:
        print(f"Checking subject: {sname}")
        
        # 2. Ensure subject exists in local
        cur_local.execute("SELECT id FROM subjects WHERE exam_id = ? AND name = ?", (local_waec_id, sname))
        local_row = cur_local.fetchone()
        if not local_row:
            cur_local.execute("INSERT INTO subjects (name, exam_id) VALUES (?, ?)", (sname, local_waec_id))
            local_sid = cur_local.lastrowid
            print(f"  Created new subject: {sname} (ID: {local_sid})")
        else:
            local_sid = local_row[0]
            
        # 3. Get all questions for this subject in V2
        # Columns in V2: id, subject_id, paper_id, context_id, question_num, section, text, image_url, explanation, difficulty, topic, year, is_expert_derived
        cur_v2.execute("SELECT id, text, explanation, difficulty, topic, year, question_num, section, image_url FROM questions WHERE subject_id = ?", (v2_sid,))
        v2_questions = cur_v2.fetchall()
        
        added_count = 0
        for q_v2 in v2_questions:
            q_v2_id, text, explanation, difficulty, topic, year, q_num, section, image_url = q_v2
            
            # Check if this question already exists in local (by text and subject)
            cur_local.execute("SELECT id FROM questions WHERE subject_id = ? AND text = ?", (local_sid, text))
            if not cur_local.fetchone():
                # Columns in Local: id, subject_id, text, explanation, difficulty, topic, year, is_ai_generated, paper_id, context_id, question_num, section, image_url
                cur_local.execute("""
                    INSERT INTO questions (subject_id, text, explanation, difficulty, topic, year, question_num, section, image_url, is_ai_generated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (local_sid, text, explanation, difficulty, topic, year, q_num, section, image_url, 0))
                local_qid = cur_local.lastrowid
                
                # 4. Get and insert choices for this question
                # Columns in V2: id, question_id, label, text, image_url, is_correct
                cur_v2.execute("SELECT label, text, image_url, is_correct FROM choices WHERE question_id = ?", (q_v2_id,))
                v2_choices = cur_v2.fetchall()
                for c in v2_choices:
                    # Columns in Local: id, question_id, text, is_correct, label, image_url
                    cur_local.execute("""
                        INSERT INTO choices (question_id, text, is_correct, label, image_url)
                        VALUES (?, ?, ?, ?, ?)
                    """, (local_qid, c[1], c[3], c[0], c[2]))
                
                added_count += 1
        
        if added_count > 0:
            print(f"  Added {added_count} new questions to {sname}")
            conn_local.commit()
        else:
            print(f"  {sname} is already up to date.")

    conn_local.close()
    conn_v2.close()
    print("Sync complete!")

if __name__ == "__main__":
    sync_waec_data()
