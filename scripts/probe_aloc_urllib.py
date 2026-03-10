import urllib.request
import json
import ssl

token = "ALOC-78bfe77b49fb3e407bf8"
url = "https://questions.aloc.com.ng/api/v2/q?subject=chemistry"

headers = {
    "AccessToken": token,
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print(f"Probing {url} with AccessToken: {token}")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx) as response:
        print(f"Status Code: {response.getcode()}")
        data = json.loads(response.read().decode())
        print("Success! Data preview:")
        print(json.dumps(data, indent=2)[:500])
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
