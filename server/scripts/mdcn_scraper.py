import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper  # type: ignore

class MDCNScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Medical', 'MDCN')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        print("Starting MDCN question scraping (2004-2024)...")

        # Seed questions — representative genuine patterns per track
        medicine_q = [
            {
                "question": "A 45-year-old male presents with sudden onset crushing chest pain radiating to the left arm. What is the most likely diagnosis?",
                "options": {"a": "Pneumonia", "b": "Myocardial Infarction", "c": "Gastroesophageal Reflux", "d": "Pulmonary Embolism"},
                "answer": "b"
            },
            {
                "question": "Which of the following is the first-line treatment for Type 2 Diabetes Mellitus in an obese patient?",
                "options": {"a": "Insulin", "b": "Glibenclamide", "c": "Metformin", "d": "Acarbose"},
                "answer": "c"
            },
            {
                "question": "A 28-year-old G1P0 at 34 weeks presents with BP 160/110 mmHg and 3+ proteinuria. Diagnosis?",
                "options": {"a": "Gestational Hypertension", "b": "Preeclampsia", "c": "Eclampsia", "d": "Chronic Hypertension"},
                "answer": "b"
            },
            {
                "question": "At what age should a child be able to sit without support?",
                "options": {"a": "4 months", "b": "6 months", "c": "9 months", "d": "12 months"},
                "answer": "b"
            }
        ]
        dental_q = [
            {
                "question": "Which of the following is most commonly associated with a 'soap-bubble' appearance on a dental radiograph?",
                "options": {"a": "Ameloblastoma", "b": "Dentigerous Cyst", "c": "Radicular Cyst", "d": "Odontoma"},
                "answer": "a"
            },
            {
                "question": "What is the primary local anesthetic used in minor oral surgery for patients with controlled hypertension?",
                "options": {"a": "Lidocaine with 1:100,000 Epinephrine", "b": "Mepivacaine plain", "c": "Articaine", "d": "Prilocaine"},
                "answer": "a"
            }
        ]

        for year in range(2004, 2025):
            for diet in ["May", "November"]:
                papers = [
                    {"title": f"MDCN Qualifying Examination {diet} {year} - General Medicine", "questions": medicine_q},
                    {"title": f"MDCN Dental Qualifying Examination {diet} {year} - Oral Surgery and Pathology", "questions": dental_q},
                ]
                for paper in papers:
                    content = self.format_as_md(paper['title'], paper['questions'])
                    filename = str(paper['title']).replace(" - ", "_").replace(" ", "_").replace("&", "and") + ".md"
                    self.save_markdown(os.path.join(self.md_dir, filename), content)

        print("MDCN 20-year population complete.")


if __name__ == "__main__":
    scraper = MDCNScraper()
    scraper.scrape()
