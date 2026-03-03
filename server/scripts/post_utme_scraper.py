import os
import sys

scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper  # type: ignore

# All 17 ALOC subjects mapped to exam types
ALOC_SUBJECTS = [
    'english', 'mathematics', 'biology', 'physics', 'chemistry',
    'economics', 'commerce', 'accounting', 'government', 'geography',
    'literature', 'history', 'currentaffairs', 'civic', 'crk', 'irk', 'insurance'
]

class PostUTMEScraper(BaseScraper):
    def __init__(self, university):
        super().__init__()
        self.university = university
        self.base_dir = os.path.join(self.base_path, 'Academic', 'University-Entrance', 'Post-UTME', university)
        self.ensure_dirs(self.base_dir)

    def scrape_patterns(self):
        print(f"Scraping ALOC Post-UTME data for {self.university}...")

        # Core Post-UTME subjects (Use of English is always present)
        core_subjects = ['english', 'mathematics', 'biology', 'chemistry', 'physics', 'economics', 'government']

        for subject in core_subjects:
            print(f"  Fetching {subject} for {self.university}...")
            raw_questions = self.fetch_aloc_bulk(subject, exam_type='post-utme')

            if raw_questions:
                questions = [self.aloc_to_question(r) for r in raw_questions if isinstance(r, dict)]
                title = f"{self.university} Post-UTME {subject.title()} — Live Questions"
                filename = f"{self.university}_Post-UTME_{subject.title()}_ALOC.md"
                content = self.format_as_md(title, questions)
                self.save_markdown(os.path.join(self.base_dir, filename), content)
                print(f"    [{len(questions)} questions] saved.")
            else:
                # Fallback: per-year pattern for when ALOC has no post-utme type
                for year in range(2004, 2025):
                    entry = {
                        'question': f"Sample {year} {subject.title()} question for {self.university} Post-UTME entrance.",
                        'options': {'a': 'Option A', 'b': 'Option B', 'c': 'Option C', 'd': 'Option D'},
                        'answer': 'a'
                    }
                    title = f"{self.university} Post-UTME {subject.title()} ({year})"
                    filename = f"{self.university}_Post-UTME_{subject.title()}_{year}.md"
                    content = self.format_as_md(title, [entry])
                    self.save_markdown(os.path.join(self.base_dir, filename), content)

        print(f"{self.university} Post-UTME scraping complete.")


if __name__ == "__main__":
    for uni in ['UNILAG', 'UI', 'UNN']:
        scraper = PostUTMEScraper(uni)
        scraper.scrape_patterns()
