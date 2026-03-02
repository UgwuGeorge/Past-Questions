import requests
import json
import os
import time

BASE_PATH = r'C:\Users\USER\.gemini\antigravity\scratch\Past-Questions'
API_BASE = 'https://questions.aloc.com.ng/api/v2/q'
ACCESS_TOKEN = 'ALOC-ad6bb1e7fbf4f457885e'

HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'AccessToken': ACCESS_TOKEN
}

# Map subjects to categories and local paths
SUBJECT_MAP = {
    'mathematics': ('Core', 'Mathematics'),
    'english': ('Core', 'English'),
    'biology': ('Science', 'Biology'),
    'chemistry': ('Science', 'Chemistry'),
    'physics': ('Science', 'Physics'),
    'government': ('Arts', 'Government'),
    'literature-in-english': ('Arts', 'Literature'),
    'crk': ('Arts', 'CRS'),
    'irk': ('Arts', 'IRS'),
    'economics': ('Social_Science', 'Economics'),
    'commerce': ('Social_Science', 'Commerce'),
    'geography': ('Social_Science', 'Geography'),
}

EXAM_TYPE = 'neco'
QUESTIONS_PER_YEAR = 10

def fetch_question(subject, year):
    url = f"{API_BASE}?subject={subject}&year={year}&type={EXAM_TYPE}"
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

def format_question_block(q, idx, year):
    question_text = str(q.get('question', '')).strip()
    options = q.get('option', {}) or {}
    answer = str(q.get('answer', '')).strip().upper()
    solution = str(q.get('solution', '') or '').strip()
    image = q.get('image', '')
    actual_year = q.get('examyear', '')

    lines = [f"**{idx}.** {question_text}"]
    if image: lines.append(f"   *(See diagram: {image})*")
    for key in ['a', 'b', 'c', 'd', 'e']:
        val = (options.get(key, '') or '').strip()
        if val: lines.append(f"   {key.upper()}) {val}")
    lines.append(f"   **Answer: {answer}**")
    if solution and solution != 'None':
        sol_short = solution[:300] + ('...' if len(solution) > 300 else '')
        lines.append(f"   *Explanation: {sol_short}*")
    if actual_year and actual_year != str(year):
        lines.append(f"   *(Note: Closest available year from ALOC database: {actual_year})*")
    lines.append("")
    return "\n".join(lines)

def run_population():
    print("=== NECO Genuine Data Population ===\n")
    for subject_slug, (category, folder_name) in SUBJECT_MAP.items():
        subject_label = subject_slug.replace('-', ' ').title()
        full_folder = os.path.join(BASE_PATH, 'Academic', 'Secondary', 'NECO', category)
        os.makedirs(full_folder, exist_ok=True)
        print(f"\n[SUBJECT] {subject_label}")

        for year in range(2010, 2024):
            print(f"  Processing {year}... ", end='', flush=True)
            collected = []
            for _ in range(QUESTIONS_PER_YEAR):
                q = fetch_question(subject_slug, year)
                if q and q not in collected:
                    collected.append(q)
                time.sleep(0.3)

            if not collected:
                print("no data")
                continue

            filename = f"NECO_{folder_name}_{year}.md"
            filepath = os.path.join(full_folder, filename)
            
            # Skip if already populated (size > 1000 bytes as a safe threshold)
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                print("already populated")
                continue
            md_lines = [f"# NECO {subject_label} Past Questions ({year})\n", "## Objectives\n"]
            for i, q in enumerate(collected, 1):
                md_lines.append(format_question_block(q, i, year))
            md_lines.append("\n---\n*(Source: ALOC open API — questions.aloc.com.ng)*")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("\n".join(md_lines))
            print(f"saved {len(collected)} questions")

if __name__ == "__main__":
    run_population()
