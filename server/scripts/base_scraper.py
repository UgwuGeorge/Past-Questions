import os
import requests
import time

class BaseScraper:
    def __init__(self, base_path=None):
        self.base_path = base_path or os.path.join(os.environ['USERPROFILE'], '.gemini', 'antigravity', 'scratch', 'Past-Questions', 'data')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
    # Test instance
    scraper = BaseScraper()
    print("BaseScraper initialized.")
