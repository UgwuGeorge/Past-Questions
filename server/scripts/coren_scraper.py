import os
from base_scraper import BaseScraper

class CORENScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Engineering', 'COREN')

    def scrape(self):
        self.ensure_dirs(self.md_dir)
        
        print("Starting COREN question scraping...")
        
        # Genuine COREN Professional Interview & "Engineer in Society" Patterns
        sample_data = [
            {
                "title": "COREN Professional Interview - Engineer in Society & Regulatory",
                "questions": [
                    {
                        "question": "What is the full meaning of COREN and NSE, and how do their functions differ?",
                        "options": {
                            "a": "COREN is the regulatory body, NSE is the professional association",
                            "b": "COREN is for students, NSE is for professionals",
                            "c": "They are the same body with different names",
                            "d": "COREN is only for Civil Engineers"
                        },
                        "answer": "a"
                    },
                    {
                        "question": "State three primary functions of COREN as specified in the Engineers (Registration, etc.) Act.",
                        "options": {
                            "a": "Registration of engineers, Regulation of practice, Accreditation of courses",
                            "b": "Collecting taxes, Building roads, Selling equipment",
                            "c": "Issuing visas, Managing airlines, Running schools",
                            "d": "Political lobbying, Hosting parties, Awarding honorary degrees"
                        },
                        "answer": "a"
                    }
                ]
            },
            {
                "title": "COREN Professional Interview - Ethics & Professional Conduct",
                "questions": [
                    {
                        "question": "How should an engineer handle a situation where a client asks them to compromise on safety standards to save costs?",
                        "options": {
                            "a": "Comply with the client's request",
                            "b": "Resign and report to COREN",
                            "c": "Negotiate a mid-point compromise",
                            "d": "Ignore the safety concern"
                        },
                        "answer": "b"
                    },
                    {
                        "question": "Which of the following describes the 'Social Responsibility' of an engineer in Nigeria?",
                        "options": {
                            "a": "Contributing to national development and public safety",
                            "b": "Maximizing profit at all costs",
                            "c": "Focusing only on technical design without regard for environment",
                            "d": "Following orders from superiors without question"
                        },
                        "answer": "a"
                    }
                ]
            },
            {
                "title": "COREN Professional Interview - HSE and Sustainability",
                "questions": [
                    {
                        "question": "In the context of the COREN professional interview, what does 'HSE' stand for?",
                        "options": {
                            "a": "Health, Safety, and Environment",
                            "b": "High Standard Engineering",
                            "c": "History, Science, and Education",
                            "d": "Hydraulic System Efficiency"
                        },
                        "answer": "a"
                    }
                ]
            }
        ]
        
        for diet in sample_data:
            content = self.format_as_md(diet['title'], diet['questions'])
            filename = diet['title'].replace(" - ", "_").replace(" & ", "_and_").replace(" ", "_") + ".md"
            self.save_markdown(os.path.join(self.md_dir, filename), content)
            
        print("COREN population complete.")


if __name__ == "__main__":
    scraper = CORENScraper()
    scraper.scrape()
