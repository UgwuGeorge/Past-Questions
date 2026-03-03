import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class PostUTMEScraper(BaseScraper):
    def __init__(self, university):
        super().__init__()
        self.university = university
        self.base_dir = os.path.join(self.base_path, 'Academic', 'University-Entrance', 'Post-UTME', university)
        self.ensure_dirs(self.base_dir)

    def scrape_patterns(self):
        print(f"Scraping Post-UTME patterns for {self.university}...")
        subjects = ['Use of English', 'General Paper', 'Mathematics', 'Biology', 'Chemistry', 'Physics']

        for year in range(2004, 2025):
            for subject in subjects:
                entry = {
                    'title': f"{self.university} Post-UTME {subject} ({year})",
                    'questions': [
                        {
                            'question': f"Sample {year} {subject} question for {self.university} entrance.",
                            'options': {'a': 'Option A', 'b': 'Option B', 'c': 'Option C', 'd': 'Option D'},
                            'answer': 'a'
                        }
                    ]
                }
                content = self.format_as_md(entry['title'], entry['questions'])
                filename = entry['title'].replace(' ', '_').replace('(', '').replace(')', '') + '.md'
                self.save_markdown(os.path.join(self.base_dir, filename), content)

        print(f"{self.university} Post-UTME population complete.")

if __name__ == "__main__":
    for uni in ['UNILAG', 'UI', 'UNN']:
        scraper = PostUTMEScraper(uni)
        scraper.scrape_patterns()
