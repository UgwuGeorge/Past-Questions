import os
import shutil
import re
from pathlib import Path

def get_project_root():
    # Assuming this script is in Past-Questions/scripts/
    return Path(__file__).resolve().parent.parent

def sort_files():
    root = get_project_root()
    unsorted_dir = root / 'data' / 'unsorted'
    data_dir = root / 'data'
    
    # Ensure unsorted directory exists
    unsorted_dir.mkdir(parents=True, exist_ok=True)
    
    # Basic keyword mapping to determine the destination folder
    # You can expand these keywords as needed based on your scraped data names
    sort_rules = {
        'waec': data_dir / 'Academic' / 'Secondary',
        'jamb': data_dir / 'Academic' / 'Secondary',
        'neco': data_dir / 'Academic' / 'Secondary',
        'university': data_dir / 'Academic' / 'Tertiary',
        'polytechnic': data_dir / 'Academic' / 'Tertiary',
        'ican': data_dir / 'Professional',
        'nimb': data_dir / 'Professional',
        'scholarship': data_dir / 'Scholarships',
        'ptdf': data_dir / 'Scholarships',
        'fsb': data_dir / 'Scholarships',
    }
    
    # Track if we moved any files to decide what to print
    files_moved = 0
    
    for item in unsorted_dir.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            # Convert filename to lowercase for easier matching
            lower_name = item.name.lower()
            
            dest_folder = None
            
            # Find the first matching keyword
            for keyword, folder_path in sort_rules.items():
                if keyword in lower_name:
                    dest_folder = folder_path
                    break
            
            if not dest_folder:
                # Default "catch-all" if no keywords match
                dest_folder = data_dir / 'Misc'
            
            # Ensure destination folder exists
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            dest_path = dest_folder / item.name
            
            # Handle naming collisions: if file already exists in destination, append a number
            counter = 1
            while dest_path.exists():
                name_without_ext = item.stem
                ext = item.suffix
                dest_path = dest_folder / f"{name_without_ext}_{counter}{ext}"
                counter += 1
                
            shutil.move(str(item), str(dest_path))
            print(f"Sorted: {item.name} -> {dest_path.relative_to(root)}")
            files_moved += 1

    if files_moved > 0:
        print(f"Successfully sorted {files_moved} files from data/unsorted.")
    else:
        print("No new files found in data/unsorted to sort.")

if __name__ == '__main__':
    sort_files()
