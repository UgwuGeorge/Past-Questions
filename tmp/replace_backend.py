import os
import re

def replace_in_file(filepath, replacements, regex_replacements=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if regex_replacements:
        for pattern, new in regex_replacements.items():
            content = re.sub(pattern, new, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

replacements_ai = {
    '"ai_proctor_persona"': '"expert_proctor_persona"',
    "how the AI should act": "how the expert should act",
    "Analyze via AI": "Analyze via Expert Engine",
    "Generate via AI": "Generate via Expert Engine",
    "AI was told to include it": "Expert Engine was told to include it",
    "the AI should act": "the expert should act"
}

replace_in_file('c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_core/core/ai.py', replacements_ai)
replace_in_file('c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/agent_core/core/agent.py', replacements_ai)

print("Done backend remaining AI replacements.")
