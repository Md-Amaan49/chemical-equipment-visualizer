#!/usr/bin/env python3
"""
Test script for production endpoints on Render
"""
import requests
import json

PRODUCTION_URL = "https://chemical-equipment-backend-2p9z.onrender.com"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing production health check endpoint...")
    try:
        response = requests.get(f"{PRODUCTION_URL}/", timeout=30)
        print(f"Health check status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Response text: {response.text[:500]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_auth_test_endpoint():
    """Test the auth test endpoint"""
    print("\nTesting production auth test endpoint...")
    try:
        response = requests.get(f"{PRODUCTION_URL}/api/auth/test/", timeout=30)
        print(f"Auth test status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Response text: {response.text[:500]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Auth test failed: {e}")
        return False

def test_login_endpoint():
    """Test the login endpoint"""
    print("\nTesting production login endpoint...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(
            f"{PRODUCTION_URL}/api/auth/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        print(f"Login status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Response text: {response.text[:500]}")
        return response.status_code in [200, 401]
    except Exception as e:
        print(f"Login test failed: {e}")
        return False

def test_admin_panel():
    """Test admin panel"""
    print("\nTesting production admin panel...")
    try:
        response = requests.get(f"{PRODUCTION_URL}/admin/", timeout=30)
        print(f"Admin panel status: {response.status_code}")
        return response.status_code in [200, 302]  # 302 redirect to login is OK
    except Exception as e:
        print(f"Admin panel test failed: {e}")
        return False

def main():
    print("=== Testing Production Endpoints ===")
    print(f"Production URL: {PRODUCTION_URL}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Auth Test", test_auth_test_endpoint),
        ("Login", test_login_endpoint),
        ("Admin Panel", test_admin_panel),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        result = test_func()
        results.append((test_name, result))
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*50}")
    print("=== Test Summary ===")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All production tests passed!")
    else:
        print("❌ Some production tests failed.")
        print("\n🔍 Debugging suggestions:")
        print("1. Check Render deployment logs")
        print("2. Verify environment variables are set")
        print("3. Check if database migrations ran successfully")
    
    return passed == total

if __name__ == "__main__":
    main()