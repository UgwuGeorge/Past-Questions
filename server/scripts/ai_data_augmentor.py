import os
import sys
import json
import time

# Ensure we can import from agent_core
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agent_core.core.ai import AIEngine
from server.scripts.base_scraper import BaseScraper

class AIDataAugmentor(BaseScraper):
    """
    Uses OpenAI to generate or refine past questions for subjects with missing data.
    """

    def __init__(self):
        super().__init__()
        self.academic_dir = os.path.join(self.base_path, 'Academic')

    def augment_subject(self, category, subcategory, subject, years=range(2010, 2024)):
        """
        Generates questions for a list of years for a specific subject if they don't exist.
        """
        print(f"Augmenting {category}/{subcategory}/{subject}...")
        
        for year in years:
            folder_path = os.path.join(self.academic_dir, subcategory, subject)
            file_path = os.path.join(folder_path, f"{year}.md")
            
            if os.path.exists(file_path):
                # Check if it's a placeholder
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "Sample" not in content and len(content) > 200:
                        print(f"  [Skipped] {year} already has data.")
                        continue
            
            print(f"  [Generating] {year} questions via AI...")
            try:
                # Generate 15 high-quality questions per year
                questions = AIEngine.generate_questions_sync(
                    exam_type=f"{subcategory} {subject}",
                    topic=f"Comprehensive {subject} syllabus for {year} {subcategory} exam",
                    difficulty="hard",
                    count=15
                )
                
                if questions:
                    # Convert to our standard format if needed
                    formatted_qs = []
                    for q in questions:
                        formatted_qs.append({
                            'question': q.get('text', ''),
                            'options': {c['text'][0].lower() if 'text' in c else 'a': c.get('text', '') for c in q.get('choices', [])},
                            'answer': next((chr(97 + i) for i, c in enumerate(q.get('choices', [])) if c.get('is_correct')), 'a')
                        })
                    
                    md_content = self.format_as_md(f"{subcategory} {subject} Past Questions - {year}", formatted_qs)
                    self.save_markdown(file_path, md_content)
                    print(f"  [Success] Saved {year}.md")
                
                time.sleep(2) # Avoid rate limits
            except Exception as e:
                print(f"  [AI Error] {year}: {e}")

    def run_priority_augmentation(self):
        """Augments core JAMB and WAEC subjects."""
        priority_targets = [
            ('Academic', 'JAMB', 'Economics'),
            ('Academic', 'JAMB', 'Government'),
            ('Academic', 'WAEC', 'Biology'),
        ]
        
        for cat, sub, sub_name in priority_targets:
            self.augment_subject(cat, sub, sub_name, years=[2020, 2021, 2022, 2023])

if __name__ == "__main__":
    augmentor = AIDataAugmentor()
    augmentor.run_priority_augmentation()
