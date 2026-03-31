import sqlite3

def list_exams():
    try:
        conn = sqlite3.connect('c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/past_questions_v2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM exams")
        exams = cursor.fetchall()
        
        with open('c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/tmp/exam_list.txt', 'w') as f:
            for exam in exams:
                f.write(f"ID: {exam[0]} - Name: {exam[1]}\n")
                
    except Exception as e:
        with open('c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/tmp/exam_list.txt', 'w') as f:
            f.write(str(e))

list_exams()
