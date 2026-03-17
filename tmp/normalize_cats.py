import sqlite3
conn = sqlite3.connect('past_questions_v2.db')
cursor = conn.cursor()

def normalize(val):
    v = val.upper().strip()
    if 'ACADEMIC' in v: return 'Academics'
    if 'PROFESSION' in v: return 'Professional'
    if 'SCHOLAR' in v: return 'Scholarships'
    return val

cursor.execute("SELECT id, category FROM exams")
rows = cursor.fetchall()
for eid, cat in rows:
    new_cat = normalize(cat)
    if new_cat != cat:
        cursor.execute("UPDATE exams SET category = ? WHERE id = ?", (new_cat, eid))

conn.commit()
cursor.execute("SELECT DISTINCT category FROM exams")
print(f"Final Categories: {[row[0] for row in cursor.fetchall()]}")
conn.close()
