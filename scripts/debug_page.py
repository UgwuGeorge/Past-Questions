import pdfplumber
import sys
import io

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def debug_page(path, page_num):
    with pdfplumber.open(path) as pdf:
        if page_num < len(pdf.pages):
            print(f"--- Page {page_num+1} of {path} ---")
            print(pdf.pages[page_num].extract_text())
        else:
            print(f"Page {page_num+1} not found.")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/Professional/ICAN/Foundation_May_2024.pdf"
    page = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    debug_page(path, page)
