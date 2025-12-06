import requests
import json

# Test the signup endpoint
url = "http://localhost:8000/signup"
data = {
    "email": "testuser2024@example.com",
    "password": "test123",
    "name": "Test User 3",
    "software_background": "Expert",
    "hardware_background": "Engineer",
    "learning_goals": "Build humanoid robots"
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    print("\n[SUCCESS] Signup successful!")
    print(f"Token: {response.json()['access_token'][:50]}...")
else:
    print("\n[ERROR] Signup failed!")
    print(f"Error: {response.text}")