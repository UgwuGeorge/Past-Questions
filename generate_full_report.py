import sqlite3
import os
import re
import json

def count_questions_md(file_path):
    try:
        if not os.path.exists(file_path): return 0
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        nums = re.findall(r'\b(\d+)\b[\.\)]', content)
        return len(set(nums))
    except: return 0

def count_questions_json(file_path):
    try:
        if not os.path.exists(file_path): return 0
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list): return len(data)
            if isinstance(data, dict):
                for key in ["questions", "data", "results"]:
                    if key in data and isinstance(data[key], list):
                        return len(data[key])
        return 0
    except: return 0

def get_report():
    conn = sqlite3.connect('agent_local_data.db')
    cursor = conn.cursor()
    
    query = """
    SELECT e.category, e.name as exam, s.name as subject, q.year, COUNT(q.id) as db_count
    FROM questions q
    JOIN subjects s ON q.subject_id = s.id
    JOIN exams e ON s.exam_id = e.id
    WHERE q.year = 2023
    GROUP BY e.id, s.id, q.year
    ORDER BY e.category, e.name, s.name
    """
    
    cursor.execute(query)
    db_results = cursor.fetchall()
    
    print("# 2023 Subject Status Report (DB vs Files)\n")
    print("| Category | Exam | Subject | DB Count | File Count | Status |")
    print("|---|---|---|---|---|---|")
    
    base_data_dir = os.path.join(os.getcwd(), "data")
    
    # We also want to check files that might not be in the DB yet
    # But for simplicity, we'll iterate through the DB results and then find files
    
    for category, exam, subject, year, db_count in db_results:
        # Try to guess file path
        # Pattern: data/Academic/JAMB/Biology/2023.md or similar
        # Or look for any file with '2023' and 'subject' in its name
        found_file_count = 0
        status = "Partial"
        
        # Fuzzy matching: strip "Past Questions" and other fluff
        clean_subject = subject.replace("Past Questions", "").replace("Questions", "").strip().lower()
        search_terms = clean_subject.split()
        
        for root, dirs, files in os.walk(base_data_dir):
            for file in files:
                file_lower = file.lower()
                if "2023" in file_lower:
                    # Check if all words in clean_subject are in the filename
                    if all(term in file_lower for term in search_terms):
                        file_path = os.path.join(root, file)
                        if file.endswith(".md"):
                            found_file_count = max(found_file_count, count_questions_md(file_path))
                        elif file.endswith(".json"):
                            found_file_count = max(found_file_count, count_questions_json(file_path))
        
        if db_count >= 40 or found_file_count >= 40:
            status = "Complete"
            
        print(f"| {category} | {exam} | {subject} | {db_count} | {found_file_count} | {status} |")
        
    conn.close()

if __name__ == "__main__":
    get_report()
