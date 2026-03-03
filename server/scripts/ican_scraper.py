import os
import sys

# Add scripts directory to sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class ICANScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.raw_dir = os.path.join(self.base_path, 'data', 'raw', 'ICAN')
        self.md_dir = os.path.join(self.base_path, 'Professional', 'Accounting', 'ICAN')

    def scrape(self):
        self.ensure_dirs(self.raw_dir, self.md_dir)
        
        years = range(2011, 2024)
        sections = ["Foundation", "Skills", "Professional"]
        diets = ["May", "November"]
        
        print(f"Starting ICAN Pathfinder discovery for years {years.start}-{years.stop-1}...")
        
        targets = []
        for year in years:
            for diet in diets:
                for section in sections:
                    targets.append(f"https://icanig.org/documents/{section.upper()}_{diet.upper()}_{year}_PATHFINDER.pdf")
        
        targets.extend([
            "https://icanig.org/documents/SKILLS_NOVEMBER_2015_PATHFINDER.pdf",
            "https://icanig.org/documents/PROFESSIONAL_MAY_2016_PATHFINDER.pdf",
            "https://icanig.org/documents/FOUNDATION_NOVEMBER_2017_PATHFINDER.pdf"
        ])
        
        for url in targets:
            self.download_file(url, self.raw_dir)

if __name__ == "__main__":
    scraper = ICANScraper()
    scraper.scrape()

