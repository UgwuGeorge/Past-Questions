import requests
import json
import os
import sys
import time
from typing import Dict, Any, cast

# Add project root to sys.path
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

BASE_PATH = os.path.join(project_root, 'data')
API_BASE = 'https://questions.aloc.com.ng/api/v2/q'
# Use the token from .env
from dotenv import load_dotenv
load_dotenv()
ACCESS_TOKEN = os.getenv("ALOC_ACCESS_TOKEN", 'ALOC-ad6bb1e7fbf4f457885e')

HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'AccessToken': ACCESS_TOKEN
}

SUBJECT_TARGETS = ['english', 'mathematics']
YEAR = 2023
QUESTIONS_TO_GET = 55 # Aim for 50 unique

def fetch_question(subject, year):
    url = f"{API_BASE}?subject={subject}&year={year}&type=neco"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            payload = resp.json()
            raw = payload.get('data', None)
            if isinstance(raw, dict): return raw
            elif isinstance(raw, list) and len(raw) > 0: return raw[0]
        return None
    except Exception as e:
        print(f"Error fetching {subject} {year}: {e}")
        return None

def format_question_block(q: Any, idx: int) -> str:
    if not isinstance(q, dict): return ""
    question_text = str(q.get('question', '')).strip()
    options = cast(Dict[str, Any], q.get('option', {}))
    answer = str(q.get('answer', '')).strip().upper()
    solution = str(q.get('solution', '') or '').strip()
    image = q.get('image', '')
    
    lines = [f"**{idx}.** {question_text}"]
    if image: lines.append(f"   *(See diagram: {image})*")
    for key in ['a', 'b', 'c', 'd', 'e']:
        val = str(options.get(key, '') or '').strip()
        if val: lines.append(f"   {key.upper()}) {val}")
    lines.append(f"   **Answer: {answer}**")
    if solution and solution.lower() != 'none':
        lines.append(f"   *Explanation: {solution[:300]}*")
    lines.append("")
    return "\n".join(lines)

def run_targeted_scrape():
    print(f"=== NECO {YEAR} Targeted Scrape (English & Math) ===\n")
    for subject_slug in SUBJECT_TARGETS:
        print(f"\n[SUBJECT] {subject_slug.upper()}")
        collected = []
        seen_texts = set()
        
        for i in range(QUESTIONS_TO_GET):
            print(f"\r  Progress: {i+1}/{QUESTIONS_TO_GET} ... ", end='', flush=True)
            q = fetch_question(subject_slug, YEAR)
            if q:
                q_text = q.get('question', '')
                if q_text not in seen_texts:
                    collected.append(q)
                    seen_texts.add(q_text)
            time.sleep(0.3)
        
        print(f"\n  Collected {len(collected)} unique questions.")
        
        # Determine save path (keep consistency with populate_neco.py)
        # mathematics -> Core/Mathematics, english -> Core/English
        folder_name = "Mathematics" if subject_slug == "mathematics" else "English"
        full_folder = os.path.join(BASE_PATH, 'Academic', 'Secondary', 'NECO', 'Core')
        os.makedirs(full_folder, exist_ok=True)
        
        filename = f"NECO_{folder_name}_{YEAR}.md"
        filepath = os.path.join(full_folder, filename)
        
        md_lines = [f"# NECO {subject_slug.title()} Past Questions ({YEAR})\n", "## Objectives\n"]
        for i, q in enumerate(collected, 1):
            md_lines.append(format_question_block(q, i))
        md_lines.append("\n---\n*(Source: ALOC open API — questions.aloc.com.ng)*")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines))
        print(f"  Saved to {filepath}")

if __name__ == "__main__":
    run_targeted_scrape()
