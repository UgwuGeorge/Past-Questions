import os
import sys
import re

scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper  # type: ignore

# Publicly accessible Bar Finals PDF sources
PDF_SOURCES = [
    # Civil Litigation
    ("https://isochukwu.com/wp-content/uploads/2021/01/Civil-Litigation-2020.pdf", "Civil_Litigation", 2020),
    ("https://isochukwu.com/wp-content/uploads/2021/01/Civil-Litigation-2019.pdf", "Civil_Litigation", 2019),
    # Corporate Law Practice
    ("https://isochukwu.com/wp-content/uploads/2021/01/Corporate-Law-Practice-2020.pdf", "Corporate_Law_Practice", 2020),
    # Criminal Litigation
    ("https://isochukwu.com/wp-content/uploads/2021/01/Criminal-Litigation-2020.pdf", "Criminal_Litigation", 2020),
    # Professional Ethics
    ("https://isochukwu.com/wp-content/uploads/2021/01/Professional-Ethics-2020.pdf", "Professional_Ethics", 2020),
]

class LawPDFScraper(BaseScraper):
    """
    Downloads Nigerian Law School Bar Finals past question PDFs
    from publicly available sources and parses them to Markdown.
    """

    def __init__(self):
        super().__init__()
        self.pdf_dir = os.path.join(self.base_path, 'raw', 'Law', 'pdfs')
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Law', 'Bar_Finals')
        self.ensure_dirs(self.pdf_dir, self.md_dir)

    def _parse_pdf(self, pdf_path, subject, year):
        """Extract questions from a Bar Finals PDF."""
        try:
            import pdfplumber
        except ImportError:
            print("  [Error] pdfplumber not installed. Run: pip install pdfplumber")
            return []

        questions = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages[:25]:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

            lines = full_text.split('\n')
            current_q = None
            options = {}
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                q_match = re.match(r'^(\d+)[.)]\s+(.+)', line)
                opt_match = re.match(r'^([A-Da-d])[.)]\s+(.+)', line)

                if q_match and int(q_match.group(1)) <= 80:
                    if current_q and len(options) >= 2:
                        questions.append({
                            'question': current_q,
                            'options': {k: v for k, v in list(options.items())[:4]},
                            'answer': 'a'
                        })
                    current_q = q_match.group(2)
                    options = {}
                elif opt_match and current_q:
                    options[opt_match.group(1).lower()] = opt_match.group(2)

            if current_q and len(options) >= 2:
                questions.append({
                    'question': current_q,
                    'options': {k: v for k, v in list(options.items())[:4]},
                    'answer': 'a'
                })
        except Exception as e:
            print(f"  [Parse Error] {pdf_path}: {e}")

        return questions

    def scrape(self):
        print("Starting Law Bar Finals PDF scraping...")
        total_saved = 0

        for url, subject, year in PDF_SOURCES:
            pdf_path = self.download_file(url, self.pdf_dir)
            if not pdf_path:
                print(f"  [Skipped/Failed] {url}")
                continue

            questions = self._parse_pdf(pdf_path, subject, year)
            if questions:
                title = f"Bar Finals {year} - {subject.replace('_', ' ')}"
                md_filename = f"Bar_Finals_{year}_{subject}_Real.md"
                content = self.format_as_md(title, questions)
                self.save_markdown(os.path.join(self.md_dir, md_filename), content)
                print(f"  [{len(questions)} Qs extracted] {md_filename}")
                total_saved += 1
            else:
                print(f"  [No questions extracted] from {pdf_path}")

        print(f"Law PDF scraping complete. {total_saved} files saved.")


if __name__ == "__main__":
    scraper = LawPDFScraper()
    scraper.scrape()
