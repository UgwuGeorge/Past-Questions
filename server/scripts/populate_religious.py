import requests
import os
import time

BASE_PATH = r'C:\Users\USER\.gemini\antigravity\scratch\Past-Questions'
API_BASE = 'https://questions.aloc.com.ng/api/v2/q'
ACCESS_TOKEN = 'ALOC-ad6bb1e7fbf4f457885e'

HEADERS = {
    'Accept': 'application/json',
    'AccessToken': ACCESS_TOKEN
}

SUBJECTS = {
    'crk': 'CRS',
    'irk': 'IRS'
}

def fetch_questions(subject, year, limit=10):
    url = f"{API_BASE}?subject={subject}&year={year}&type=neco"
    collected = []
    for _ in range(limit):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                data = resp.json().get('data')
                if data and data not in collected:
                    collected.append(data)
            time.sleep(0.3)
        except:
            pass
    return collected

def format_md(title, questions):
    lines = [f"# {title}\n", "## Objectives\n"]
    for i, q in enumerate(questions, 1):
        lines.append(f"**{i}.** {q.get('question','')}")
        opts = q.get('option', {}) or {}
        for k in ['a','b','c','d','e']:
            val = (opts.get(k) or '').strip()
            if val: lines.append(f"   {k.upper()}) {val}")
        lines.append(f"   **Answer: {str(q.get('answer','')).upper()}**\n")
    lines.append("\n---\n*(Source: ALOC open API — questions.aloc.com.ng)*")
    return "\n".join(lines)

def populate():
    for slug, folder in SUBJECTS.items():
        print(f"Populating {folder}...")
        path = os.path.join(BASE_PATH, 'Academic', 'Secondary', 'NECO', 'Arts')
        os.makedirs(path, exist_ok=True)
        for year in range(2010, 2024):
            print(f"  {year}...", end=' ', flush=True)
            qs = fetch_questions(slug, year)
            if qs:
                with open(os.path.join(path, f"NECO_{folder}_{year}.md"), 'w', encoding='utf-8') as f:
                    f.write(format_md(f"NECO {folder} Past Questions ({year})", qs))
                print(f"saved {len(qs)}")
            else:
                print("failed/no data")

if __name__ == "__main__":
    populate()
