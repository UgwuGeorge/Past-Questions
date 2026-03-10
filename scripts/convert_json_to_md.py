import os
import json
import glob

# Set base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'Academic', 'Secondary', 'WAEC')

def convert_json_to_md():
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    converted_count = 0
    
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        subject_name = data.get("subject_name", "Unknown Subject")
        year = data.get("year", "2023")
        
        # Follow the format expected by agent_core/scripts/import_data.py :
        # # Exam Subject (Year)
        # **1.** Question text
        #    A) Choice A
        #    B) Choice B
        #    **Answer: A**
        
        md_content = f"# {subject_name} ({year})\n\n"
        
        for q in data.get("questions", []):
            num = q.get("number")
            text = q.get("text")
            md_content += f"**{num}.** {text}\n"
            
            correct_label = None
            for choice in q.get("choices", []):
                label = choice.get("label")
                c_text = choice.get("text")
                md_content += f"   {label}) {c_text}\n"
                if choice.get("is_correct"):
                    correct_label = label
                    
            if correct_label:
                # Add extra newline below answer block as expected by import_data regex split behavior
                md_content += f"   **Answer: {correct_label}**\n\n"
                
        # Write to Markdown
        md_file_path = file_path.replace(".json", ".md")
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print(f"Converted: {os.path.basename(md_file_path)}")
        
        # Remove original JSON so we have only MD files
        os.remove(file_path)
        converted_count += 1
        
    print(f"Total converted files: {converted_count}")

if __name__ == "__main__":
    convert_json_to_md()
