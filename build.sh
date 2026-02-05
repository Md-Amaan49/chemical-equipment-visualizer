#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting build process ==="

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create database directory if it doesn't exist
echo "Creating database directory..."
mkdir -p /tmp

# Make migrations for all apps
echo "Making migrations..."
python manage.py makemigrations --noinput

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Verify database was created properly
echo "Verifying database..."
python manage.py shell -c "
from django.contrib.auth.models import User
print(f'Database verification: User table exists, count: {User.objects.count()}')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "=== Build process completed ==="