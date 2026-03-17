import sqlite3
conn = sqlite3.connect('past_questions_v2.db')
cursor = conn.cursor()
cursor.execute('SELECT DISTINCT category FROM exams')
cats = [row[0] for row in cursor.fetchall()]
print(f"Categories: {cats}")
conn.close()
