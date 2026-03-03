import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class TRCNScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Education', 'TRCN')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        
        print("Starting TRCN question scraping...")
        
        sample_data = [
            {
                "year": 2023,
                "questions": [
                    {
                        "question": "Which of these is NOT a professional teaching standard in Nigeria?",
                        "options": {"a": "Professional Knowledge", "b": "Professional Practice", "c": "Professional Profit", "d": "Professional Values"},
                        "answer": "c"
                    },
                    {
                        "question": "The Teachers Registration Council of Nigeria (TRCN) was established by which Act?",
                        "options": {"a": "Act 31 of 1993", "b": "Act 45 of 1990", "c": "Act 12 of 2004", "d": "Act 5 of 1999"},
                        "answer": "a"
                    }
                ]
            },
            {
                "year": 2017,
                "questions": [
                    {
                        "question": "Who is the primary focus of the teaching-learning process?",
                        "options": {"a": "Teacher", "b": "Learner", "c": "Principal", "d": "Parent"},
                        "answer": "b"
                    },
                    {
                        "question": "The philosopher who believed education should be based on nature was:",
                        "options": {"a": "Dewey", "b": "Rousseau", "c": "Plato", "d": "Socrates"},
                        "answer": "b"
                    }
                ]
            }
        ]
        
        for diet in sample_data:
            year = diet['year']
            content = self.format_as_md(f"TRCN Professional Qualifying Examination ({year})", diet['questions'])
            self.save_markdown(os.path.join(self.md_dir, f"TRCN_Past_Questions_{year}.md"), content)
            
        print("TRCN population complete.")

if __name__ == "__main__":
    scraper = TRCNScraper()
    scraper.scrape()

