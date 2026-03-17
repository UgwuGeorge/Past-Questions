import sqlite3
conn = sqlite3.connect('past_questions_v2.db')
cursor = conn.cursor()

# Map to the Enum NAMES (uppercase) as SQLAlchemy models usually expect for SQLEnum
mapping = {
    'Academics': 'ACADEMICS',
    'Professional': 'PROFESSIONAL',
    'Scholarships': 'SCHOLARSHIPS'
}

print("Setting exam categories to UPPERCASE names...")
cursor.execute("SELECT id, category FROM exams")
rows = cursor.fetchall()
for eid, cat in rows:
    if cat in mapping:
        new_cat = mapping[cat]
        cursor.execute("UPDATE exams SET category = ? WHERE id = ?", (new_cat, eid))

conn.commit()
cursor.execute("SELECT DISTINCT category FROM exams")
print(f"Final Categories in DB: {[row[0] for row in cursor.fetchall()]}")
conn.close()
