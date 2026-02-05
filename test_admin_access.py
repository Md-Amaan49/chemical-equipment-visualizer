#!/usr/bin/env python3
"""
Test script for admin panel access
"""
import requests

BASE_URL = "http://localhost:8000"

def test_admin_access():
    """Test admin panel accessibility"""
    print("Testing admin panel access...")
    try:
        response = requests.get(f"{BASE_URL}/admin/")
        print(f"Admin panel status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Admin panel is accessible")
            return True
        elif response.status_code == 302:
            print("✅ Admin panel redirects to login (expected)")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Admin panel test failed: {e}")
        return False

if __name__ == "__main__":
    test_admin_access()