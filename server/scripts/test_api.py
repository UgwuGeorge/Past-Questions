import os
import requests

def test_neco_api():
    url = "https://questions.aloc.com.ng/api/v2/m?subject=mathematics&year=2020&type=neco"
    access_token = os.getenv("ALOC_ACCESS_TOKEN")
    headers = {
        "Accept": "application/json",
        "AccessToken": access_token,
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Successfully fetched data!")
            # Print a small sample of the data
            print(f"Exam: {data.get('data', {}).get('exam')}")
            print(f"Subject: {data.get('data', {}).get('subject')}")
            questions = data.get('data', {}).get('questions', [])
            print(f"Number of questions found: {len(questions)}")
            if questions:
                print("First question sample:")
                print(questions[0].get('question'))
        else:
            print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_neco_api()
