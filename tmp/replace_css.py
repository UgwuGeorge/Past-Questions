import os

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

replacements_css = {
    ".ask-ai-fab": ".ask-expert-fab"
}
replace_in_file('c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/frontend/src/App.css', replacements_css)

print("Done CSS replacements.")
