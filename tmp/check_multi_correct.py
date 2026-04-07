
import sqlite3

def check_multiple_correct():
    db_path = 'c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_local_data.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT question_id, count(*) 
        FROM choices 
        WHERE is_correct = 1 
        GROUP BY question_id 
        HAVING count(*) > 1
    """)
    dupes = cursor.fetchall()
    
    if dupes:
        print(f"Found {len(dupes)} questions with multiple correct answers.")
        for qid, count in dupes[:10]:
            print(f"Question ID {qid} has {count} correct answers.")
    else:
        print("No questions with multiple correct answers found.")
        
    conn.close()

if __name__ == "__main__":
    check_multiple_correct()
