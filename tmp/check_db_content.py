import sqlite3

conn = sqlite3.connect('past_questions_v2.db')
cursor = conn.cursor()

print("Exams:")
cursor.execute("SELECT id, name, category, sub_category FROM exams")
for row in cursor.fetchall():
    print(row)

print("\nSubjects count per exam:")
cursor.execute("SELECT exam_id, COUNT(*) FROM subjects GROUP BY exam_id")
for row in cursor.fetchall():
    print(row)

conn.close()
