#!/usr/bin/env python
"""
Test upload using web-like approach to ensure compatibility
"""
import requests
import os

def test_web_upload():
    """Test upload using the same approach as web frontend"""
    print("🌐 Testing Web-like Upload to Django Backend...")
    
    # Create session
    session = requests.Session()
    
    # Test 1: Login
    print("\n1. Logging in...")
    try:
        login_url = "http://localhost:8000/api/auth/login/"
        login_data = {"username": "admin", "password": "admin123"}
        
        response = session.post(login_url, json=login_data)
        response.raise_for_status()
        
        print("✅ Login successful!")
        print(f"Session cookies: {dict(session.cookies)}")
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    # Test 2: Upload file (web-style)
    print("\n2. Testing file upload (web-style)...")
    sample_file = "sample_equipment_data.csv"
    
    if not os.path.exists(sample_file):
        print(f"❌ Sample file {sample_file} not found!")
        return False
    
    try:
        upload_url = "http://localhost:8000/api/upload/"
        
        with open(sample_file, 'rb') as file_obj:
            files = {'file': file_obj}
            response = session.post(upload_url, files=files)
        
        response.raise_for_status()
        data = response.json()
        
        print("✅ Upload successful!")
        print(f"Dataset ID: {data.get('dataset_id')}")
        print(f"Records processed: {data.get('record_count')}")
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return False

if __name__ == '__main__':
    test_web_upload()