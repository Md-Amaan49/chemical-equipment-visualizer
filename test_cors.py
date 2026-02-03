#!/usr/bin/env python
"""
Test CORS and frontend-like requests
"""
import requests
import json

def test_cors_login():
    """Test login with CORS headers like a browser would send"""
    base_url = 'http://localhost:8000'
    login_url = f'{base_url}/api/auth/login/'
    
    # Headers that a browser would send
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000',
        'Referer': 'http://localhost:3000/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    credentials = {'username': 'admin', 'password': 'admin123'}
    
    print("🧪 Testing CORS Login (Browser-like request)...")
    print(f"URL: {login_url}")
    print(f"Origin: {headers['Origin']}")
    
    try:
        # First test OPTIONS request (preflight)
        options_response = requests.options(login_url, headers=headers)
        print(f"\nOPTIONS preflight:")
        print(f"Status: {options_response.status_code}")
        print(f"CORS headers: {dict(options_response.headers)}")
        
        # Then test actual POST request
        response = requests.post(
            login_url,
            data=json.dumps(credentials),
            headers=headers,
            timeout=10
        )
        
        print(f"\nPOST request:")
        print(f"Status Code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        else:
            print("❌ Login failed!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure Django server is running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_cors_login()