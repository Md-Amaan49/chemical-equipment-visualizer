#!/usr/bin/env python
"""
Comprehensive integration test for both web and desktop applications
"""
import sys
import os
import requests

# Add desktop_app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'desktop_app'))

from services.api_client import APIClient

def test_web_integration():
    """Test web application integration"""
    print("🌐 Testing Web Application Integration...")
    
    session = requests.Session()
    
    # Test login
    try:
        login_url = "http://localhost:8000/api/auth/login/"
        login_data = {"username": "admin", "password": "admin123"}
        response = session.post(login_url, json=login_data)
        response.raise_for_status()
        print("✅ Web login successful")
    except Exception as e:
        print(f"❌ Web login failed: {e}")
        return False
    
    # Test upload
    try:
        upload_url = "http://localhost:8000/api/upload/"
        with open("sample_equipment_data.csv", 'rb') as file_obj:
            files = {'file': file_obj}
            response = session.post(upload_url, files=files)
        response.raise_for_status()
        data = response.json()
        dataset_id = data.get('dataset_id')
        print(f"✅ Web upload successful - Dataset ID: {dataset_id}")
    except Exception as e:
        print(f"❌ Web upload failed: {e}")
        return False
    
    # Test analytics
    try:
        analytics_url = f"http://localhost:8000/api/analytics/{dataset_id}/"
        response = session.get(analytics_url)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Web analytics successful - Records: {data.get('summary', {}).get('total_count')}")
    except Exception as e:
        print(f"❌ Web analytics failed: {e}")
        return False
    
    # Test history
    try:
        history_url = "http://localhost:8000/api/history/"
        response = session.get(history_url)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Web history successful - Datasets: {len(data.get('datasets', []))}")
    except Exception as e:
        print(f"❌ Web history failed: {e}")
        return False
    
    return True

def test_desktop_integration():
    """Test desktop application integration"""
    print("\n🖥️  Testing Desktop Application Integration...")
    
    api_client = APIClient()
    
    # Test login
    try:
        response = api_client.login("admin", "admin123")
        print("✅ Desktop login successful")
    except Exception as e:
        print(f"❌ Desktop login failed: {e}")
        return False
    
    # Test upload
    try:
        response = api_client.upload_csv("sample_equipment_data.csv")
        dataset_id = response.get('dataset_id')
        print(f"✅ Desktop upload successful - Dataset ID: {dataset_id}")
    except Exception as e:
        print(f"❌ Desktop upload failed: {e}")
        return False
    
    # Test analytics
    try:
        response = api_client.get_analytics(dataset_id)
        print(f"✅ Desktop analytics successful - Records: {response.get('summary', {}).get('total_count')}")
    except Exception as e:
        print(f"❌ Desktop analytics failed: {e}")
        return False
    
    # Test history
    try:
        response = api_client.get_history()
        print(f"✅ Desktop history successful - Datasets: {len(response.get('datasets', []))}")
    except Exception as e:
        print(f"❌ Desktop history failed: {e}")
        return False
    
    return True

def main():
    """Run comprehensive integration tests"""
    print("🧪 Running Comprehensive Integration Tests...")
    print("=" * 60)
    
    # Check if sample file exists
    if not os.path.exists("sample_equipment_data.csv"):
        print("❌ Sample file 'sample_equipment_data.csv' not found!")
        return False
    
    # Test web integration
    web_success = test_web_integration()
    
    # Test desktop integration
    desktop_success = test_desktop_integration()
    
    print("\n" + "=" * 60)
    print("📊 Integration Test Results:")
    print(f"Web Application: {'✅ PASS' if web_success else '❌ FAIL'}")
    print(f"Desktop Application: {'✅ PASS' if desktop_success else '❌ FAIL'}")
    
    if web_success and desktop_success:
        print("\n🎉 All integration tests passed!")
        print("Both web and desktop applications are working correctly.")
        return True
    else:
        print("\n❌ Some integration tests failed.")
        return False

if __name__ == '__main__':
    main()