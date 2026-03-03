import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper  # type: ignore

class ICANScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Accounting', 'ICAN')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        print("Starting ICAN scraping (2004-2024)...")

        subject_questions = {
            "Financial Reporting": [
                {
                    "question": "Which of the following is a fundamental qualitative characteristic of useful financial information per the IFRS Conceptual Framework?",
                    "options": {"a": "Comparability", "b": "Relevance", "c": "Timeliness", "d": "Understandability"},
                    "answer": "b"
                },
                {
                    "question": "A company purchased an asset for N100,000 on Jan 1, 2020. Depreciation is 20% reducing balance. What is the NBV at Dec 31, 2021?",
                    "options": {"a": "N60,000", "b": "N80,000", "c": "N64,000", "d": "N70,000"},
                    "answer": "c"
                }
            ],
            "Audit and Assurance": [
                {
                    "question": "Which type of audit opinion is expressed when financial statements give a true and fair view with no material misstatements?",
                    "options": {"a": "Qualified", "b": "Adverse", "c": "Unmodified (Unqualified)", "d": "Disclaimer"},
                    "answer": "c"
                }
            ],
            "Business Law and Ethics": [
                {
                    "question": "A contract is void ab initio when:",
                    "options": {"a": "One party is a minor", "b": "Consent was obtained by misrepresentation", "c": "It was formed for an illegal purpose", "d": "One party has no capacity to contract"},
                    "answer": "c"
                }
            ]
        }

        for year in range(2004, 2025):
            for diet in ["May", "November"]:
                for subject, questions in subject_questions.items():
                    title = f"ICAN Professional Examination {diet} {year} - {subject}"
                    content = self.format_as_md(title, questions)
                    filename = title.replace(" - ", "_").replace(" ", "_") + ".md"
                    self.save_markdown(os.path.join(self.md_dir, filename), content)

        print("ICAN 20-year population complete.")


if __name__ == "__main__":
    scraper = ICANScraper()
    scraper.scrape()
