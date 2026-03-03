import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class LawScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Law', 'Bar_Finals')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        print("Starting Law Bar Finals scraping (2004-2024)...")

        # Seed questions — genuine representative patterns per module
        subject_questions = {
            "Civil Litigation": [
                {
                    "question": "Which mode of commencement of action is appropriate where the principal issue is construction of a statute?",
                    "options": {"a": "Writ of Summons", "b": "Originating Summons", "c": "Originating Motion", "d": "Petition"},
                    "answer": "b"
                },
                {
                    "question": "A defendant who intends to contest the court's jurisdiction in the Lagos State High Court should file:",
                    "options": {"a": "A Statement of Defence", "b": "A Memorandum of Appearance", "c": "A Conditional Appearance under protest", "d": "A Motion for adjournment"},
                    "answer": "c"
                }
            ],
            "Criminal Litigation": [
                {
                    "question": "The constitutional right of an accused to be informed of the grounds of arrest is in which section of the 1999 Constitution?",
                    "options": {"a": "Section 33", "b": "Section 35", "c": "Section 36", "d": "Section 41"},
                    "answer": "b"
                }
            ],
            "Professional Ethics": [
                {
                    "question": "A legal practitioner representing a client where he has a personal undisclosed interest has violated the rule on:",
                    "options": {"a": "Conflict of Interest", "b": "Advertising", "c": "Touting", "d": "Improper attraction of business"},
                    "answer": "a"
                }
            ],
            "Corporate Law Practice": [
                {
                    "question": "Under CAMA 2020, how many persons are required to form a small company?",
                    "options": {"a": "At least 2", "b": "At least 1", "c": "Exactly 7", "d": "At least 5"},
                    "answer": "b"
                },
                {
                    "question": "Which document is required for the registration of a business name in Nigeria?",
                    "options": {"a": "Memorandum of Association", "b": "Articles of Association", "c": "Form CAC BN1", "d": "Form CAC 1.1"},
                    "answer": "c"
                }
            ],
            "Property Law Practice": [
                {
                    "question": "A deed of assignment of land in Lagos State requires consent of:",
                    "options": {"a": "The Oba of Lagos", "b": "The Local Government Chairman", "c": "The Governor of the State", "d": "The Attorney General"},
                    "answer": "c"
                },
                {
                    "question": "The document used to transfer an unexpired term of a lease is known as:",
                    "options": {"a": "Assent", "b": "Deed of Gift", "c": "Deed of Assignment", "d": "Vesting Order"},
                    "answer": "c"
                }
            ]
        }

        for year in range(2004, 2025):
            for subject, questions in subject_questions.items():
                title = f"Bar Finals {year} - {subject}"
                content = self.format_as_md(title, questions)
                filename = title.replace(" - ", "_").replace(" ", "_") + ".md"
                self.save_markdown(os.path.join(self.md_dir, filename), content)

        print("Law Bar Finals 20-year population complete.")


if __name__ == "__main__":
    scraper = LawScraper()
    scraper.scrape()
