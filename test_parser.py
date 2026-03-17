import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_core.scripts.import_data import parse_markdown_file

file_path = "data/Professional/Law/Bar_Finals/Bar_Finals_2024_Civil_Litigation.md"
data = parse_markdown_file(file_path)

if data:
    print(f"Parsed {len(data['questions'])} questions.")
else:
    print("Failed to parse.")
