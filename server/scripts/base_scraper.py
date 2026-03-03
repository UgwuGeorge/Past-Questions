import os
import requests
import time
import html
import random

ALOC_API_BASE = 'https://questions.aloc.com.ng/api/v2'
ALOC_TOKEN = 'ALOC-ad6bb1e7fbf4f457885e'
ALOC_HEADERS = {'Accept': 'application/json', 'AccessToken': ALOC_TOKEN}

OPEN_TRIVIA_URL = 'https://opentdb.com/api.php'


class BaseScraper:
    def __init__(self, base_path=None):
        self.base_path = base_path or os.path.join(
            os.environ['USERPROFILE'], '.gemini', 'antigravity', 'scratch', 'Past-Questions', 'data'
        )
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def ensure_dirs(self, *dirs):
        for d in dirs:
            os.makedirs(d, exist_ok=True)

    def download_file(self, url, folder):
        local_filename = os.path.join(folder, url.split('/')[-1])
        if os.path.exists(local_filename):
            print(f"  [Skipped] {local_filename} already exists.")
            return local_filename
        print(f"  [Downloading] {url}...")
        try:
            with requests.get(url, stream=True, headers=self.headers, timeout=30) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return local_filename
        except Exception as e:
            print(f"  [Error] Failed to download {url}: {e}")
            return None

    def fetch_aloc_bulk(self, subject, exam_type=None, year=None, limit=40):
        """Fetch up to `limit` questions from the ALOC bulk endpoint (/m)."""
        url = f"{ALOC_API_BASE}/m?subject={subject}"
        if exam_type:
            url += f"&type={exam_type}"
        if year:
            url += f"&year={year}"
        questions = []
        try:
            resp = requests.get(url, headers=ALOC_HEADERS, timeout=15)
            if resp.status_code == 200:
                data = resp.json().get('data', [])
                if isinstance(data, list):
                    questions = list(data)[:limit]
                elif isinstance(data, dict):
                    questions = [data]
            time.sleep(0.3)
        except Exception as e:
            print(f"  [ALOC Error] {subject} {year}: {e}")
        return questions

    def aloc_to_question(self, raw):
        """Convert a raw ALOC API dict into our standard question format."""
        opts = raw.get('option', {}) or {}
        return {
            'question': raw.get('question', ''),
            'options': {
                'a': opts.get('a', ''),
                'b': opts.get('b', ''),
                'c': opts.get('c', ''),
                'd': opts.get('d', ''),
            },
            'answer': str(raw.get('answer', 'a')).lower()
        }

    def fetch_open_trivia(self, category=17, difficulty='hard', amount=20):
        """
        Fetch questions from Open Trivia DB.
        Category 17 = Science & Nature (used for Medical/Pharmacy).
        Category 20 = Mythology. Category 23 = History. etc.
        """
        questions = []
        try:
            params = {
                'amount': amount,
                'category': category,
                'difficulty': difficulty,
                'type': 'multiple'
            }
            resp = requests.get(OPEN_TRIVIA_URL, params=params, timeout=15)
            if resp.status_code == 200:
                raw_list = resp.json().get('results', [])
                for item in raw_list:
                    q_text = html.unescape(item.get('question', ''))
                    correct = html.unescape(item.get('correct_answer', ''))
                    incorrect = [html.unescape(x) for x in item.get('incorrect_answers', [])]
                    options_list = [correct] + incorrect
                    random.shuffle(options_list)
                    correct_key = next(
                        (k for k, v in zip('abcd', options_list) if v == correct), 'a'
                    )
                    questions.append({
                        'question': q_text,
                        'options': dict(zip('abcd', options_list)),
                        'answer': correct_key
                    })
            time.sleep(0.5)  # OTD rate limit: 1 request per 5s recommended
        except Exception as e:
            print(f"  [OpenTrivia Error]: {e}")
        return questions

    def format_as_md(self, title, questions):
        lines = [f"# {title}\n", "## Questions\n"]
        for i, q in enumerate(questions, 1):
            lines.append(f"**{i}.** {q['question']}")
            if 'options' in q:
                for k, v in q['options'].items():
                    lines.append(f"   {k.upper()}) {v}")
            if 'answer' in q:
                lines.append(f"   **Answer: {q['answer'].upper()}**\n")
        return "\n".join(lines)

    def save_markdown(self, filepath, content):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [Saved] {filepath}")


if __name__ == "__main__":
    scraper = BaseScraper()
    print("BaseScraper initialized.")
