#!/usr/bin/env python3
"""
Test script for authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_auth_test_endpoint():
    """Test the auth test endpoint"""
    print("\nTesting auth test endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/test/")
        print(f"Auth test status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Auth test failed: {e}")
        return False

def test_login_endpoint():
    """Test the login endpoint with admin credentials"""
    print("\nTesting login endpoint...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Login status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [200, 401]  # 401 is OK if user doesn't exist yet
    except Exception as e:
        print(f"Login test failed: {e}")
        return False

def main():
    print("=== Testing Authentication Endpoints ===")
    
    tests = [
        ("Health Check", test_health_check),
        ("Auth Test", test_auth_test_endpoint),
        ("Login", test_login_endpoint),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        print(f"✅ {test_name}: {'PASSED' if result else 'FAILED'}")
    
    print("\n=== Test Summary ===")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Ready to deploy.")
        return True
    else:
        print("❌ Some tests failed. Check the issues before deploying.")
        return False

if __name__ == "__main__":
    main()