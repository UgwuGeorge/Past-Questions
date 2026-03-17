from pypdf import PdfReader
import json

reader = PdfReader("tmp/ican_atswa.pdf")
text = ""
for i, page in enumerate(reader.pages):
    text += page.extract_text()

with open("tmp/ican_atswa_raw.txt", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Extracted {len(text)} characters.")
