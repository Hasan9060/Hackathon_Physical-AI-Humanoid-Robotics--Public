#!/usr/bin/env python3
"""
Test Urdu translation functionality
"""

import asyncio
import httpx
import json

async def test_urdu_translation():
    """Test Urdu translation endpoint"""

    print("Testing Urdu Translation Service...")
    print("=" * 50)

    # Test text
    test_text = """
    Welcome to the Physical AI & Humanoid Robotics Lab Guide.

    This comprehensive guide covers:
    - ROS 2 fundamentals
    - Simulation and digital twins
    - AI control systems
    - Hardware procurement

    Learn how to build academic robotics infrastructure.
    """

    print(f"Original text (first 100 chars): {test_text[:100]}...")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test direct translation
            print("\n1. Testing direct translation...")
            response = await client.post(
                "http://localhost:8000/api/v1/translate",
                json={
                    "text": test_text,
                    "target_lang": "ur",
                    "source_lang": "en"
                }
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✓ Translation successful!")
                print(f"  Provider: {data['provider']}")
                print(f"  Chunks processed: {data['chunks_processed']}")
                print(f"  Cached: {data['cached']}")
                print(f"\nTranslated text:")
                print("-" * 40)
                print(data['translated_text'][:300] + "..." if len(data['translated_text']) > 300 else data['translated_text'])
                print("-" * 40)

                # Check if it contains Urdu characters
                has_urdu = any(ord(c) >= 0x0600 and ord(c) <= 0x06FF for c in data['translated_text'])
                if has_urdu:
                    print("\n✓ Translation contains Urdu characters!")
                else:
                    print("\n⚠ Translation might not contain Urdu characters")

            else:
                print(f"✗ Translation failed with status: {response.status_code}")
                print(f"Error: {response.text}")

            # Test chapter translation
            print("\n2. Testing chapter translation with progress...")
            chapter_response = await client.post(
                "http://localhost:8000/api/v1/translate-chapter",
                json={
                    "text": test_text,
                    "target_lang": "ur",
                    "source_lang": "en",
                    "chunk_size": 100  # Small chunks for testing
                }
            )

            if chapter_response.status_code == 200:
                chapter_data = chapter_response.json()
                task_id = chapter_data['task_id']
                print(f"✓ Chapter translation started")
                print(f"  Task ID: {task_id}")

                # Poll for progress
                max_attempts = 10
                for i in range(max_attempts):
                    await asyncio.sleep(1)  # Wait 1 second

                    progress_response = await client.get(
                        f"http://localhost:8000/api/v1/translate-progress/{task_id}"
                    )

                    if progress_response.status_code == 200:
                        progress_data = progress_response.json()
                        print(f"\n  Progress check {i+1}:")
                        print(f"    Status: {progress_data['status']}")
                        print(f"    Progress: {progress_data['progress']*100:.1f}%")
                        print(f"    Chunk: {progress_data['current_chunk']}/{progress_data['total_chunks']}")

                        if progress_data['status'] == 'completed':
                            print("\n✓ Chapter translation completed!")
                            print(f"Translated text preview:")
                            print("-" * 40)
                            preview = progress_data['translated_text'][:200] + "..." if len(progress_data['translated_text']) > 200 else progress_data['translated_text']
                            print(preview)
                            print("-" * 40)
                            break
                        elif progress_data['status'] == 'failed':
                            print(f"\n✗ Chapter translation failed: {progress_data['error']}")
                            break

            else:
                print(f"✗ Chapter translation failed to start: {chapter_response.status_code}")

            # Test translation stats
            print("\n3. Testing translation stats...")
            stats_response = await client.get("http://localhost:8000/api/v1/translation-stats")

            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                print(f"✓ Translation stats:")
                print(f"  Cache size: {stats_data['cache_size']}")
                print(f"  Active tasks: {stats_data['active_tasks']}")

    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        print("\nMake sure the backend server is running on http://localhost:8000")
        print("Run: cd backend && python3 main.py")

if __name__ == "__main__":
    print("Starting Urdu translation test...\n")
    asyncio.run(test_urdu_translation())