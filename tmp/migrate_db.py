import sqlite3
import os

DB_PATH = 'agent_core/past_questions_v2.db'

def migrate_db():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Add required_tier and price to exams
    try:
        cursor.execute("ALTER TABLE exams ADD COLUMN required_tier VARCHAR DEFAULT 'FREE'")
        print("Added 'required_tier' to 'exams'")
    except sqlite3.OperationalError as e:
        print(f"'required_tier' already exists or error: {e}")

    try:
        cursor.execute("ALTER TABLE exams ADD COLUMN price FLOAT DEFAULT 0.0")
        print("Added 'price' to 'exams'")
    except sqlite3.OperationalError as e:
        print(f"'price' already exists or error: {e}")

    # 2. Create subscriptions table if it doesn't exist
    # Base.metadata.create_all(bind=engine) in main.py usually handles this,
    # but let's ensure it's there or just let fastapi do it on restart.
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_db()
