#!/usr/bin/env python3
"""
Test database connectivity endpoint
"""
import requests

BASE_URL = "http://localhost:8000"

def test_db_endpoint():
    """Test the database connectivity endpoint"""
    print("Testing database connectivity endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/test-db/")
        print(f"DB test status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"DB test failed: {e}")
        return False

if __name__ == "__main__":
    test_db_endpoint()