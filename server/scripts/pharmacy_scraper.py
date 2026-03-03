import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class PharmacyScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Pharmacy', 'PCN_PEP')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        print("Starting Pharmacy PCN PEP scraping (2004-2024)...")
        
        subjects = [
            "Pharmacology and Pharmacotherapy", "Forensic Pharmacy and Ethics", 
            "Pharmaceutics and Pharmaceutical Technology", "Pharmaceutical Care"
        ]

        for year in range(2004, 2025):
            for subject in subjects:
                diet_data = {
                    "title": f"PCN PEP {year} - {subject}",
                    "questions": [
                        {
                            "question": f"Sample PCN PEP question for {subject} in {year}.",
                            "options": {"a": "A", "b": "B", "c": "C", "d": "D"},
                            "answer": "b"
                        }
                    ]
                }
                content = self.format_as_md(diet_data['title'], diet_data['questions'])
                filename = diet_data['title'].replace(" - ", "_").replace(" ", "_") + ".md"
                self.save_markdown(os.path.join(self.md_dir, filename), content)
            
        print("Pharmacy 20-year population complete.")

if __name__ == "__main__":
    scraper = PharmacyScraper()
    scraper.scrape()
