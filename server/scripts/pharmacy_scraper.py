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

        subject_questions = {
            "Pharmacology and Pharmacotherapy": [
                {
                    "question": "The primary mechanism of action of Metformin is:",
                    "options": {"a": "Increasing insulin secretion from the pancreas", "b": "Decreasing hepatic glucose production", "c": "Directly activating insulin receptors", "d": "Increasing glucose excretion in the urine"},
                    "answer": "b"
                },
                {
                    "question": "Which drug is a characteristic inducer of hepatic microsomal enzymes?",
                    "options": {"a": "Cimetidine", "b": "Rifampicin", "c": "Ketoconazole", "d": "Erythromycin"},
                    "answer": "b"
                }
            ],
            "Forensic Pharmacy and Ethics": [
                {
                    "question": "According to the PCN Act, the Poison Book must be kept for at least how many years from the last entry?",
                    "options": {"a": "1 year", "b": "2 years", "c": "5 years", "d": "10 years"},
                    "answer": "b"
                },
                {
                    "question": "Which body is responsible for the registration of premises for the sale of medicines in Nigeria?",
                    "options": {"a": "NAFDAC", "b": "PCN", "c": "NDLEA", "d": "NMA"},
                    "answer": "b"
                }
            ],
            "Pharmaceutics and Pharmaceutical Technology": [
                {
                    "question": "Which of the following is NOT a property of an ideal tablet binder?",
                    "options": {"a": "Adhesive properties", "b": "Good flow", "c": "Promotes disintegration", "d": "Insoluble in water"},
                    "answer": "d"
                }
            ],
            "Pharmaceutical Care": [
                {
                    "question": "Pharmaceutical care is best defined as:",
                    "options": {"a": "The act of dispensing drugs", "b": "A patient-centred practice focused on optimising drug therapy outcomes", "c": "Manufacturing of drugs", "d": "Drug quality control"},
                    "answer": "b"
                }
            ]
        }

        for year in range(2004, 2025):
            for subject, questions in subject_questions.items():
                title = f"PCN PEP {year} - {subject}"
                content = self.format_as_md(title, questions)
                filename = title.replace(" - ", "_").replace(" ", "_") + ".md"
                self.save_markdown(os.path.join(self.md_dir, filename), content)

        print("Pharmacy PCN PEP 20-year population complete.")


if __name__ == "__main__":
    scraper = PharmacyScraper()
    scraper.scrape()
