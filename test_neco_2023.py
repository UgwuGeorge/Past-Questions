import requests
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ALOC_ACCESS_TOKEN", 'ALOC-ad6bb1e7fbf4f457885e')

HEADERS = {
    'Accept': 'application/json',
    'AccessToken': ACCESS_TOKEN
}

url = "https://questions.aloc.com.ng/api/v2/q?subject=english&year=2023&type=neco"
print(f"Testing URL: {url}")
resp = requests.get(url, headers=HEADERS)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    print(resp.json())
else:
    print(resp.text)
