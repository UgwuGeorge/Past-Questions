"""
ALOC Fast Scraper — Reharz
===========================
Uses concurrent threads to fetch data from the ALOC questions API at speed.
Token: QB-14323484c8e1eb3c66c0
"""
import requests
import json
import os
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

ALOC_TOKEN = "QB-14323484c8e1eb3c66c0"
BASE_URL = "https://questions.aloc.com.ng/api/v2/q"

# All subjects supported by ALOC
SUBJECTS = [
    'english', 'mathematics', 'biology', 'chemistry', 'physics',
    'accounting', 'government', 'economics', 'commerce', 'agriculture',
    'history', 'geography', 'civicedu', 'currentaffairs', 'crk', 'irk',
    'englishlit', 'insurance'
]

YEARS = list(range(2000, 2024))  # extend back to year 2000
BATCH_SIZE = 20   # attempts per year (deduped)
MAX_WORKERS = 8   # concurrent threads

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'aloc_raw')
os.makedirs(DATA_DIR, exist_ok=True)

print_lock = Lock()

def log(msg):
    with print_lock:
        print(msg, flush=True)

def fetch_one(subject, year):
    """Fetch a single random question for a subject/year from ALOC."""
    headers = {
        'Accept': 'application/json',
        'AccessToken': ALOC_TOKEN
    }
    params = {'subject': subject, 'year': year}
    try:
        r = requests.get(BASE_URL, headers=headers, params=params, timeout=12)
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 200:
                d = data.get('data')
                # API sometimes returns a list, sometimes a dict
                if isinstance(d, list) and d:
                    return d[0]
                elif isinstance(d, dict) and d.get('id'):
                    return d
        return None
    except Exception:
        return None

def scrape_subject_year(subject, year):
    """Fetch BATCH_SIZE unique questions for one subject/year combo."""
    # Skip if file already exists with meaningful content
    filepath = os.path.join(DATA_DIR, f"{subject}_{year}_aloc.json")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 200:
        try:
            with open(filepath) as f:
                existing = json.load(f)
            if isinstance(existing, list) and len(existing) >= BATCH_SIZE:
                log(f"  [~] Skip {subject}/{year} — already have {len(existing)} Qs")
                return len(existing)
        except Exception:
            pass

    seen_ids = set()
    questions = []

    for _ in range(BATCH_SIZE):
        q = fetch_one(subject, year)
        if q and isinstance(q, dict):
            qid = q.get('id')
            if qid and qid not in seen_ids:
                questions.append(q)
                seen_ids.add(qid)
        time.sleep(0.3)  # small delay per request

    if questions:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        log(f"  [+] {subject}/{year} — {len(questions)} unique questions saved")
        return len(questions)
    else:
        log(f"  [-] {subject}/{year} — no data returned")
        return 0

def scrape_all():
    tasks = [(subj, yr) for subj in SUBJECTS for yr in YEARS]
    total = 0

    log(f"\n[*] ALOC Mass Scrape — {len(tasks)} jobs, {MAX_WORKERS} threads")
    log(f"    Token: {ALOC_TOKEN[:8]}...")
    log(f"    Subjects: {len(SUBJECTS)} | Years: {YEARS[0]}–{YEARS[-1]} | Batch: {BATCH_SIZE}\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {executor.submit(scrape_subject_year, s, y): (s, y) for s, y in tasks}
        done = 0
        for future in as_completed(future_map):
            subj, yr = future_map[future]
            try:
                count = future.result()
                total += count
            except Exception as e:
                log(f"  [x] Error {subj}/{yr}: {e}")
            done += 1
            if done % 20 == 0:
                log(f"\n  ── Progress: {done}/{len(tasks)} jobs done, {total} Qs total ──\n")

    log(f"\n[✓] Scrape Complete! {total} total questions saved to: {DATA_DIR}")

if __name__ == "__main__":
    scrape_all()
