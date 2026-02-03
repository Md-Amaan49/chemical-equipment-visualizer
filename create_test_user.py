#!/usr/bin/env python
"""
Create test user for Chemical Equipment Parameter Visualizer
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_equipment_visualizer.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    """Create or update test user"""
    username = 'testuser'
    password = 'test123'
    email = 'test@example.com'
    
    try:
        # Try to get existing test user
        test_user = User.objects.get(username=username)
        print(f"Test user '{username}' already exists. Updating password...")
        test_user.set_password(password)
        test_user.email = email
        test_user.save()
        print(f"✅ Test user '{username}' password updated successfully!")
        
    except User.DoesNotExist:
        # Create new test user
        print(f"Creating new test user '{username}'...")
        test_user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Test user '{username}' created successfully!")
    
    print(f"\n👤 Test User Credentials:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Email: {email}")
    
    return test_user

if __name__ == '__main__':
    create_test_user()