import requests
import json

# Setup
BASE_URL = "https://localhost:8000/api"
CERTS = ("agent_core/certs/cert.pem", "agent_core/certs/key.pem")

# We'll use a test user. Usually there's one created at start.
# Let's try to register or login a test user.
USER_DATA = {
    "username": "test_monetize_user",
    "email": "test_monetize@example.com",
    "password": "testpassword123"
}

def check_access():
    print("1. Registering/Logging In...")
    try:
        resp = requests.post(f"{BASE_URL}/auth/register", json=USER_DATA, verify=False)
        if resp.status_code != 200:
            resp = requests.post(f"{BASE_URL}/auth/login", json={"username": USER_DATA["username"], "password": USER_DATA["password"]}, verify=False)
        
        data = resp.json()
        token = data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Check Subscription Status
        print("2. Checking status...")
        status_resp = requests.get(f"{BASE_URL}/subscription/status", headers=headers, verify=False)
        status = status_resp.json()
        print(f"Current Status: {status['tier']}")
        
        # 3. Find an ICAN exam (ID might vary, we'll fetch ID)
        print("3. Fetching exams...")
        exams_resp = requests.get(f"{BASE_URL}/exams?name=ICAN", headers=headers, verify=False)
        exams = exams_resp.json()
        ican_exam = next((e for e in exams if "ICAN" in e["name"]), None)
        
        if not ican_exam:
            print("No ICAN exam found. Available exams:")
            print([e['name'] for e in exams])
            return

        print(f"Found ICAN Exam: {ican_exam['name']} (Required Tier: {ican_exam['required_tier']})")
        
        # 4. Attempt to start simulation (should fail)
        print("4. Attempting to start simulation (should fail)...")
        sim_data = {"user_id": data["user"]["id"], "exam_id": ican_exam["id"], "question_count": 5}
        sim_resp = requests.post(f"{BASE_URL}/simulation/start", headers=headers, json=sim_data, verify=False)
        
        if sim_resp.status_code == 402:
            print(f"SUCCESS: System correctly blocked access. Message: {sim_resp.json()['detail']}")
        else:
            print(f"FAILURE: Got status {sim_resp.status_code} with reply: {sim_resp.text}")
            
        # 5. Purchase ELITE
        print("5. Upgrading to ELITE...")
        upgrade_resp = requests.post(f"{BASE_URL}/subscription/purchase", headers=headers, json={"tier": "ELITE"}, verify=False)
        print(f"Upgrade response: {upgrade_resp.json()['message']}")
        
        # 6. Retry start (should succeed)
        print("6. Retrying simulation start after upgrade...")
        sim_resp_v2 = requests.post(f"{BASE_URL}/simulation/start", headers=headers, json=sim_data, verify=False)
        
        if sim_resp_v2.status_code == 200:
            print(f"SUCCESS: Simulation started with {len(sim_resp_v2.json()['questions'])} questions.")
        else:
            print(f"FAILURE: Post-upgrade simulation failed with status {sim_resp_v2.status_code}: {sim_resp_v2.text}")

    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    check_access()
