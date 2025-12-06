"""
Test Signup with Long Password
"""
import httpx
import asyncio

async def test_long_password():
    print("=" * 60)
    print("TESTING SIGNUP WITH LONG PASSWORD")
    print("=" * 60)
    
    api_url = "http://localhost:8000"
    
    # Generate a password > 72 chars
    long_password = "a" * 100
    
    payload = {
        "email": "longpw@test.com",
        "password": long_password,
        "full_name": "Test Long PW",
        "software_background": "None",
        "hardware_background": "None",
        "learning_goals": "Testing"
    }
    
    try:
        response = httpx.post(f"{api_url}/signup", json=payload, timeout=10.0)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[PASS] Signup successful with 100 char password!")
            token = response.json()
            print(f"Token received: {token['access_token'][:10]}...")
        elif response.status_code == 400 and "already registered" in response.text:
             print("[PASS] User already exists (Test ran before)")
        else:
            print(f"[FAIL] Failed: {response.text}")
            
    except Exception as e:
        print(f"[FAIL] Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_long_password())
