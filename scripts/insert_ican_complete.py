
import sqlite3
import os
import re

DB = 'past_questions_v2.db'

def get_subject_id(c, subj_name, exam_name):
    # Find exam ID
    c.execute("SELECT id FROM exams WHERE name=?", (exam_name,))
    r = c.fetchone()
    if not r:
        return None
    eid = r[0]
    
    # Find subject ID
    c.execute("SELECT id FROM subjects WHERE name=? AND exam_id=?", (subj_name, eid))
    r = c.fetchone()
    if not r:
        # Create it if missing
        c.execute("INSERT INTO subjects (name, exam_id) VALUES (?, ?)", (subj_name, eid))
        return c.lastrowid
    return r[0]

def parse_and_insert(level, exam_name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    data_dir = f'data/Professional/ICAN/{level}'
    if not os.path.exists(data_dir):
        print(f"Dir {data_dir} not found.")
        return

    for filename in os.listdir(data_dir):
        if not filename.endswith('.md') or '_2024' not in filename:
            continue
            
        # Subject name from filename: ICAN_Financial_Accounting_May_2024.md
        subj_name = filename.replace('ICAN_', '').split('_May_2024')[0].split('_Nov_2023')[0].replace('_', ' ')
        sid = get_subject_id(c, subj_name, exam_name)
        if not sid:
            print(f"Exam {exam_name} not found in DB.")
            continue
            
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract Theory Section (Everything after 'SECTION B' or 'Section B')
        theory_match = re.search(r'SECTION B[:\s]+.*?(?=\s*SOLUTION|\s*Examiner|$)', content, re.DOTALL | re.IGNORECASE)
        if theory_match:
            theory_block = theory_match.group(0)
            # Find individual questions: e.g. "QUESTION 1", "Question 1"
            qs = re.split(r'\bQUESTION\s+\d+\b', theory_block, flags=re.IGNORECASE)
            for idx, q_text in enumerate(qs[1:], 1):
                # Clean up question text
                q_text = q_text.strip()
                if not q_text: continue
                
                # Try to find corresponding solution in same file
                sol_pattern = rf'SOLUTION {idx}.*?(?=\s*SOLUTION|\s*Examiner|$)'
                sol_match = re.search(sol_pattern, content, re.DOTALL | re.IGNORECASE)
                explanation = sol_match.group(0).strip() if sol_match else "Official solution provided in Pathfinder."
                
                # Check for duplicate
                c.execute("SELECT id FROM questions WHERE subject_id=? AND text=? AND section=?", (sid, q_text[:200], "Section B: Theory"))
                if c.fetchone():
                    continue

                c.execute("INSERT INTO questions (subject_id, text, explanation, difficulty, year, is_ai_generated, section) VALUES (?,?,?,?,?,?,?)",
                          (sid, q_text, explanation, "MEDIUM", 2024, False, "Section B: Theory"))
                print(f"  Added Theory Q{idx} for {subj_name} ({exam_name})")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parse_and_insert("Foundation", "ICAN Foundation")
    parse_and_insert("Skills", "ICAN Skills")
    parse_and_insert("Professional", "ICAN Professional")
