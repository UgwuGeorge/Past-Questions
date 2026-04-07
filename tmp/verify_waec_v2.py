
import sqlite3

def check_waec(db_path, log_file):
    with open(log_file, 'a') as f:
        f.write(f"\n--- Checking {db_path} ---\n")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name FROM exams WHERE name LIKE '%WAEC%'")
            waec_exams = cursor.fetchall()
            
            if not waec_exams:
                f.write("No WAEC exams found.\n")
                return

            for eid, ename in waec_exams:
                f.write(f"\nExam: {ename} (ID: {eid})\n")
                
                cursor.execute("SELECT id, name FROM subjects WHERE exam_id = ?", (eid,))
                subjects = cursor.fetchall()
                
                if not subjects:
                    f.write("  No subjects linked to this exam.\n")
                    continue
                    
                total_questions = 0
                for sid, sname in subjects:
                    cursor.execute("SELECT count(*) FROM questions WHERE subject_id = ?", (sid,))
                    qcount = cursor.fetchone()[0]
                    f.write(f"  - Subject: {sname} (ID: {sid}) | Questions: {qcount}\n")
                    total_questions += qcount
                
                f.write(f"Total Questions for {ename}: {total_questions}\n")

            conn.close()
        except Exception as e:
            f.write(f"Error: {e}\n")

if __name__ == "__main__":
    open('tmp/waec_check_results.txt', 'w').close()
    check_waec('agent_local_data.db', 'tmp/waec_check_results.txt')
    check_waec('past_questions_v2.db', 'tmp/waec_check_results.txt')
