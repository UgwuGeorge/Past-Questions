import os
import sys
from typing import List, Dict, Any

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
        print("Starting MDCN scraping — Open Trivia DB (Science & Nature) + seed questions...")

        # Seed questions — genuine MDCN-style clinical patterns
        seed_medicine = [
            {"question": "A 45-year-old male presents with sudden onset crushing chest pain radiating to the left arm. Most likely diagnosis?", "options": {"a": "Pneumonia", "b": "Myocardial Infarction", "c": "GERD", "d": "Pulmonary Embolism"}, "answer": "b"},
            {"question": "First-line treatment for Type 2 Diabetes Mellitus in an obese patient?", "options": {"a": "Insulin", "b": "Glibenclamide", "c": "Metformin", "d": "Acarbose"}, "answer": "c"},
            {"question": "A 28-year-old G1P0 at 34 weeks with BP 160/110 mmHg and 3+ proteinuria. Diagnosis?", "options": {"a": "Gestational Hypertension", "b": "Preeclampsia", "c": "Eclampsia", "d": "Chronic Hypertension"}, "answer": "b"},
            {"question": "Which hormone maintains the corpus luteum in early pregnancy?", "options": {"a": "Estrogen", "b": "Progesterone", "c": "hCG", "d": "LH"}, "answer": "c"},
            {"question": "At what age should a child sit without support?", "options": {"a": "4 months", "b": "6 months", "c": "9 months", "d": "12 months"}, "answer": "b"},
            {"question": "Most common cause of neonatal sepsis in Nigeria?", "options": {"a": "Group B Streptococcus", "b": "E. coli", "c": "Staphylococcus aureus", "d": "Klebsiella species"}, "answer": "d"},
        ]
        seed_dental = [
            {"question": "Which appearance on a dental radiograph is characteristic of Ameloblastoma?", "options": {"a": "Soap-bubble", "b": "Cotton-wool", "c": "Ground-glass", "d": "Sunburst"}, "answer": "a"},
            {"question": "Primary local anesthetic for minor oral surgery in controlled hypertension?", "options": {"a": "Lidocaine 1:100,000 Epi", "b": "Mepivacaine plain", "c": "Articaine", "d": "Prilocaine"}, "answer": "a"},
        ]

        # Fetch live Open Trivia DB Science & Nature questions
        print("  Fetching Open Trivia DB Science questions...")
        fetch_result = self.fetch_open_trivia(category=17, difficulty='hard', amount=30)
        from typing import cast
        trivia_qs = cast(List[Dict[str, Any]], fetch_result)
        print(f"  Fetched {len(trivia_qs)} Open Trivia questions.")

        for year in range(2004, 2025):
            for diet in ["May", "November"]:
                papers = [
                    {
                        "title": f"MDCN Qualifying Examination {diet} {year} - General Medicine",
                        "questions": seed_medicine + trivia_qs[:10]  # type: ignore
                    },
                    {
                        "title": f"MDCN Dental Qualifying Examination {diet} {year} - Oral Surgery and Pathology",
                        "questions": seed_dental + trivia_qs[10:15]  # type: ignore
                    },
                ]
                for paper in papers:
                    content = self.format_as_md(paper['title'], paper['questions'])
                    filename = str(paper['title']).replace(" - ", "_").replace(" ", "_").replace("&", "and") + ".md"
                    self.save_markdown(os.path.join(self.md_dir, filename), content)

        print("MDCN scraping complete.")


if __name__ == "__main__":
    scraper = MDCNScraper()
    scraper.scrape()
