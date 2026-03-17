import sqlite3
import os

DB = 'past_questions_v2.db'

def check_ican():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    print("--- ICAN EXAMS ---")
    c.execute("SELECT id, name, category FROM exams WHERE name LIKE '%ICAN%'")
    exams = c.fetchall()
    if not exams:
        print("No ICAN exams found.")
        return
        
    for eid, name, cat in exams:
        print(f"Exam: {name} (ID: {eid}, Category: {cat})")
        c.execute("SELECT id, name FROM subjects WHERE exam_id = ?", (eid,))
        subjects = c.fetchall()
        for sid, sname in subjects:
            c.execute("SELECT COUNT(*) FROM questions WHERE subject_id = ?", (sid,))
            q_count = c.fetchone()[0]
            print(f"  Subject: {sname} - {q_count} questions")
    
    conn.close()

if __name__ == "__main__":
    check_ican()
