import os
import sys

scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper  # type: ignore

class ICANPDFScraper(BaseScraper):
    """
    Downloads ICAN Pathfinder PDFs from accountancyng.com (May 2011 - Nov 2024)
    and converts them to Markdown question files using pdfplumber.
    """

    def __init__(self):
        super().__init__()
        self.pdf_dir = os.path.join(self.base_path, 'raw', 'ICAN', 'pdfs')
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Accounting', 'ICAN')
        self.ensure_dirs(self.pdf_dir, self.md_dir)

    def _build_urls(self):
        """Build all Pathfinder PDF URLs for download."""
        base = "https://www.accountancyng.com/wp-content/uploads"
        levels = ['foundation', 'skills', 'professional']
        diets = ['may', 'november']
        urls = []
        for year in range(2011, 2025):
            for diet in diets:
                for level in levels:
                    # Common pattern observed on accountancyng.com
                    fname = f"ican-{level}-{diet}-{year}-pathfinder.pdf"
                    urls.append(f"{base}/{year}/{fname}")
        return urls

    def _parse_pdf_to_questions(self, pdf_path):
        """
        Parse a Pathfinder PDF and extract questions.
        Returns a list of question dicts.
        """
        try:
            import pdfplumber
        except ImportError:
            print("  [Error] pdfplumber not installed. Run: pip install pdfplumber")
            return []

        questions = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages[:30]:  # Limit to first 30 pages (MCQ section)
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

            # Simple line-by-line parser: look for numbered questions
            lines = full_text.split('\n')
            current_q = None
            options = {}
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Detect question start: e.g. "1. Which of the following..."
                import re
                q_match = re.match(r'^(\d+)[.)]\s+(.+)', line)
                opt_match = re.match(r'^([A-Da-d])[.)]\s+(.+)', line)

                if q_match and int(q_match.group(1)) <= 60:
                    if current_q and len(options) >= 2:
                        questions.append({
                            'question': current_q,
                            'options': {k.lower(): v for k, v in list(options.items())[:4]},
                            'answer': 'a'  # Answer key not always in Pathfinder body
                        })
                    current_q = q_match.group(2)
                    options = {}
                elif opt_match and current_q:
                    key = opt_match.group(1).lower()
                    options[key] = opt_match.group(2)

            if current_q and len(options) >= 2:
                questions.append({
                    'question': current_q,
                    'options': {k.lower(): v for k, v in list(options.items())[:4]},
                    'answer': 'a'
                })
        except Exception as e:
            print(f"  [Parse Error] {pdf_path}: {e}")

        return questions

    def scrape(self):
        print("Starting ICAN Pathfinder PDF scraping...")
        urls = self._build_urls()
        downloaded = 0

        for url in urls:
            fname = url.split('/')[-1]
            # Extract metadata from filename
            parts = fname.replace('.pdf', '').split('-')
            # e.g. ican-professional-may-2015-pathfinder
            try:
                level = parts[1].title()
                diet = parts[2].title()
                year = parts[3]
            except IndexError:
                continue

            pdf_path = self.download_file(url, self.pdf_dir)
            if not pdf_path:
                continue

            downloaded += 1
            questions = self._parse_pdf_to_questions(pdf_path)

            if questions:
                title = f"ICAN {level} Pathfinder {diet} {year}"
                md_filename = f"ICAN_{level}_{diet}_{year}_Pathfinder.md"
                md_path = os.path.join(self.md_dir, md_filename)
                content = self.format_as_md(title, questions)
                self.save_markdown(md_path, content)
                print(f"  [{len(questions)} questions extracted] {md_filename}")

        print(f"ICAN PDF scraping complete. {downloaded} PDFs downloaded.")


if __name__ == "__main__":
    scraper = ICANPDFScraper()
    scraper.scrape()
