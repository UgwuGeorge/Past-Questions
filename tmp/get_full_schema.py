
import sqlite3

def log_schema(db_name, output_file):
    with open(output_file, 'a') as f:
        f.write(f"\n--- Schema for {db_name} ---\n")
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [t[0] for t in cursor.fetchall()]
            f.write(f"Tables: {tables}\n")
            
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table})")
                cols = cursor.fetchall()
                f.write(f"\nTable {table}:\n")
                for col in cols:
                    f.write(f"  {col}\n")
            
            # Also get sample data from exams
            if 'exams' in tables:
                cursor.execute("SELECT * FROM exams LIMIT 20")
                f.write(f"\nSample Exams:\n {cursor.fetchall()}\n")
                
            conn.close()
        except Exception as e:
            f.write(f"Error: {e}\n")

if __name__ == "__main__":
    open('tmp/full_schema.txt', 'w').close() # clear
    log_schema('agent_local_data.db', 'tmp/full_schema.txt')
    log_schema('past_questions_v2.db', 'tmp/full_schema.txt')
