import os
import sys
import requests
from bs4 import BeautifulSoup
import time
import re

# Add project root to sys.path
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import formatters from existing scraper if possible, or just reimplement
def format_as_md(title, questions):
    md = [f"# {title}\n", "## Objectives\n"]
    for i, q in enumerate(questions, 1):
        md.append(f"**{i}.** {q.get('question', '')}")
        options = q.get('options', {})
        for label in ['a', 'b', 'c', 'd', 'e']:
            if label in options:
                md.append(f"   {label.upper()}) {options[label]}")
        md.append(f"   **Answer: {q.get('answer', '').upper()}**")
        if q.get('explanation'):
            md.append(f"   *Explanation: {q['explanation']}*")
        md.append("")
    md.append("\n---\n*(Source: MySchool.ng via Web Scraper)*")
    return "\n".join(md)

def parse_question_text(text):
    # Split by typical option markers A. B. C. etc.
    parts = re.split(r'\n([A-E])\.\s+', text)
    q_text = parts[0].strip()
    options = {}
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            label = parts[i].lower()
            content = parts[i+1].split('\n')[0].strip()
            options[label] = content
    return {'question': q_text, 'options': options}

def scrape_answer_page(url, headers):
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            ans_text = soup.select_one('.text-success')
            explanation = ""
            answer_key = 'a'
            if ans_text:
                match = re.search(r'Option ([A-E])', ans_text.get_text())
                if match:
                    answer_key = match.group(1).lower()
            exp_header = soup.find(re.compile(r'h[3-5]'), string=re.compile(r'Explanation', re.I))
            if exp_header:
                exp_div = exp_header.find_next('div')
                if exp_div:
                    explanation = exp_div.get_text(strip=True)
            return {'answer': answer_key, 'explanation': explanation}
    except:
        pass
    return {'answer': 'a', 'explanation': ''}

def run_neco_web_scrape(subject, limit=50):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    subject_map = {
        'english': 'english-language',
        'mathematics': 'mathematics'
    }
    
    subject_stub = subject_map.get(subject.lower(), subject.lower())
    # Note: MySchool URLs for specific years might vary, but classroom/subject often shows recent ones
    # We'll try to scrape the main list. 
    url = f"https://myschool.ng/classroom/{subject_stub}?exam_type=neco"
    print(f"Scraping NECO {subject} from {url}...")
    
    questions = []
    seen_texts = set()
    
    try:
        # Initial page
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"Failed to load page: {resp.status_code}")
            return
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # In a real scenario, we might need to handle pagination to get 50
        # For now we'll get what's on the first few pages if possible
        
        # Loop through pages if needed, but for the demo we'll just show the logic
        page = 1
        while len(questions) < limit and page <= 5:
            current_url = f"{url}&page={page}"
            print(f"  Page {page}...")
            resp = requests.get(current_url, headers=headers, timeout=15)
            if resp.status_code != 200: break
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.media')
            if not items: break
            
            for item in items:
                if len(questions) >= limit: break
                media_body = item.select_one('.media-body')
                if not media_body: continue
                
                full_text = media_body.get_text(separator='\n', strip=True)
                q_data = parse_question_text(full_text)
                
                if q_data['question'] in seen_texts: continue
                seen_texts.add(q_data['question'])
                
                discuss_link = media_body.find('a', string=re.compile(r'View Answer', re.I))
                if discuss_link and discuss_link.get('href'):
                    ans_url = discuss_link['href']
                    if not ans_url.startswith('http'):
                        ans_url = "https://myschool.ng" + ans_url
                    ans_info = scrape_answer_page(ans_url, headers)
                    q_data.update(ans_info)
                
                questions.append(q_data)
                time.sleep(1)
            
            page += 1
            
        if questions:
            title = f"NECO {subject.title()} 2023 (Web Scraped)"
            md_content = format_as_md(title, questions)
            
            # Save path
            folder_name = "Mathematics" if subject.lower() == "mathematics" else "English"
            full_folder = os.path.join(project_root, 'data', 'Academic', 'Secondary', 'NECO', 'Core')
            os.makedirs(full_folder, exist_ok=True)
            
            filename = f"NECO_{folder_name}_2023_Web.md"
            filepath = os.path.join(full_folder, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"  Saved {len(questions)} questions to {filepath}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    for sub in ['english', 'mathematics']:
        run_neco_web_scrape(sub, limit=20) # Lower limit for faster demo
