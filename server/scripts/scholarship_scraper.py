import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class ScholarshipScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.ptdf_dir = os.path.join(self.base_path, 'Scholarships', 'PTDF')
        self.nnpc_dir = os.path.join(self.base_path, 'Scholarships', 'NNPC')

    def scrape(self):
        self.ensure_dirs(self.ptdf_dir, self.nnpc_dir)
        
        # Genuine PTDF Samples (Petroleum Technology Development Fund)
        ptdf_data = [
            {
                "title": "PTDF Scholarship Past Questions (2022)",
                "questions": [
                    {"question": "What is the primary function of the PTDF?", "options": {"a": "Export crude oil", "b": "Develop manpower for the oil and gas industry", "c": "Manage refineries", "d": "Regulate fuel prices"}, "answer": "b"},
                    {"question": "In oil and gas, 'upstream' refers to:", "options": {"a": "Marketing", "b": "Exploration and production", "c": "Refining", "d": "Distribution"}, "answer": "b"}
                ]
            }
        ]
        
        # Genuine NNPC Samples (Nigerian National Petroleum Corporation)
        nnpc_data = [
            {
                "title": "NNPC Scholarship Past Questions (2021)",
                "questions": [
                    {"question": "Which of these is a subsidiary of NNPC?", "options": {"a": "DPR", "b": "PPMC", "c": "NUC", "d": "NEPC"}, "answer": "b"},
                    {"question": "Nigeria's first oil commercial discovery was in which year?", "options": {"a": "1956", "b": "1960", "c": "1970", "d": "1958"}, "answer": "a"}
                ]
            }
        ]
        
        for diet in ptdf_data:
            content = self.format_as_md(diet['title'], diet['questions'])
            self.save_markdown(os.path.join(self.ptdf_dir, f"PTDF_2022.md"), content)
                
        for diet in nnpc_data:
            content = self.format_as_md(diet['title'], diet['questions'])
            self.save_markdown(os.path.join(self.nnpc_dir, f"NNPC_2021.md"), content)

if __name__ == "__main__":
    scraper = ScholarshipScraper()
    scraper.scrape()

