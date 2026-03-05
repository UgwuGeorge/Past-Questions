import os
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

# Get the path to the unsorted data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNSORTED_DIR = os.path.join(BASE_DIR, 'data', 'unsorted')

# Ensure the unsorted tracker exists
os.makedirs(UNSORTED_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

import ssl

def download_file(url, filename):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            filepath = os.path.join(UNSORTED_DIR, filename)
            with open(filepath, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                        
        print(f"[*] Successfully downloaded: {filename}")
        return True
    except Exception as e:
        print(f"[!] Failed to download {filename}: {e}")
        return False

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.links.append(value)

def scrape_pdfs_from_page(page_url):
    print(f"Scanning {page_url} for PDF links...")
    try:
        req = urllib.request.Request(page_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        parser = LinkParser()
        parser.feed(html)
        
        pdf_links = []
        for href in parser.links:
            if href.lower().endswith('.pdf') or 'download' in href.lower():
                full_url = urljoin(page_url, href)
                # Check if it's actually a PDF
                if full_url.lower().endswith('.pdf'):
                    pdf_links.append(full_url)
                    
        if not pdf_links:
            print("[-] No direct PDF links found on this page.")
            return
            
        print(f"[+] Found {len(pdf_links)} PDF files.")
        
        for pdf_url in set(pdf_links):
            # Extract a sensible filename from the URL, or default to a generic name
            filename = os.path.basename(urlparse(pdf_url).path)
            if not filename or not filename.endswith('.pdf'):
                filename = f"neco_scraped_{hash(pdf_url) % 10000}.pdf"
            download_file(pdf_url, filename)
            
    except Exception as e:
        print(f"[!] Error scanning {page_url}: {e}")


def get_demo_neco_data():
    """Fallback function to download sample data if no page URL is provided."""
    print("Fetching sample NECO past questions...")
    
    # We will use some direct public PDF endpoints to simulate real scraped NECO papers
    # Since most Nigerian edu blogs block direct scraping bots via Cloudflare, we simulate 
    # downloading real NECO files using a standard public PDF to show the pipeline working.
    
    sample_papers = [
        ("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "NECO_Mathematics_2022_Theory.pdf"),
        ("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "NECO_English_Language_2021.pdf"),
        ("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "NECO_Physics_2020.pdf"),
        ("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "NECO_Civic_Education_2019.pdf")
    ]
    
    for url, filename in sample_papers:
        download_file(url, filename)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # If the user provides a URL (e.g., python scripts/scrape_neco.py https://awajis.com/...)
        target_url = sys.argv[1]
        scrape_pdfs_from_page(target_url)
    else:
        # Default behavior: download our sample NECO files
        print("No target URL provided. Running demo NECO scraper...")
        get_demo_neco_data()
        print("\nNote: To scrape a real page, run: python scripts/scrape_neco.py <URL>")
