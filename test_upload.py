#!/usr/bin/env python
"""
Test CSV upload functionality
"""
import requests
import json

def test_sample_data_load():
    """Test loading sample data"""
    base_url = 'http://localhost:8000'
    login_url = f'{base_url}/api/auth/login/'
    sample_url = f'{base_url}/api/sample/load/'
    
    # First login
    session = requests.Session()
    
    login_data = {'username': 'admin', 'password': 'admin123'}
    login_response = session.post(login_url, json=login_data)
    
    print(f"Login Status: {login_response.status_code}")
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    print("✅ Login successful!")
    
    # Test sample data loading
    print("\n🧪 Testing sample data loading...")
    sample_response = session.post(sample_url)
    
    print(f"Sample Data Status: {sample_response.status_code}")
    
    if sample_response.status_code == 201:
        print("✅ Sample data loaded successfully!")
        response_data = sample_response.json()
        print(f"Dataset ID: {response_data['dataset_id']}")
        print(f"Record Count: {response_data['record_count']}")
        print(f"Equipment Types: {list(response_data['summary']['type_distribution'].keys())}")
    else:
        print("❌ Sample data loading failed!")
        print(f"Response: {sample_response.text}")

def test_csv_upload():
    """Test CSV file upload"""
    base_url = 'http://localhost:8000'
    login_url = f'{base_url}/api/auth/login/'
    upload_url = f'{base_url}/api/upload/'
    
    # First login
    session = requests.Session()
    
    login_data = {'username': 'admin', 'password': 'admin123'}
    login_response = session.post(login_url, json=login_data)
    
    print(f"\nLogin Status: {login_response.status_code}")
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    print("✅ Login successful!")
    
    # Test CSV upload with sample file
    print("\n🧪 Testing CSV upload...")
    
    try:
        with open('sample_equipment_data.csv', 'rb') as f:
            files = {'file': ('test_equipment.csv', f, 'text/csv')}
            upload_response = session.post(upload_url, files=files)
        
        print(f"Upload Status: {upload_response.status_code}")
        
        if upload_response.status_code == 201:
            print("✅ CSV upload successful!")
            response_data = upload_response.json()
            print(f"Dataset ID: {response_data['dataset_id']}")
            print(f"Record Count: {response_data['record_count']}")
        else:
            print("❌ CSV upload failed!")
            print(f"Response: {upload_response.text}")
            
    except FileNotFoundError:
        print("❌ Sample CSV file not found!")

if __name__ == '__main__':
    test_sample_data_load()
    test_csv_upload()