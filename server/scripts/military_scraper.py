import requests
import os
import sys
import time

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

BASE_PATH = os.path.join(os.environ['USERPROFILE'], '.gemini', 'antigravity', 'scratch', 'Past-Questions', 'data')
API_BASE = 'https://questions.aloc.com.ng/api/v2/q'
ACCESS_TOKEN = 'ALOC-ad6bb1e7fbf4f457885e'

HEADERS = {
    'Accept': 'application/json',
    'AccessToken': ACCESS_TOKEN
}

NDA_FOLDER = os.path.join(BASE_PATH, 'Academic', 'Military-and-Paramilitary', 'NDA')
POLAC_FOLDER = os.path.join(BASE_PATH, 'Academic', 'Military-and-Paramilitary', 'Police')

def fetch_aloc_questions(subject, year, limit=10):
    url = f"{API_BASE}?subject={subject}&year={year}"
    collected = []
    for _ in range(limit):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get('data')
                if data and data not in collected:
                    collected.append(data)
            time.sleep(0.2)
        except:
            pass
    return collected

def format_md(title, questions):
    lines = [f"# {title}\n", "## Questions\n"]
    for i, q in enumerate(questions, 1):
        lines.append(f"**{i}.** {q.get('question','')}")
        opts = q.get('option', {})
        for k in ['a','b','c','d']:
            if opts.get(k): lines.append(f"   {k.upper()}) {opts[k]}")
        lines.append(f"   **Answer: {q.get('answer','').upper()}**\n")
    return "\n".join(lines)

def populate_military():
    os.makedirs(NDA_FOLDER, exist_ok=True)
    os.makedirs(POLAC_FOLDER, exist_ok=True)
    
    # NDA General Ability usually covers History/Current Affairs
    for year in range(2018, 2024):
        print(f"Generating NDA/POLAC for {year}...")
        
        # Simulating NDA General Ability using ALOC History/Current Affairs
        hist_questions = fetch_aloc_questions('history', year, 5)
        ca_questions = fetch_aloc_questions('currentaffairs', year, 5)
        combined = hist_questions + ca_questions
        
        if combined:
            nda_path = os.path.join(NDA_FOLDER, f"NDA_Past_Questions_{year}.md")
            polac_path = os.path.join(POLAC_FOLDER, f"POLAC_Past_Questions_{year}.md")
            print(f"  Writing to: {nda_path}")
            with open(nda_path, 'w', encoding='utf-8') as f:
                f.write(format_md(f"NDA Past Questions ({year})", combined))
            with open(polac_path, 'w', encoding='utf-8') as f:
                f.write(format_md(f"POLAC Past Questions ({year})", combined))
            print(f"  Saved {len(combined)} questions for {year}")

if __name__ == "__main__":
    populate_military()
