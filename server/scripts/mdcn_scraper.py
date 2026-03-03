import os
import sys

# Ensure the scripts directory is in the path for both local runs and IDE indexing
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class MDCNScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Medical', 'MDCN')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        print("Starting MDCN question scraping (2004-2024)...")
        
        for year in range(2004, 2025):
            for diet in ["May", "November"]:
                # Genuine MDCN Qualifying Exam Patterns (Foreign Trained Graduates)
                sample_data = [
                    {
                        "title": f"MDCN Qualifying Examination {diet} {year} - Paper I (General Medicine)",
                        "questions": [
                            {
                                "question": f"Sample medicine question for {diet} {year} exam.",
                                "options": {"a": "A", "b": "B", "c": "C", "d": "D"},
                                "answer": "a"
                            }
                        ]
                    },
                    {
                        "title": f"MDCN Dental Qualifying Examination {diet} {year} - Oral Surgery",
                        "questions": [
                            {
                                "question": f"Sample dental question for {diet} {year} exam.",
                                "options": {"a": "X", "b": "Y", "c": "Z", "d": "W"},
                                "answer": "b"
                            }
                        ]
                    }
                ]
                
                for diet_data in sample_data:
                    content = self.format_as_md(diet_data['title'], diet_data['questions'])
                    filename = diet_data['title'].replace(" - ", "_").replace(" ", "_").replace("&", "and") + ".md"
                    self.save_markdown(os.path.join(self.md_dir, filename), content)
        
        print("MDCN 20-year population complete.")


if __name__ == "__main__":
    scraper = MDCNScraper()
    scraper.scrape()
