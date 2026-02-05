#!/usr/bin/env python
"""
Test desktop application upload functionality
"""
import sys
import os

# Add desktop_app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'desktop_app'))

from services.api_client import APIClient
import requests

def test_desktop_upload():
    """Test if desktop app can upload files to Django backend"""
    print("🧪 Testing Desktop App Upload to Django Backend...")
    
    # Create API client
    api_client = APIClient()
    
    # Test 1: Login first
    print("\n1. Logging in...")
    try:
        response = api_client.login("admin", "admin123")
        print("✅ Login successful!")
        print(f"User: {response.get('user', {}).get('username')}")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    # Test 2: Test upload with sample file
    print("\n2. Testing file upload...")
    sample_file = "sample_equipment_data.csv"
    
    if not os.path.exists(sample_file):
        print(f"❌ Sample file {sample_file} not found!")
        return False
    
    try:
        response = api_client.upload_csv(sample_file)
        print("✅ Upload successful!")
        print(f"Dataset ID: {response.get('dataset_id')}")
        print(f"Records processed: {response.get('record_count')}")
        return True
        
    except requests.RequestException as e:
        error_msg = api_client.handle_request_error(e)
        print(f"❌ Upload failed: {error_msg}")
        
        # Print more debug info
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response headers: {dict(e.response.headers)}")
            print(f"Response content: {e.response.text[:500]}")
        
        return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

if __name__ == '__main__':
    test_desktop_upload()