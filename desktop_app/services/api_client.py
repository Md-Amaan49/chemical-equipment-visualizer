"""
API Client for desktop application
Handles communication with Django REST API backend
"""

import requests
import json
from typing import Dict, Any, Optional


class APIClient:
    """Client for communicating with the Django REST API"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user"""
        url = f"{self.base_url}/auth/login/"
        data = {
            'username': username,
            'password': password
        }
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def logout(self) -> Dict[str, Any]:
        """Logout user"""
        url = f"{self.base_url}/auth/logout/"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()
    
    def check_auth_status(self) -> Dict[str, Any]:
        """Check current authentication status"""
        url = f"{self.base_url}/auth/user/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """Upload CSV file"""
        url = f"{self.base_url}/upload/"
        
        with open(file_path, 'rb') as file:
            files = {'file': file}
            # Remove Content-Type header for file upload
            headers = {k: v for k, v in self.session.headers.items() 
                      if k.lower() != 'content-type'}
            response = self.session.post(url, files=files, headers=headers)
        
        response.raise_for_status()
        return response.json()
    
    def get_analytics(self, dataset_id: int) -> Dict[str, Any]:
        """Get analytics for a specific dataset"""
        url = f"{self.base_url}/analytics/{dataset_id}/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_datasets(self) -> Dict[str, Any]:
        """Get all datasets for current user"""
        url = f"{self.base_url}/datasets/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_history(self) -> Dict[str, Any]:
        """Get dataset history (last 5 datasets)"""
        url = f"{self.base_url}/history/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def delete_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """Delete a specific dataset"""
        url = f"{self.base_url}/datasets/{dataset_id}/"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()
    
    def handle_request_error(self, error: requests.RequestException) -> str:
        """Handle and format request errors"""
        if hasattr(error, 'response') and error.response is not None:
            try:
                error_data = error.response.json()
                return error_data.get('error', f'HTTP {error.response.status_code}')
            except:
                return f'HTTP {error.response.status_code}: {error.response.text}'
        else:
            return str(error)