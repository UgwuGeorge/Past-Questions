
import sqlite3
import os

DB = 'past_questions_v2.db'
def check():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT e.name, s.name, COUNT(*) 
        FROM questions q 
        JOIN subjects s ON q.subject_id = s.id 
        JOIN exams e ON s.exam_id = e.id 
        WHERE q.section = 'Section B: Theory' 
        GROUP BY e.name, s.name
    """)
    for row in c.fetchall():
        print(f"Exam: {row[0]}, Subject: {row[1]}, Section B Count: {row[2]}")
    conn.close()

if __name__ == "__main__":
    check()
