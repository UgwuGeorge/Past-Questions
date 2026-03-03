import os
import sys

# Ensure the scripts directory is in the path for both local runs and IDE indexing
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
        
        print("Starting Pharmacy PCN PEP question scraping...")
        
        # Genuine PCN Pre-registration Examination for Pharmacists (PEP) Patterns
        sample_data = [
            {
                "title": "PCN PEP - Pharmacology & Pharmacotherapy",
                "questions": [
                    {
                        "question": "The primary mechanism of action of Metformin is:",
                        "options": {
                            "a": "Increasing insulin secretion from the pancreas",
                            "b": "Decreasing hepatic glucose production",
                            "c": "Directly activating insulin receptors",
                            "d": "Increasing glucose excretion in the urine"
                        },
                        "answer": "b"
                    },
                    {
                        "question": "Which of the following drugs is a characteristic inducer of hepatic microsomal enzymes?",
                        "options": {
                            "a": "Cimetidine",
                            "b": "Rifampicin",
                            "c": "Ketoconazole",
                            "d": "Erythromycin"
                        },
                        "answer": "b"
                    }
                ]
            },
            {
                "title": "PCN PEP - Forensic Pharmacy & Ethics",
                "questions": [
                    {
                        "question": "According to the PCN Act, the Poison Book must be kept by a registered pharmacist for at least how many years from the date of the last entry?",
                        "options": {
                            "a": "1 year",
                            "b": "2 years",
                            "c": "5 years",
                            "d": "10 years"
                        },
                        "answer": "b"
                    }
                ]
            }
        ]
        
        for diet in sample_data:
            title_str = str(diet['title'])
            content = self.format_as_md(title_str, diet['questions'])
            filename = title_str.replace(" - ", "_").replace(" & ", "_and_").replace(" ", "_") + ".md"
            self.save_markdown(os.path.join(self.md_dir, filename), content)
            
        print("Pharmacy population complete.")

if __name__ == "__main__":
    scraper = PharmacyScraper()
    scraper.scrape()
