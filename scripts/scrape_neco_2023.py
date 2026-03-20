"""
NECO 2023 Scraper — ALOC API → .md files
==========================================
Fetches genuine NECO 2023 questions and saves as formatted .md files
mirroring the JAMB 2023 structure.
"""
import urllib.request
import urllib.parse
import json
import os
import time
import ssl

ALOC_TOKEN = "QB-14323484c8e1eb3c66c0"
BASE_URL = "https://questions.aloc.com.ng/api/v2/q"
YEAR = 2023

SUBJECTS = {
    'english': 60,
    'mathematics': 40,
    'physics': 40,
    'chemistry': 40,
    'biology': 40,
    'economics': 40,
    'government': 40,
    'commerce': 40,
    'geography': 40,
    'accounting': 40,
    'history': 40,
    'civic-education': 40,
    'agricultural-science': 40,
    'literature-in-english': 40,
}

SUBJECT_DISPLAY = {
    'english': 'English',
    'mathematics': 'Mathematics',
    'physics': 'Physics',
    'chemistry': 'Chemistry',
    'biology': 'Biology',
    'economics': 'Economics',
    'government': 'Government',
    'commerce': 'Commerce',
    'geography': 'Geography',
    'accounting': 'Accounting',
    'history': 'History',
    'civic-education': 'Civic-Education',
    'agricultural-science': 'Agricultural-Science',
    'literature-in-english': 'Literature-in-English',
}

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data', 'Academic', 'NECO')
os.makedirs(DATA_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_one(subject, year):
    params = urllib.parse.urlencode({'subject': subject, 'year': year, 'type': 'neco'})
    url = f"{BASE_URL}?{params}"
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'AccessToken': ALOC_TOKEN
    })
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
            data = json.loads(r.read())
            if data.get('status') == 200:
                d = data.get('data')
                if isinstance(d, list) and d:
                    return d[0]
                elif isinstance(d, dict) and d.get('id'):
                    return d
        return None
    except Exception:
        return None

def question_to_md(num, q):
    text = q.get('question', '').strip()
    opts = q.get('option', {})
    answer = (q.get('answer') or '').strip().upper()
    solution = (q.get('solution') or '').strip()
    image = (q.get('image') or '').strip()

    lines = [f"**{num}.** {text}"]

    if image:
        lines.append(f"   *(See image: {image})*")

    label_map = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'}
    for label in ['A', 'B', 'C', 'D']:
        opt_text = opts.get(label.lower()) or opts.get(label) or ''
        if opt_text and str(opt_text).strip():
            lines.append(f"   {label}) {str(opt_text).strip()}")

    lines.append(f"   **Answer: {answer}**")
    if solution:
        lines.append(f"   *Explanation: {solution}*")

    return '\n'.join(lines)

def scrape_subject(slug, display_name, target_count):
    subject_dir = os.path.join(DATA_DIR, display_name)
    os.makedirs(subject_dir, exist_ok=True)
    output_path = os.path.join(subject_dir, '2023.md')

    # Skip if already complete
    if os.path.exists(output_path):
        existing = open(output_path, encoding='utf-8').read()
        count = existing.count('\n**')
        if count >= target_count:
            print(f"  [SKIP] {display_name} already has {count} questions")
            return count

    print(f"[*] Scraping NECO 2023 {display_name} (target: {target_count})...")
    
    seen_ids = set()
    questions = []
    attempts = 0
    max_attempts = target_count * 4

    while len(questions) < target_count and attempts < max_attempts:
        attempts += 1
        q = fetch_one(slug, YEAR)
        if q and isinstance(q, dict):
            qid = q.get('id')
            if qid and qid not in seen_ids:
                questions.append(q)
                seen_ids.add(qid)
                if len(questions) % 10 == 0:
                    print(f"  [+] {display_name}: {len(questions)}/{target_count}")
        time.sleep(0.4)

    if not questions:
        print(f"  [!] {display_name}: No questions retrieved.")
        return 0

    # Write .md file
    md_lines = [
        f"# NECO {display_name} Past Questions - {YEAR}",
        "",
        "## Questions",
        ""
    ]
    for i, q in enumerate(questions, 1):
        md_lines.append(question_to_md(i, q))
        md_lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(f"  [DONE] {display_name}: {len(questions)} questions saved -> {output_path}")
    return len(questions)

def run():
    print("\nNECO 2023 Scraper — ALOC API")
    print("=" * 40)
    total = 0
    results = {}

    for slug, target in SUBJECTS.items():
        display = SUBJECT_DISPLAY[slug]
        count = scrape_subject(slug, display, target)
        results[display] = count
        total += count
        time.sleep(1)  # Pause between subjects

    print("\n" + "=" * 40)
    print("NECO 2023 Scrape Complete")
    print(f"{'Subject':<30} {'Questions':>10}")
    print("-" * 42)
    for subj, cnt in results.items():
        status = "✓" if cnt >= 10 else "✗"
        print(f"{status} {subj:<28} {cnt:>10}")
    print("-" * 42)
    print(f"  {'TOTAL':<28} {total:>10}")

if __name__ == "__main__":
    run()
