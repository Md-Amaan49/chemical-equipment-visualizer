#!/usr/bin/env python3
"""
Test script to check backend connection and endpoints
"""
import requests
import json

# Backend URL
BACKEND_URL = "https://chemical-equipment-backend-2p9z.onrender.com"

def test_backend_connection():
    """Test various backend endpoints to identify issues"""
    
    print("🔍 Testing Backend Connection...")
    print(f"Backend URL: {BACKEND_URL}")
    print("-" * 50)
    
    # Test 1: Root endpoint (health check)
    print("1. Testing root endpoint (health check)...")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=30)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Root endpoint working!")
        else:
            print("   ❌ Root endpoint failed!")
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
    
    print()
    
    # Test 2: Admin endpoint
    print("2. Testing admin endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/admin/", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Admin endpoint accessible!")
        elif response.status_code == 302:
            print("   ✅ Admin endpoint redirecting (normal behavior)!")
        else:
            print(f"   ❌ Admin endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Admin endpoint error: {e}")
    
    print()
    
    # Test 3: Auth test endpoint
    print("3. Testing auth test endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/auth/test/", timeout=30)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Auth test endpoint working!")
        else:
            print("   ❌ Auth test endpoint failed!")
    except Exception as e:
        print(f"   ❌ Auth test endpoint error: {e}")
    
    print()
    
    # Test 4: Login endpoint (GET request - should return method not allowed)
    print("4. Testing login endpoint (GET request)...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/auth/login/", timeout=30)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 405:
            print("   ✅ Login endpoint exists (method not allowed for GET is expected)!")
        elif response.status_code == 200:
            print("   ✅ Login endpoint accessible!")
        else:
            print(f"   ❌ Login endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Login endpoint error: {e}")
    
    print()
    
    # Test 5: Login endpoint (POST request with test data)
    print("5. Testing login endpoint (POST request)...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(
            f"{BACKEND_URL}/api/auth/login/", 
            json=login_data,
            headers=headers,
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Login successful!")
        elif response.status_code == 401:
            print("   ⚠️  Login failed (credentials issue, but endpoint working)")
        else:
            print(f"   ❌ Login endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Login POST error: {e}")
    
    print()
    print("🏁 Backend connection test completed!")

if __name__ == "__main__":
    test_backend_connection()