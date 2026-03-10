"""
ALOC Fast Scraper (Targeted) — Reharz
=====================================
Uses concurrent threads to fetch targeted data from ALOC questions API.
"""
import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

ALOC_TOKEN = "QB-14323484c8e1eb3c66c0"
BASE_URL = "https://questions.aloc.com.ng/api/v2/q"

SUBJECTS = ['english', 'mathematics', 'physics', 'chemistry', 'biology']
YEARS = [2020, 2021, 2022, 2023]
BATCH_SIZE = 15
MAX_WORKERS = 8

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'aloc_raw')
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
    params = {'subject': subject, 'year': year}
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

def scrape_subject_year(subject, year):
    filepath = os.path.join(DATA_DIR, f"{subject}_{year}_aloc.json")
    if os.path.exists(filepath):
        try:
            with open(filepath) as f:
                existing = json.load(f)
            if isinstance(existing, list) and len(existing) >= BATCH_SIZE:
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
        time.sleep(0.3)

    if questions:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        log(f"  [+] {subject}/{year} — {len(questions)} unique questions saved")
        return len(questions)
    return 0

def scrape_all():
    tasks = [(s, y) for s in SUBJECTS for y in YEARS]
    total = 0

    log(f"\n[*] ALOC Targeted Scrape — {len(tasks)} jobs")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {executor.submit(scrape_subject_year, s, y): (s, y) for s, y in tasks}
        for future in as_completed(future_map):
            try:
                total += future.result()
            except Exception as e:
                pass

    log(f"\n[✓] Scrape Complete! Total questions this run: {total}")

if __name__ == "__main__":
    scrape_all()
