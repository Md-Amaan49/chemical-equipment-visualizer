#!/usr/bin/env python
"""
Setup admin user for Chemical Equipment Parameter Visualizer
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_equipment_visualizer.settings')
django.setup()

from django.contrib.auth.models import User

def setup_admin():
    """Create or update admin user"""
    username = 'admin'
    password = 'admin123'
    email = 'admin@example.com'
    
    try:
        # Try to get existing admin user
        admin_user = User.objects.get(username=username)
        print(f"Admin user '{username}' already exists. Updating password...")
        admin_user.set_password(password)
        admin_user.email = email
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print(f"✅ Admin user '{username}' password updated successfully!")
        
    except User.DoesNotExist:
        # Create new admin user
        print(f"Creating new admin user '{username}'...")
        admin_user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Admin user '{username}' created successfully!")
    
    print(f"\n🔐 Login Credentials:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Email: {email}")
    
    return admin_user

if __name__ == '__main__':
    setup_admin()