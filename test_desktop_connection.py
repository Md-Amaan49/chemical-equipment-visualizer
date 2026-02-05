#!/usr/bin/env python
"""
Test desktop application connection to Django backend
"""
import sys
import os

# Add desktop_app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'desktop_app'))

from services.api_client import APIClient
import requests

def test_desktop_connection():
    """Test if desktop app can connect to Django backend"""
    print("🧪 Testing Desktop App Connection to Django Backend...")
    
    # Create API client
    api_client = APIClient()
    
    # Test 1: Basic connection
    print("\n1. Testing basic connection...")
    try:
        response = requests.get("http://localhost:8000/api/sample/info/")
        print(f"✅ Server is reachable: {response.status_code}")
    except requests.ConnectionError:
        print("❌ Cannot connect to Django server!")
        print("Make sure Django server is running: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # Test 2: Login functionality
    print("\n2. Testing login functionality...")
    try:
        response = api_client.login("admin", "admin123")
        print("✅ Login successful!")
        print(f"User: {response.get('user', {}).get('username')}")
    except requests.RequestException as e:
        error_msg = api_client.handle_request_error(e)
        print(f"❌ Login failed: {error_msg}")
        return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Test 3: Check authentication status
    print("\n3. Testing authentication status...")
    try:
        response = api_client.check_auth_status()
        print("✅ Authentication check successful!")
        print(f"Authenticated user: {response.get('user', {}).get('username')}")
    except requests.RequestException as e:
        error_msg = api_client.handle_request_error(e)
        print(f"❌ Auth check failed: {error_msg}")
        return False
    except Exception as e:
        print(f"❌ Auth check error: {e}")
        return False
    
    # Test 4: Test sample data info (no auth required)
    print("\n4. Testing sample data info...")
    try:
        response = requests.get("http://localhost:8000/api/sample/info/")
        data = response.json()
        print("✅ Sample data info retrieved!")
        print(f"Sample file: {data.get('filename')}")
        print(f"Record count: {data.get('record_count')}")
    except Exception as e:
        print(f"❌ Sample data info error: {e}")
        return False
    
    print("\n🎉 All desktop connection tests passed!")
    print("\nDesktop application should work correctly.")
    print("To run the desktop app: python desktop_app/main.py")
    
    return True

if __name__ == '__main__':
    test_desktop_connection()