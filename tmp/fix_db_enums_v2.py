import sqlite3
import os

db_path = 'past_questions_v2.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Map potential values to the PascalCase values defined in main_models.ExamCategory
mapping = {
    'ACADEMICS': 'Academics',
    'PROFESSIONAL': 'Professional',
    'SCHOLARSHIPS': 'Scholarships',
    'academics': 'Academics',
    'professional': 'Professional',
    'scholarships': 'Scholarships',
    'Professional Level': 'Professional'
}

print("Fixing exam categories to PascalCase...")
cursor.execute("SELECT id, name, category FROM exams")
exams = cursor.fetchall()
for eid, name, cat in exams:
    if cat in mapping:
        new_cat = mapping[cat]
        print(f"Updating {name}: {cat} -> {new_cat}")
        cursor.execute("UPDATE exams SET category = ? WHERE id = ?", (new_cat, eid))
    else:
        print(f"Keeping {name}: {cat}")

conn.commit()
conn.close()
print("Done.")
