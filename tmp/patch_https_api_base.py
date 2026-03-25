import os

target_dir = r"c:\Users\ugwug\.gemini\antigravity\scratch\Past-Questions\frontend\src"

for root, _, files in os.walk(target_dir):
    for file in files:
        if file.endswith((".js", ".jsx")):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            target_string1 = 'const API_BASE = `http://${window.location.hostname}:8000/api`;'
            target_string2 = 'const API_BASE = "http://" + window.location.hostname + ":8000/api";'

            new_string = 'const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000/api`;'

            if target_string1 in content or target_string2 in content:
                content = content.replace(target_string1, new_string)
                content = content.replace(target_string2, new_string)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated {filepath}")
