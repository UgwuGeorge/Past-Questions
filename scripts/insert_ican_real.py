"""
Insert REAL ICAN Past Questions into the database.
Questions sourced from ICAN Pathfinder November 2024 & May 2024 diets (icanig.org).
Format: 5 options (A-E), 20 MCQs per subject Section A.
Covers all 15 ICAN subjects across Foundation, Skills, and Professional levels.
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'past_questions_v2.db')

# ICAN exam structure with all 15 subjects
ICAN_SUBJECTS = {
    "Foundation": [
        "Financial Accounting",
        "Management Information",
        "Business Law",
        "Quantitative Techniques in Business",
    ],
    "Skills": [
        "Financial Reporting",
        "Taxation",
        "Performance Management",
        "Audit and Assurance",
        "Public Sector Accounting and Finance",
        "Financial Management",
    ],
    "Professional": [
        "Corporate Reporting",
        "Advanced Taxation",
        "Strategic Financial Management",
        "Advanced Audit and Assurance",
        "Case Study",
    ]
}

def get_questions_data():
    """Return dict of subject -> list of question dicts.
    Questions sourced from ICAN Pathfinder Nov 2024 & May 2024 (icanig.org)."""
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ican_questions_data.json'), 'r', encoding='utf-8'))

def insert_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get or create ICAN exam entries for each level
    exam_ids = {}
    for level in ICAN_SUBJECTS:
        exam_name = f"ICAN {level}"
        c.execute("SELECT id FROM exams WHERE name = ?", (exam_name,))
        row = c.fetchone()
        if row:
            exam_ids[level] = row[0]
        else:
            c.execute("INSERT INTO exams (name, category, description, sub_category) VALUES (?, ?, ?, ?)",
                      (exam_name, "Professional", f"ICAN {level} Level Examination", level))
            exam_ids[level] = c.lastrowid

    # Load questions data
    questions_data = get_questions_data()
    
    total_q = 0
    for level, subjects in ICAN_SUBJECTS.items():
        exam_id = exam_ids[level]
        for subject_name in subjects:
            # Get or create subject
            c.execute("SELECT id FROM subjects WHERE name = ? AND exam_id = ?", (subject_name, exam_id))
            row = c.fetchone()
            if row:
                sid = row[0]
                # Clear old questions
                c.execute("DELETE FROM choices WHERE question_id IN (SELECT id FROM questions WHERE subject_id = ?)", (sid,))
                c.execute("DELETE FROM questions WHERE subject_id = ?", (sid,))
            else:
                c.execute("INSERT INTO subjects (name, exam_id) VALUES (?, ?)", (subject_name, exam_id))
                sid = c.lastrowid

            qs = questions_data.get(subject_name, [])
            for q in qs:
                c.execute(
                    "INSERT INTO questions (subject_id, text, explanation, difficulty, year, is_ai_generated, section, topic) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (sid, q['text'], q.get('explanation',''), 'MEDIUM', q.get('year', 2024), False, 'Multiple Choice', q.get('topic', ''))
                )
                qid = c.lastrowid
                for ch in q['choices']:
                    c.execute(
                        "INSERT INTO choices (question_id, text, is_correct, label) VALUES (?, ?, ?, ?)",
                        (qid, ch['text'], ch['is_correct'], ch['label'])
                    )
                total_q += 1

            print(f"  [{level}] {subject_name}: {len(qs)} questions inserted (subject_id={sid})")

    conn.commit()
    conn.close()
    print(f"\n[DONE] Inserted {total_q} total ICAN questions across all levels.")

if __name__ == "__main__":
    insert_all()
