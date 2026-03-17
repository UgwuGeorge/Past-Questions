import sqlite3
import os

db_path = 'past_questions_v2.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Map potential values to the Enum NAMES used by SQLAlchemy
mapping = {
    'Academics': 'ACADEMICS',
    'Professional': 'PROFESSIONAL',
    'Scholarships': 'SCHOLARSHIPS',
    'academics': 'ACADEMICS',
    'professional': 'PROFESSIONAL',
    'scholarships': 'SCHOLARSHIPS',
    'Professional Level': 'PROFESSIONAL'
}

print("Cleaning up exam categories...")
cursor.execute("SELECT id, name, category FROM exams")
exams = cursor.fetchall()
for eid, name, cat in exams:
    if cat in mapping:
        new_cat = mapping[cat]
        print(f"Updating {name}: {cat} -> {new_cat}")
        cursor.execute("UPDATE exams SET category = ? WHERE id = ?", (new_cat, eid))
    elif cat not in ['ACADEMICS', 'PROFESSIONAL', 'SCHOLARSHIPS']:
        # Default fallback or just log
        print(f"Warning: unknown category '{cat}' for {name}")

conn.commit()
conn.close()
print("Done.")
