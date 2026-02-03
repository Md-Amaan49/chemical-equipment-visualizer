#!/usr/bin/env python
"""
Test login functionality for Chemical Equipment Parameter Visualizer
"""
import requests
import json

def test_login():
    """Test the login API endpoint"""
    base_url = 'http://localhost:8000'
    login_url = f'{base_url}/api/auth/login/'
    
    # Test credentials
    credentials = [
        {'username': 'admin', 'password': 'admin123'},
        {'username': 'testuser', 'password': 'test123'}
    ]
    
    print("🧪 Testing Login API Endpoint...")
    print(f"URL: {login_url}")
    
    for cred in credentials:
        print(f"\n👤 Testing login for: {cred['username']}")
        
        try:
            response = requests.post(
                login_url,
                data=json.dumps(cred),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Login successful!")
                response_data = response.json()
                print(f"Response: {json.dumps(response_data, indent=2)}")
            else:
                print("❌ Login failed!")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed! Make sure Django server is running at http://localhost:8000")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_login()