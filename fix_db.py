import sqlite3

db_path = 'agent_local_data.db'

def fix_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fix questions table
    questions_missing = [
        ('paper_id', 'INTEGER'),
        ('context_id', 'INTEGER'),
        ('question_num', 'INTEGER'),
        ('section', 'VARCHAR'),
        ('image_url', 'VARCHAR')
    ]
    for col, ctype in questions_missing:
        try:
            cursor.execute(f"ALTER TABLE questions ADD COLUMN {col} {ctype}")
            print(f"Added {col} to questions")
        except sqlite3.OperationalError:
            print(f"{col} already exists in questions")

    # Fix choices table
    choices_missing = [
        ('label', 'VARCHAR'),
        ('image_url', 'VARCHAR')
    ]
    for col, ctype in choices_missing:
        try:
            cursor.execute(f"ALTER TABLE choices ADD COLUMN {col} {ctype}")
            print(f"Added {col} to choices")
        except sqlite3.OperationalError:
            print(f"{col} already exists in choices")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_db()
