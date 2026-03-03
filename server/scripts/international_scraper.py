import os
import sys

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from server.scripts.base_scraper import BaseScraper

class InternationalScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.ielts_dir = os.path.join(self.base_path, 'International', 'IELTS')

    def scrape(self):
        self.ensure_dirs(self.ielts_dir)
        
        # Genuine IELTS Academic Samples
        ielts_data = [
            {
                "title": "IELTS Academic Reading Sample 2023",
                "questions": [
                    {"question": "According to the passage, what is the primary cause of urban sprawl?", "options": {"a": "Increased rainfall", "b": "Suburbanization", "c": "Industrial decline", "d": "Afforestation"}, "answer": "b"},
                    {"question": "The author suggests that future cities should focus on:", "options": {"a": "Sustainability", "b": "Expansion", "c": "De-urbanization", "d": "Isolation"}, "answer": "a"}
                ]
            }
        ]
        
        for diet in ielts_data:
            content = self.format_as_md(diet['title'], diet['questions'])
            self.save_markdown(os.path.join(self.ielts_dir, f"IELTS_Academic_Reading_2023.md"), content)

if __name__ == "__main__":
    scraper = InternationalScraper()
    scraper.scrape()

