"""
Download ICAN Pathfinder PDFs using requests with proper session/headers.
"""
import requests
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tmp', 'ican_pdfs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
})

# Try multiple known pathfinder URLs from icanig.org
URLS = [
    # Nov 2024 Foundation
    ("nov2024_foundation.pdf", "https://icanig.org/ican/wp-content/uploads/2025/01/NOVEMBER-2024-FOUNDATION-LEVEL-PATHFINDER.pdf"),
    ("nov2024_foundation2.pdf", "https://icanig.org/ican/wp-content/uploads/2025/02/NOVEMBER-2024-FOUNDATION-LEVEL-PATHFINDER.pdf"),
    # May 2024 Foundation  
    ("may2024_foundation.pdf", "https://icanig.org/ican/wp-content/uploads/2024/08/MAY-2024-FOUNDATION-LEVEL-PATHFINDER.pdf"),
    # Nov 2023 Foundation
    ("nov2023_foundation.pdf", "https://icanig.org/ican/wp-content/uploads/2024/02/NOVEMBER-2023-FOUNDATION-LEVEL-PATHFINDER.pdf"),
    # Try the new site structure
    ("nov2024_found_v2.pdf", "https://icanig.org/ican/download/pathfinder/november-2024-foundation/"),
    # Try direct document paths
    ("may2024_skills.pdf", "https://icanig.org/ican/wp-content/uploads/2024/08/MAY-2024-SKILLS-LEVEL-PATHFINDER.pdf"),
    ("nov2024_skills.pdf", "https://icanig.org/ican/wp-content/uploads/2025/01/NOVEMBER-2024-SKILLS-LEVEL-PATHFINDER.pdf"),
    ("nov2024_professional.pdf", "https://icanig.org/ican/wp-content/uploads/2025/01/NOVEMBER-2024-PROFESSIONAL-LEVEL-PATHFINDER.pdf"),
]

for filename, url in URLS:
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        # First visit the main page to get cookies
        session.get("https://icanig.org/ican/", timeout=10)
        
        resp = session.get(url, timeout=30, allow_redirects=True)
        content_type = resp.headers.get('Content-Type', '')
        
        if 'pdf' in content_type.lower() or resp.content[:4] == b'%PDF':
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            print(f"[OK] {filename} - {len(resp.content)} bytes ({content_type})")
        else:
            print(f"[--] {filename} - Not PDF. Status={resp.status_code}, Type={content_type}, First bytes={resp.content[:30]}")
    except Exception as e:
        print(f"[ERR] {filename} - {e}")

# Also try alternative sources
ALT_URLS = [
    ("funai_atswa.pdf", "https://library.funai.edu.ng/wp-content/uploads/2021/05/ATSWA-Study-Text-Accounting.pdf"),
    ("icagh_atswa.pdf", "https://www.icagh.org/files/ATSWA-Past-Questions.pdf"),
]

for filename, url in ALT_URLS:
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        resp = session.get(url, timeout=30, allow_redirects=True)
        content_type = resp.headers.get('Content-Type', '')
        if 'pdf' in content_type.lower() or resp.content[:4] == b'%PDF':
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            print(f"[OK] {filename} - {len(resp.content)} bytes")
        else:
            print(f"[--] {filename} - Not PDF. Status={resp.status_code}, Type={content_type}")
    except Exception as e:
        print(f"[ERR] {filename} - {e}")
