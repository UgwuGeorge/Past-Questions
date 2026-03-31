import os

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

replacements_results = {
    "'ai'": "'expert'",
    "aiFeedback": "expertFeedback",
    "setAiFeedback": "setExpertFeedback",
    "aiAnalysisResult": "expertAnalysisResult",
    "setAiAnalysisResult": "setExpertAnalysisResult",
    "aiData": "expertData",
    "AI Analysis Result Section": "Expert Analysis Result Section",
    "/user/ai-feedback/": "/user/expert-feedback/"
}

replace_in_file('c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/frontend/src/pages/MyResults.jsx', replacements_results)

replacements_sub = {
    "customer@reharz.ai": "customer@reharz.com"
}
replace_in_file('c:/Users/ugwug/.gemini/antigravity/scratch/Past-Questions/frontend/src/pages/SubscriptionHub.jsx', replacements_sub)

print("Done frontend replacements.")
