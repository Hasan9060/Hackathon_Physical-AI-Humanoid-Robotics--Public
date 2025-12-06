import requests
import json

# Test the query endpoint with Gemini
url = "http://localhost:8000/query"
data = {
    "question": "What is ROS 2?",
    "max_results": 3
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("\n[SUCCESS] Query successful!")
    print(f"\nAnswer: {result.get('answer', 'No answer')}")
    print(f"\nConfidence: {result.get('confidence', 0)}")
    print(f"\nSources found: {len(result.get('sources', []))}")
else:
    print("\n[ERROR] Query failed!")
    print(f"Error: {response.text}")