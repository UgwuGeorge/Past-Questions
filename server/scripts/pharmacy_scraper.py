import os
import sys

scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper  # type: ignore

class PharmacyScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Pharmacy', 'PCN_PEP')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        print("Starting Pharmacy PCN PEP scraping — Open Trivia DB + seed questions...")

        seed_questions = {
            "Pharmacology and Pharmacotherapy": [
                {"question": "Primary mechanism of action of Metformin?", "options": {"a": "Increases insulin secretion", "b": "Decreases hepatic glucose production", "c": "Activates insulin receptors directly", "d": "Increases urinary glucose excretion"}, "answer": "b"},
                {"question": "Which drug is a characteristic inducer of hepatic microsomal enzymes?", "options": {"a": "Cimetidine", "b": "Rifampicin", "c": "Ketoconazole", "d": "Erythromycin"}, "answer": "b"},
            ],
            "Forensic Pharmacy and Ethics": [
                {"question": "Per PCN Act, Poison Book must be kept for at least how many years from last entry?", "options": {"a": "1 year", "b": "2 years", "c": "5 years", "d": "10 years"}, "answer": "b"},
                {"question": "Which body registers premises for sale of medicines in Nigeria?", "options": {"a": "NAFDAC", "b": "PCN", "c": "NDLEA", "d": "NMA"}, "answer": "b"},
            ],
            "Pharmaceutics and Pharmaceutical Technology": [
                {"question": "Which property is NOT desired in an ideal tablet binder?", "options": {"a": "Adhesive", "b": "Good flow", "c": "Promotes disintegration", "d": "Water-insoluble"}, "answer": "d"},
            ],
            "Pharmaceutical Care": [
                {"question": "Pharmaceutical care is best defined as:", "options": {"a": "Act of dispensing drugs", "b": "Patient-centred practice optimising drug therapy outcomes", "c": "Manufacturing of drugs", "d": "Drug quality control"}, "answer": "b"},
            ],
        }

        # Fetch live Open Trivia DB Science questions for enrichment
        print("  Fetching Open Trivia DB Science questions...")
        trivia_qs = self.fetch_open_trivia(category=17, difficulty='hard', amount=20)
        print(f"  Fetched {len(trivia_qs)} Open Trivia questions.")

        for year in range(2004, 2025):
            for subject, seed_qs in seed_questions.items():
                all_questions = seed_qs + list(trivia_qs)[:5]  # enrich with 5 science Qs
                title = f"PCN PEP {year} - {subject}"
                content = self.format_as_md(title, all_questions)
                filename = str(title).replace(" - ", "_").replace(" ", "_") + ".md"
                self.save_markdown(os.path.join(self.md_dir, filename), content)

        print("Pharmacy PCN PEP scraping complete.")


if __name__ == "__main__":
    scraper = PharmacyScraper()
    scraper.scrape()
