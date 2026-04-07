
import sqlite3

def check_db(db_name):
    print(f"\n--- Checking {db_name} ---")
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Tables: {tables}")
        
        if 'exams' in tables:
            cursor.execute("SELECT count(*) FROM exams")
            print(f"Exams count: {cursor.fetchone()[0]}")
            cursor.execute("SELECT * FROM exams LIMIT 5")
            print(f"Sample exams: {cursor.fetchall()}")
        
        if 'questions' in tables:
            cursor.execute("SELECT count(*) FROM questions")
            print(f"Questions count: {cursor.fetchone()[0]}")
            
        if 'exams' in tables:
            # specifically check for WAEC
            cursor.execute("SELECT id, name FROM exams WHERE name LIKE '%WAEC%' OR category LIKE '%WAEC%'")
            waec = cursor.fetchall()
            print(f"WAEC Exams: {waec}")
            for ex in waec:
                eid = ex[0]
                cursor.execute(f"SELECT count(*) FROM questions WHERE exam_id = {eid}")
                qcount = cursor.fetchone()[0]
                print(f"  - {ex[1]} (ID: {eid}): {qcount} questions")
                
        conn.close()
    except Exception as e:
        print(f"Error checking {db_name}: {e}")

if __name__ == "__main__":
    check_db('agent_local_data.db')
    check_db('past_questions_v2.db')
