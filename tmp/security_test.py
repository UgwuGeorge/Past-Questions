import requests
import sys

BASE_URL = "https://localhost:8000/api"

# Disable SSL warnings for local test
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_attack():
    print("--- STARTING SECURITY STRESS TEST ---")
    
    # 1. Register a fresh user
    reg_payload = {"username": "attacker", "email": "attacker@reharz.ai", "password": "password123"}
    try:
        r = requests.post(f"{BASE_URL}/auth/register", json=reg_payload, verify=False)
        print(f"Register 'attacker': {r.status_code}")
        if r.status_code != 200:
            # Maybe already exists, try login
            pass
    except Exception as e:
        print(f"Connection Failed: {e}")
        return

    # 2. Login as 'attacker'
    login_payload = {"username": "attacker", "password": "password123"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_payload, verify=False)
    print(f"Login 'attacker': {r.status_code}")
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 3. ATTACK A: IDOR (Accessing user 1's stats)
    r = requests.get(f"{BASE_URL}/user/1/stats", headers=headers, verify=False)
    print(f"ATTACK A (IDOR User 1): {r.status_code} - Expected 403")

    # 4. ATTACK B: Admin Bypass (Accessing global stats)
    r = requests.get(f"{BASE_URL}/admin/stats", headers=headers, verify=False)
    print(f"ATTACK B (Admin Bypass): {r.status_code} - Expected 403 or 401 depends on route")

    # 5. ATTACK C: Simulation Tampering (Fetch session 1)
    r = requests.get(f"{BASE_URL}/simulation/1/result", headers=headers, verify=False)
    print(f"ATTACK C (Simulation 1): {r.status_code} - Expected 403/404 if not owned")

    print("--- TEST COMPLETE ---")

if __name__ == "__main__":
    test_attack()
