import pdfplumber
import sys
import io

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def debug_pdf(path, num_pages=5):
    print(f"--- Debugging {path} ---")
    with pdfplumber.open(path) as pdf:
        for i in range(min(num_pages, len(pdf.pages))):
            print(f"--- PAGE {i+1} ---")
            print(pdf.pages[i].extract_text())
            print("\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_pdf(sys.argv[1], 20)
    else:
        debug_pdf("data/Professional/ICAN/Skills_May_2024.pdf", 20)
