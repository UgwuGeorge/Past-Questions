"""
JAMB JSON to Markdown Converter
==============================
Converts raw scraper output into the repository's standard MD format.
"""
import os
import json
import glob

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), 'data', 'jamb_2023_raw')
OUTPUT_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), 'data', 'Academic', 'JAMB')

def convert():
    json_files = glob.glob(os.path.join(RAW_DIR, "*.json"))
    
    for file_path in json_files:
        basename = os.path.basename(file_path)
        subject = basename.split('_')[0].capitalize()
        year = "2023"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
            
        md_content = f"# JAMB {subject} Past Questions - {year}\n\n## Questions\n\n"
        
        for i, q in enumerate(questions, 1):
            q_text = q.get('question', '').strip()
            options = q.get('option', {})
            answer = q.get('answer', '').upper()
            solution = q.get('solution', '').strip()
            image = q.get('image', '').strip()
            
            md_content += f"**{i}.** {q_text}\n"
            if image:
                md_content += f"   *(See image: {image})*\n"
                
            for label, text in options.items():
                if text and label in ['a', 'b', 'c', 'd', 'e']:
                    md_content += f"   {label.upper()}) {text}\n"
            
            md_content += f"   **Answer: {answer}**\n"
            if solution:
                md_content += f"   *Explanation: {solution}*\n"
            md_content += "\n"
            
        # Ensure subject directory exists
        subj_dir = os.path.join(OUTPUT_DIR, subject)
        os.makedirs(subj_dir, exist_ok=True)
        
        target_path = os.path.join(subj_dir, f"{year}.md")
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print(f"Converted {subject} ({len(questions)}q) -> {target_path}")

if __name__ == "__main__":
    convert()
