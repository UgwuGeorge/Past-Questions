"""
JAMB 2023 Deep Scraper — specialized for UTME recovery
=====================================================
Fetches genuine 2023 JAMB questions from ALOC API.
"""
import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

ALOC_TOKEN = "QB-14323484c8e1eb3c66c0"
BASE_URL = "https://questions.aloc.com.ng/api/v2/q"

# Subjects and their target counts
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
    'history': 40
}

YEAR = 2023
MAX_WORKERS = 5 # Lower workers to avoid aggressive rate limiting

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), 'data', 'jamb_2023_raw')
os.makedirs(DATA_DIR, exist_ok=True)

print_lock = Lock()

def log(msg):
    with print_lock:
        print(msg, flush=True)

def fetch_one(subject, year):
    headers = {
        'Accept': 'application/json',
        'AccessToken': ALOC_TOKEN
    }
    params = {'subject': subject, 'year': year, 'type': 'utme'}
    try:
        r = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 200:
                d = data.get('data')
                if isinstance(d, list) and d:
                    return d[0]
                elif isinstance(d, dict) and d.get('id'):
                    return d
        return None
    except Exception:
        return None

def scrape_subject(subject, target_count):
    log(f"[*] Starting {subject} (Target: {target_count})...")
    filepath = os.path.join(DATA_DIR, f"{subject}_{YEAR}.json")
    
    seen_ids = set()
    questions = []
    
    # Check for existing
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                questions = json.load(f)
                seen_ids = {q['id'] for q in questions if 'id' in q}
        except Exception:
            pass
            
    if len(questions) >= target_count:
        log(f"  [-] {subject} already complete ({len(questions)}q)")
        return len(questions)

    attempts = 0
    max_attempts = target_count * 3 # Allow for duplicates
    
    while len(questions) < target_count and attempts < max_attempts:
        attempts += 1
        q = fetch_one(subject, YEAR)
        if q and isinstance(q, dict):
            qid = q.get('id')
            if qid and qid not in seen_ids:
                questions.append(q)
                seen_ids.add(qid)
                if len(questions) % 5 == 0:
                    log(f"  [+] {subject}: {len(questions)}/{target_count}")
        
        time.sleep(0.5) # Throttle

    if questions:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        log(f"  [DONE] {subject} saved: {len(questions)} unique questions")
        return len(questions)
    
    return 0

def run_deep_scrape():
    total = 0
    log(f"\nJAMB 2023 Deep Scrape Initialized")
    log(f"====================================")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {executor.submit(scrape_subject, s, c): s for s, c in SUBJECTS.items()}
        for future in as_completed(future_map):
            try:
                total += future.result()
            except Exception as e:
                log(f"  [!] Error in {future_map[future]}: {e}")

    log(f"\n[FINAL STATUS] Scrape Complete. Total unique questions retrieved: {total}")

if __name__ == "__main__":
    run_deep_scrape()
