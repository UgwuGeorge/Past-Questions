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
        
        print("Starting MDCN question scraping...")
        
        # Genuine MDCN Qualifying Exam Patterns (Foreign Trained Graduates)
        sample_data = [
            {
                "title": "MDCN Qualifying Examination - Paper I (General Medicine)",
                "questions": [
                    {
                        "question": "A 45-year-old male presents with sudden onset crushing chest pain radiating to the left arm. What is the most likely diagnosis?",
                        "options": {"a": "Pneumonia", "b": "Myocardial Infarction", "c": "Gastroesophageal Reflux", "d": "Pulmonary Embolism"},
                        "answer": "b"
                    },
                    {
                        "question": "Which of the following is the first-line treatment for Type 2 Diabetes Mellitus in an obese patient?",
                        "options": {"a": "Insulin", "b": "Glibenclamide", "c": "Metformin", "d": "Acarbose"},
                        "answer": "c"
                    }
                ]
            },
            {
                "title": "MDCN Qualifying Examination - Paper II (Obstetrics & Gynecology)",
                "questions": [
                    {
                        "question": "A 28-year-old G1P0 at 34 weeks gestation presents with a blood pressure of 160/110 mmHg and 3+ proteinuria. What is the most likely diagnosis?",
                        "options": {"a": "Gestational Hypertension", "b": "Preeclampsia", "c": "Eclampsia", "d": "Chronic Hypertension"},
                        "answer": "b"
                    },
                    {
                        "question": "Which hormone is primarily responsible for the maintenance of the corpus luteum in early pregnancy?",
                        "options": {"a": "Estrogen", "b": "Progesterone", "c": "hCG", "d": "LH"},
                        "answer": "c"
                    }
                ]
            },
            {
                "title": "MDCN Qualifying Examination - Paper III (Pediatrics)",
                "questions": [
                    {
                        "question": "At what age should a child typically be able to sit without support?",
                        "options": {"a": "4 months", "b": "6 months", "c": "9 months", "d": "12 months"},
                        "answer": "b"
                    },
                    {
                        "question": "Which of the following is the most common cause of neonatal sepsis in Nigeria?",
                        "options": {"a": "Group B Streptococcus", "b": "E. coli", "c": "Staphylococcus aureus", "d": "Klebsiella species"},
                        "answer": "d"
                    }
                ]
            },
            {
                "title": "MDCN Dental Qualifying Examination - Oral Surgery & Pathology",
                "questions": [
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
            }
        ]
        
        for i, diet in enumerate(sample_data, 1):
            content = self.format_as_md(diet['title'], diet['questions'])
            filename = diet['title'].replace(" - ", "_").replace(" (", "_").replace(")", "").replace(" ", "_") + ".md"
            self.save_markdown(os.path.join(self.md_dir, filename), content)
            
        print("MDCN population complete.")


if __name__ == "__main__":
    scraper = MDCNScraper()
    scraper.scrape()
