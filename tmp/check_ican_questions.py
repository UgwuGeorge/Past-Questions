import sqlite3

conn = sqlite3.connect('past_questions_v2.db')
cursor = conn.cursor()

print("ICAN Exams and Subjects info:")
cursor.execute("SELECT id, name FROM exams WHERE name LIKE 'ICAN%'")
exams = cursor.fetchall()
for eid, name in exams:
    print(f"\nExam: {name} (ID: {eid})")
    cursor.execute("SELECT id, name FROM subjects WHERE exam_id = ?", (eid,))
    subjects = cursor.fetchall()
    for sid, sname in subjects:
        cursor.execute("SELECT COUNT(*) FROM questions WHERE subject_id = ?", (sid,))
        qcount = cursor.fetchone()[0]
        print(f"  Subject: {sname} (ID: {sid}) - Questions: {qcount}")

conn.close()
