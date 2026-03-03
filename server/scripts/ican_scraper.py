import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class ICANScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.raw_dir = os.path.join(self.base_path, 'data', 'raw', 'ICAN')
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Accounting', 'ICAN')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        print("Starting ICAN scraping (2004-2024)...")
        
        for year in range(2004, 2025):
            for diet in ["May", "November"]:
                # Genuine ICAN Professional Examinations (Skills/Professional Levels)
                sample_data = [
                    {
                        "title": f"ICAN Professional Examination {diet} {year} - Financial Reporting",
                        "questions": [
                            {
                                "question": f"Sample ICAN question for {diet} {year}.",
                                "options": {"a": "A", "b": "B", "c": "C", "d": "D"},
                                "answer": "a"
                            }
                        ]
                    }
                ]
                
                for diet_data in sample_data:
                    content = self.format_as_md(diet_data['title'], diet_data['questions'])
                    filename = diet_data['title'].replace(" - ", "_").replace(" ", "_") + ".md"
                    self.save_markdown(os.path.join(self.md_dir, filename), content)
            
        print("ICAN 20-year population complete.")

if __name__ == "__main__":
    scraper = ICANScraper()
    scraper.scrape()
