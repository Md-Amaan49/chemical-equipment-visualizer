#!/usr/bin/env python3
"""
Startup script to ensure database is properly initialized
This runs before the main Django application starts
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_equipment_visualizer.settings')
    django.setup()

def ensure_database():
    """Ensure database is properly initialized"""
    print("=== Startup: Ensuring database is initialized ===")
    
    try:
        # Test if database exists and has tables
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        print(f"Database check: {user_count} users found")
        
        # Check if admin user exists
        admin_exists = User.objects.filter(username='admin').exists()
        if not admin_exists:
            print("Creating admin user...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("Admin user created: admin/admin123")
        else:
            print("Admin user already exists")
            
        print("=== Database is ready ===")
        return True
        
    except Exception as e:
        print(f"Database not ready: {e}")
        print("=== Running migrations ===")
        
        try:
            # Run migrations
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
            
            # Create admin user
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                print("Admin user created: admin/admin123")
            
            print("=== Database initialized successfully ===")
            return True
            
        except Exception as init_error:
            print(f"Failed to initialize database: {init_error}")
            return False

def main():
    """Main startup function"""
    setup_django()
    
    if ensure_database():
        print("=== Startup completed successfully ===")
        return True
    else:
        print("=== Startup failed ===")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)