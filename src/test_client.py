import requests
import json

BASE_URL = "http://192.168.1.171:8502"

def test_live_api():
    print("Testing Root Endpoint...")
    res = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {res.status_code}")
    print(f"Raw Response Text: {res.text}\n")

    print("Testing Health Check Endpoint...")
    res = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {res.status_code}")
    print(f"Raw Response Text: {res.text}\n")

    print("Testing Audit Endpoint...")
    payload = {
        "query": "What is the review timeframe for transaction monitoring alerts exceeding $10,000?"
    }
    res = requests.post(f"{BASE_URL}/audit", json=payload)
    print(f"Status Code: {res.status_code}")
    print(f"Raw Response Text: {res.text}")
    if res.status_code == 200:
        print("Parsed JSON:")
        print(json.dumps(res.json(), indent=2))

if __name__ == "__main__":
    try:
        test_live_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to FastAPI server. Make sure it is running with 'uvicorn src.api:app --reload'")