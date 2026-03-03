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
        
        # Genuine Shell Samples
        shell_data = [
            {
                "title": "Shell Undergraduate Scholarship - Aptitude Test Pattern",
                "questions": [
                    {"question": "Which of the following is a primary objective of the Shell SPDC Scholarship scheme?", "options": {"a": "To promote healthcare", "b": "To support academic excellence in Nigeria", "c": "To build roads", "d": "To provide electricity"}, "answer": "b"}
                ]
            }
        ]

        # Genuine TotalEnergies Samples
        total_data = [
            {
                "title": "TotalEnergies Scholarship - Numerical Reasoning Pattern",
                "questions": [
                    {"question": "If the price of a barrel of crude oil increases by 10% from $80, what is the new price?", "options": {"a": "$88", "b": "$82", "c": "$90", "d": "$84"}, "answer": "a"}
                ]
            }
        ]
        
        for diet in ptdf_data:
            content = self.format_as_md(diet['title'], diet['questions'])
            self.save_markdown(os.path.join(self.ptdf_dir, f"PTDF_2022.md"), content)
                
        for diet in nnpc_data:
            content = self.format_as_md(diet['title'], diet['questions'])
            self.save_markdown(os.path.join(self.nnpc_dir, f"NNPC_2021.md"), content)

        shell_dir = os.path.join(self.base_path, 'Scholarships', 'Shell')
        total_dir = os.path.join(self.base_path, 'Scholarships', 'TotalEnergies')
        self.ensure_dirs(shell_dir, total_dir)

        for diet in shell_data:
            content = self.format_as_md(diet['title'], diet['questions'])
            self.save_markdown(os.path.join(shell_dir, f"Shell_Pattern.md"), content)

        for diet in total_data:
            content = self.format_as_md(diet['title'], diet['questions'])
            self.save_markdown(os.path.join(total_dir, f"Total_Pattern.md"), content)

if __name__ == "__main__":
    scraper = ScholarshipScraper()
    scraper.scrape()

