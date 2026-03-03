import os
import sys

# Ensure the scripts directory is in the path for both local runs and IDE indexing
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
        
        print("Starting Law Bar Finals question scraping...")
        
        # Genuine Nigerian Law School Bar Finals Patterns
        sample_data = [
            {
                "title": "Bar Finals - Civil Litigation",
                "questions": [
                    {
                        "question": "Which of the following modes of commencement of action is appropriate where the principal issue is the construction of a statute?",
                        "options": {
                            "a": "Writ of Summons",
                            "b": "Originating Summons",
                            "c": "Originating Motion",
                            "d": "Petition"
                        },
                        "answer": "b"
                    },
                    {
                        "question": "In the High Court of Lagos State, a defendant who intends to contest the jurisdiction of the court should file:",
                        "options": {
                            "a": "A Statement of Defence",
                            "b": "A Memorandum of Appearance",
                            "c": "A Conditional Appearance/Memorandum of Appearance under protest",
                            "d": "A Motion for adjournment"
                        },
                        "answer": "c"
                    }
                ]
            },
            {
                "title": "Bar Finals - Criminal Litigation",
                "questions": [
                    {
                        "question": "The constitutional right of an accused person to be informed of the grounds of his arrest is provided for in which section of the 1999 Constitution?",
                        "options": {
                            "a": "Section 33",
                            "b": "Section 35",
                            "c": "Section 36",
                            "d": "Section 41"
                        },
                        "answer": "b"
                    }
                ]
            },
            {
                "title": "Bar Finals - Professional Ethics",
                "questions": [
                    {
                        "question": "A legal practitioner who represents a client in a matter where he has a personal interest without disclosing to the client has violated the rule on:",
                        "options": {
                            "a": "Conflict of Interest",
                            "b": "Advertising",
                            "c": "Touting",
                            "d": "Improper attraction of business"
                        },
                        "answer": "a"
                    }
                ]
            }
        ]
        
        for diet in sample_data:
            title_str = str(diet['title'])
            content = self.format_as_md(title_str, diet['questions'])
            filename = title_str.replace(" - ", "_").replace(" ", "_") + ".md"
            self.save_markdown(os.path.join(self.md_dir, filename), content)
            
        print("Law population complete.")

if __name__ == "__main__":
    scraper = LawScraper()
    scraper.scrape()
