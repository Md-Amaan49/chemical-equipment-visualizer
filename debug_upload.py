#!/usr/bin/env python
"""
Debug desktop application upload with detailed logging
"""
import sys
import os

# Add desktop_app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'desktop_app'))

from services.api_client import APIClient
import requests

def debug_upload():
    """Debug upload process step by step"""
    print("🔍 Debugging Desktop App Upload Process...")
    
    # Create API client
    api_client = APIClient()
    
    # Test 1: Login and check session
    print("\n1. Login and check session...")
    try:
        login_response = api_client.login("admin", "admin123")
        print("✅ Login successful!")
        print(f"Session cookies: {dict(api_client.session.cookies)}")
        
        # Check auth status
        auth_response = api_client.check_auth_status()
        print(f"✅ Auth check successful: {auth_response.get('user', {}).get('username')}")
        
    except Exception as e:
        print(f"❌ Login/auth failed: {e}")
        return False
    
    # Test 2: Test upload with detailed logging
    print("\n2. Testing upload with session cookies...")
    sample_file = "sample_equipment_data.csv"
    
    if not os.path.exists(sample_file):
        print(f"❌ Sample file {sample_file} not found!")
        return False
    
    try:
        # Manual upload test to see what's happening
        url = f"{api_client.base_url}/upload/"
        print(f"Upload URL: {url}")
        print(f"Session cookies: {dict(api_client.session.cookies)}")
        
        with open(sample_file, 'rb') as file_obj:
            files = {'file': (os.path.basename(sample_file), file_obj, 'text/csv')}
            
            # Test with session cookies
            response = requests.post(url, files=files, cookies=api_client.session.cookies)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                print("✅ Upload successful!")
                print(f"Dataset ID: {data.get('dataset_id')}")
                print(f"Records processed: {data.get('record_count')}")
                return True
            else:
                print(f"❌ Upload failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

if __name__ == '__main__':
    debug_upload()