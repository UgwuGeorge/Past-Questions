import pdfplumber  # type: ignore
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

def extract_deep_scan(pdf_path, level):
    print(f"\n--- Scanning {pdf_path} ({level}) ---")
    if not os.path.exists(pdf_path):
        print(f"File {pdf_path} not found.")
        return

    subjects = SUBJECTS_BY_LEVEL[level]
    subject_pages = {}

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text: continue
            
            # Check the top of the page for subject headers
            # Subject headers are often the only thing on the first line or centered
            lines = text.split('\n')
            top_text = "\n".join(lines[:10]).upper()
            
            for s in subjects:
                search_name = s.replace(",", "").upper()
                # Use regex to find subject name as a whole word/line
                if re.search(r'\b' + re.escape(search_name) + r'\b', top_text):
                    if s not in subject_pages:
                        # Heuristic: exclude TOC pages (usually early)
                        if i > 2: 
                            subject_pages[s] = i
        
        sorted_subjects = sorted(subject_pages.items(), key=lambda x: x[1])
        print(f"  Detected subject starts: {sorted_subjects}")

        for i, (name, start_p) in enumerate(sorted_subjects):
            # The subject ends when the next one starts OR at the end of the PDF
            end_p = sorted_subjects[i+1][1] if i+1 < len(sorted_subjects) else len(pdf.pages)
            
            if end_p <= start_p:
                # If logic failed, use a fixed range of 50 pages or end of PDF
                end_p = min(start_p + 50, len(pdf.pages))

            print(f"  Extracting {name} from page {start_p+1} to {end_p}")
            subject_text: str = ""
            for p_idx in range(start_p, end_p):
                p_text = pdf.pages[p_idx].extract_text()
                if p_text:
                    subject_text += str(p_text) + "\n"  # type: ignore
            
            # Determine diet name from path
            # e.g. Foundation_May_2024.pdf -> May_2024
            parts = os.path.basename(pdf_path).replace(".pdf", "").split("_")
            diet_name = "_".join(parts[-2:])
            
            md_content: str = f"# ICAN {name} ({diet_name})\n\n"
            
            # Parsing MCQs
            added_count: int = 0
            # Standard ICAN MCQ format
            q_blocks = re.split(r'\n(?=\d+\.)', subject_text)
            for block in q_blocks:
                q_head = re.match(r'(\d+)\.\s+(.+?)(?=\s*[A-E]\.\s+)', block, re.DOTALL)
                if q_head:
                    q_num, q_body = q_head.groups()
                    choices = re.findall(r'([A-E])\.\s+(.+?)(?=\s+[A-E]\.\s+|\s*[A-E]\s+|\s+ANSWER:|\s+(?:Answer:)|$)', block, re.DOTALL)
                    answer = re.search(r'(?:ANSWER|Answer):\s*([A-E])', block)
                    if choices and answer:
                        ans_label = str(answer.group(1)).upper()
                        md_content += f"**{q_num}.** {q_body.strip().replace('\n', ' ')}\n"  # type: ignore
                        for label, c_text in choices:
                            md_content += f"   {label}) {c_text.strip().replace('\n', ' ')}\n"  # type: ignore
                        md_content += f"   **Answer: {ans_label}**\n\n"  # type: ignore
                        added_count += 1
            
            if added_count < 2:
                md_content += "## Theory and Practice Section\n\n"  # type: ignore
                md_content += str(subject_text)  # type: ignore

            safe_name = name.replace(" ", "_").replace(",", "")
            out_path = f"data/Professional/ICAN/{level}/ICAN_{safe_name}_{diet_name}.md"
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"    Saved {out_path} ({added_count} MCQs, {len(subject_text)} chars)")

if __name__ == "__main__":
    files = [
        ("Foundation", "data/Professional/ICAN/Foundation_May_2024.pdf"),
        ("Skills", "data/Professional/ICAN/Skills_May_2024.pdf"),
        ("Professional", "data/Professional/ICAN/Professional_May_2024.pdf"),
        ("Foundation", "data/Professional/ICAN/Foundation_Nov_2023.pdf"),
        ("Skills", "data/Professional/ICAN/Skills_Nov_2023.pdf"),
        ("Professional", "data/Professional/ICAN/Professional_Nov_2023.pdf"),
    ]
    for level, path in files:
        if os.path.exists(path):
            extract_deep_scan(path, level)
        else:
            print(f"Skipping {path}")
