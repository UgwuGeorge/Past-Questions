import requests

token = "ALOC-78bfe77b49fb3e407bf8"
url = "https://questions.aloc.com.ng/api/v2/q"
headers = {
    "AccessToken": token,
    "Accept": "application/json"
}
params = {"subject": "chemistry"}

print(f"Testing ALOC API with token: {token}")
r = requests.get(url, headers=headers, params=params)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:500]}")

# Try v1
url_v1 = "https://questions.aloc.com.ng/api/q"
r_v1 = requests.get(url_v1, headers=headers, params=params)
print(f"\nTesting ALOC API v1")
print(f"Status: {r_v1.status_code}")
print(f"Response: {r_v1.text[:500]}")

# Try .ng
url_ng = "https://questions.aloc.ng/api/v2/q"
r_ng = requests.get(url_ng, headers=headers, params=params)
print(f"\nTesting ALOC API .ng")
print(f"Status: {r_ng.status_code}")
print(f"Response: {r_ng.text[:500]}")
