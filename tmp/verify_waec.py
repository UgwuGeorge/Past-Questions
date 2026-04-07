
import sqlite3

def check_waec(db_path):
    print(f"\n--- Checking {db_path} ---")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get WAEC exams
        cursor.execute("SELECT id, name FROM exams WHERE name LIKE '%WAEC%'")
        waec_exams = cursor.fetchall()
        
        if not waec_exams:
            print("No WAEC exams found.")
            return

        for eid, ename in waec_exams:
            print(f"\nExam: {ename} (ID: {eid})")
            
            # Get subjects for this exam
            cursor.execute("SELECT id, name FROM subjects WHERE exam_id = ?", (eid,))
            subjects = cursor.fetchall()
            
            if not subjects:
                print("  No subjects linked to this exam.")
                continue
                
            total_questions = 0
            for sid, sname in subjects:
                cursor.execute("SELECT count(*) FROM questions WHERE subject_id = ?", (sid,))
                qcount = cursor.fetchone()[0]
                print(f"  - Subject: {sname} (ID: {sid}) | Questions: {qcount}")
                total_questions += qcount
            
            print(f"Total Questions for {ename}: {total_questions}")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_waec('agent_local_data.db')
    check_waec('past_questions_v2.db')
