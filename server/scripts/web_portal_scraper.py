import os
import sys
import requests
from bs4 import BeautifulSoup
import time
import json
import re

scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from base_scraper import BaseScraper

class WebPortalScraper(BaseScraper):
    """
    Scrapes academic past questions from education portals like MySchool.ng
    """

    def __init__(self):
        super().__init__()
        self.academic_dir = os.path.join(self.base_path, 'Academic')
        self.subject_map = {
            'english': 'english-language',
            'mathematics': 'mathematics',
            'physics': 'physics',
            'chemistry': 'chemistry',
            'biology': 'biology',
            'economics': 'economics',
            'government': 'government'
        }

    def scrape_myschool_subject(self, subject, exam_type='jamb', limit=10):
        """
        Scrapes questions for a given subject from MySchool.ng
        """
        subject_stub = self.subject_map.get(subject.lower(), subject.lower())
        url = f"https://myschool.ng/classroom/{subject_stub}?exam_type={exam_type}"
        print(f"Scraping {subject} ({exam_type}) from {url}...")
        
        questions = []
        try:
            resp = requests.get(url, headers=self.headers, timeout=15)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                question_items = soup.select('.media')[:limit]
                
                for item in question_items:
                    media_body = item.select_one('.media-body')
                    if not media_body: continue
                    
                    # Extract question text and options
                    full_text = media_body.get_text(separator='\n', strip=True)
                    
                    # MySchool often lists options within the same block
                    # We'll try to parse them out
                    q_data = self.parse_question_text(full_text)
                    
                    # Get Answer and Explanation from discussion page
                    discuss_link = media_body.find('a', string=re.compile(r'View Answer', re.I))
                    if discuss_link and discuss_link.get('href'):
                        ans_url = discuss_link['href']
                        if not ans_url.startswith('http'):
                            ans_url = "https://myschool.ng" + ans_url
                        
                        ans_data = self.scrape_answer_page(ans_url)
                        q_data.update(ans_data)
                    
                    if q_data.get('question'):
                        questions.append(q_data)
                    
                    time.sleep(1) # Be nice
                
                return questions
        except Exception as e:
            print(f"  [Scrape Error] {url}: {e}")
        return []

    def parse_question_text(self, text):
        """Helper to split question and options."""
        # Split by typical option markers A. B. C. etc.
        parts = re.split(r'\n([A-E])\.\s+', text)
        q_text = parts[0].strip()
        options = {}
        
        if len(parts) > 1:
            for i in range(1, len(parts), 2):
                label = parts[i].lower()
                content = parts[i+1].split('\n')[0].strip()
                options[label] = content
        
        return {
            'question': q_text,
            'options': options
        }

    def scrape_answer_page(self, url):
        """Scrapes the correct answer and explanation."""
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                ans_text = soup.select_one('.text-success')
                explanation = ""
                
                answer_key = 'a'
                if ans_text:
                    match = re.search(r'Option ([A-E])', ans_text.get_text())
                    if match:
                        answer_key = match.group(1).lower()
                
                # Try to find explanation
                exp_header = soup.find(re.compile(r'h[3-5]'), string=re.compile(r'Explanation', re.I))
                if exp_header:
                    explanation = exp_header.find_next('div').get_text(strip=True)
                
                return {
                    'answer': answer_key,
                    'explanation': explanation
                }
        except:
            pass
        return {'answer': 'a', 'explanation': ''}

    def run_academic_scrape(self):
        """Runs the scraper for main JAMB subjects."""
        subjects = ['English', 'Mathematics', 'Biology', 'Chemistry', 'Physics']
        for sub in subjects:
            questions = self.scrape_myschool_subject(sub, 'jamb', limit=5)
            if questions:
                md_content = self.format_as_md(f"JAMB {sub} - Scraped Data", questions)
                # Saving to a general 2024 folder as a start
                save_path = os.path.join(self.academic_dir, 'JAMB', sub, '2024.md')
                self.save_markdown(save_path, md_content)

    def generate_full_structure(self):
        """Ensures all folders exist for the target categories."""
        categories = {
            'Academic': {
                'JAMB': ['English', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Economics', 'Government'],
                'WAEC': ['English', 'Mathematics', 'Physics', 'Chemistry', 'Biology'],
                'NECO': ['English', 'Mathematics'],
                'Post-UTME': ['UNILAG', 'UI', 'UNN', 'OAU']
            },
            'Professional': {
                'ICAN': ['Skills', 'Professional'],
                'Law': ['Civil', 'Criminal', 'Corporate'],
                'TRCN': ['General'],
                'COREN': ['General']
            }
        }
        
        for cat, subcats in categories.items():
            for subcat, subjects in subcats.items():
                for subject in subjects:
                    path = os.path.join(self.base_path, cat, subcat, subject)
                    os.makedirs(path, exist_ok=True)
        print(f"Directory structure ready in {self.base_path}")

if __name__ == "__main__":
    scraper = WebPortalScraper()
    scraper.generate_full_structure()
    scraper.run_academic_scrape()
