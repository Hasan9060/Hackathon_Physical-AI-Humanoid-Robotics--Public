"""
Test the chatbot query endpoint
"""

import httpx
import asyncio

async def test_query():
    api_url = "http://localhost:8000"
    
    print("🧪 Testing Chatbot Query...")
    print("=" * 60)
    
    # Test 1: Simple health check
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = httpx.get(f"{api_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Query endpoint
    print("\n2️⃣ Testing query endpoint...")
    try:
        response = httpx.post(
            f"{api_url}/query",
            json={
                "question": "What is ROS 2?",
                "max_results": 5
            },
            timeout=30.0
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Query successful!")
            print(f"\n   📝 Answer: {data['answer'][:200]}...")
            print(f"   📊 Confidence: {data['confidence']}")
            print(f"   📚 Sources: {len(data['sources'])}")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_query())
