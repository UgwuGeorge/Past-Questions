import sqlite3
import os

db_path = 'past_questions_v2.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Rename is_ai_generated to is_expert_derived in questions
        cursor.execute("PRAGMA table_info(questions)")
        cols = [c[1] for c in cursor.fetchall()]
        if 'is_ai_generated' in cols and 'is_expert_derived' not in cols:
            print("Renaming 'is_ai_generated' to 'is_expert_derived' in questions...")
            cursor.execute("ALTER TABLE questions RENAME COLUMN is_ai_generated TO is_expert_derived")
        
        # 2. Rename ai_feedback table to expert_analysis
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ai_feedback'")
        if cursor.fetchone():
            print("Renaming table 'ai_feedback' to 'expert_analysis'...")
            cursor.execute("ALTER TABLE ai_feedback RENAME TO expert_analysis")
            
        # 3. Rename feedback_json to analysis_json in expert_analysis
        cursor.execute("PRAGMA table_info(expert_analysis)")
        cols = [c[1] for c in cursor.fetchall()]
        if 'feedback_json' in cols and 'analysis_json' not in cols:
            print("Renaming 'feedback_json' to 'analysis_json' in expert_analysis...")
            cursor.execute("ALTER TABLE expert_analysis RENAME COLUMN feedback_json TO analysis_json")

        conn.commit()
        print("Migration complete.")
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
