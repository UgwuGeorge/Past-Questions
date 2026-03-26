import pdfplumber
import re
import os
import sys
import io

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SUBJECTS_BY_LEVEL = {
    "Foundation": [
        "Financial Accounting", "Management Information", 
        "Business, Management and Finance", "Business Law", "Taxation"
    ],
    "Skills": [
        "Financial Reporting", "Audit and Assurance", "Taxation", 
        "Corporate Strategic Management and Ethics", "Performance Management", 
        "Public Sector Accounting and Finance"
    ],
    "Professional": [
        "Corporate Reporting", "Advanced Audit and Assurance", 
        "Strategic Financial Management", "Advanced Taxation", "Case Study"
    ]
}

PDF_FILES = {
    "Foundation": "data/Professional/ICAN/Foundation_May_2024.pdf",
    "Skills": "data/Professional/ICAN/Skills_May_2024.pdf",
    "Professional": "data/Professional/ICAN/Professional_May_2024.pdf"
}

OUTPUT_DIR = "data/Professional/ICAN"

def extract_level(level, pdf_path):
    print(f"Processing {level} level from {pdf_path}...")
    if not os.path.exists(pdf_path):
        print(f"File {pdf_path} not found.")
        return

    subjects = SUBJECTS_BY_LEVEL[level]
    
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Search for subject starts
    subject_starts = []
    for s in subjects:
        # Relaxed matching: just the subject name in the text, case-insensitive
        # Prefer matches followed by "SECTION A", "PAPER", or "EXAMINATION"
        search_name = s.replace(",", "").upper()
        
        best_match = None
        # Find all occurrences
        for match in re.finditer(re.escape(search_name), full_text, re.IGNORECASE):
            start = match.start()
            # Look ahead for context
            context = full_text[start:start+500].upper()
            if "SECTION A" in context or "MULTIPLE-CHOICE" in context or "EXAMINATION" in context:
                best_match = start
                break
        
        if best_match is not None:
            subject_starts.append((best_match, s))
        else:
            # Fallback to any occurrence if no context found
            match = re.search(re.escape(search_name), full_text, re.IGNORECASE)
            if match:
                subject_starts.append((match.start(), s))
    
    subject_starts.sort()
    print(f"  Found {len(subject_starts)} subjects: {[s[1] for s in subject_starts]}")

    for i in range(len(subject_starts)):
        start_idx, s_name = subject_starts[i]
        end_idx = subject_starts[i+1][0] if i+1 < len(subject_starts) else len(full_text)
        
        text = full_text[start_idx:end_idx]
        
        md_content = f"# ICAN {s_name} (2024)\n\n"
        
        # More robust MCQ detection:
        # Match: N. question text ... Choice A ... Choice E ... Answer: X
        # We'll try to find whole question blocks
        q_regex = r'(\d+)\.\s+(.+?)\s+([A-E])\.\s+(.+?)(?=\s+[A-E]\.|\s+ANSWER:|\s+Answer:|\Z)'
        
        questions = []
        current_q = None
        
        # Split text into potential question blocks using numbering
        lines = text.split('\n')
        added_count = 0
        
        # Look for the answer key first (sometimes ICAN has answers at the end of the section)
        # But usually they are after each question.
        
        # Let's use a simpler split and then parse
        potential_qs = re.split(r'\n(?=\d+\.)', text)
        for block in potential_qs:
            # Question number and text
            q_head = re.match(r'(\d+)\.\s+(.+?)(?=\s*[A-E]\.\s+)', block, re.DOTALL)
            if q_head:
                q_num, q_body = q_head.groups()
                choices = re.findall(r'([A-E])\.\s+(.+?)(?=\s+[A-E]\.\s+|\s*[A-E]\s+|\s+ANSWER:|\s+(?:Answer:)|$)', block, re.DOTALL)
                answer = re.search(r'(?:ANSWER|Answer):\s*([A-E])', block)
                
                if choices and answer:
                    ans_label = answer.group(1).upper()
                    md_content += f"**{q_num}.** {q_body.strip().replace('\n', ' ')}\n"
                    for label, c_text in choices:
                        md_content += f"   {label}) {c_text.strip().replace('\n', ' ')}\n"
                    md_content += f"   **Answer: {ans_label}**\n\n"
                    added_count += 1

        if added_count == 0:
            md_content += "## Theory Section\n\n"
            md_content += text[:10000] # More text for theory
        
        safe_name = s_name.replace(" ", "_").replace(",", "")
        out_path = os.path.join(OUTPUT_DIR, level, f"ICAN_{safe_name}_2024.md")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  Saved {out_path} ({added_count} MCQs detected)")

if __name__ == "__main__":
    for level, path in PDF_FILES.items():
        extract_level(level, path)

if __name__ == "__main__":
    for level, path in PDF_FILES.items():
        extract_level(level, path)
