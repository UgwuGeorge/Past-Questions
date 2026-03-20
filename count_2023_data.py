import os
import re
import json

def count_questions_md(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Handle **1.** or 1. or 1) patterns, possibly with bolding
        # Matches: **1.** , 1. , **1)** , 1) 
        matches = re.findall(r'(\d+)[\.\)]', content)
        # However, we only want those that look like the start of a question block
        # Usually they are followed by text and then A) B) C) 
        # A more reliable way is to look for markers at the start of lines or inside bolding
        matches = re.findall(r'^\s*(\*\*)*\d+[\.\)](\*\*)*', content, re.MULTILINE)
        
        # Unique numbers check
        nums = re.findall(r'\b(\d+)\b[\.\)]', content)
        unique_nums = len(set(nums))
        return unique_nums
    except Exception as e:
        return 0

def count_questions_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return len(data)
            elif isinstance(data, dict):
                # Check for common keys
                for key in ["questions", "data", "results"]:
                    if key in data and isinstance(data[key], list):
                        return len(data[key])
        return 0
    except Exception as e:
        return 0

base_dir = os.path.join(os.getcwd(), "data")
base_dir = os.path.abspath(base_dir)

print(f"Audit of 2023 Past Questions Data (Base: {base_dir})\n")
print("| Exam Category | Subject | File | Count | Status |")
print("|---|---|---|---|---|")

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if "2023" in file:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, base_dir)
            
            if file.endswith(".md"):
                count = count_questions_md(path)
            elif file.endswith(".json"):
                count = count_questions_json(path)
            else:
                continue
                
            # Determine status
            # Most objective exams are 40-50 questions. 
            # English can be 60-100.
            status = "Complete" if (isinstance(count, int) and count >= 40) else "Partial"
            
            # Simple category parsing
            parts = rel_path.split(os.sep)
            category = parts[0] if len(parts) > 1 else "Unknown"
            subject = parts[-2] if len(parts) > 2 else file.replace(".md", "").replace(".json", "")
            
            print(f"| {category} | {subject} | {file} | {count} | {status} |")
