# Quick Start Guide - Chemical Equipment Parameter Visualizer

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Md-Amaan49/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer
```

### 2. Backend Setup (Django)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create admin user
python setup_admin.py

# Start Django server
python manage.py runserver
```
Backend will be available at: `http://localhost:8000`

### 3. Frontend Setup (React)
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```
Frontend will be available at: `http://localhost:3000`

### 4. Desktop App (PyQt5)
```bash
# Install PyQt5 dependencies
pip install PyQt5 matplotlib requests

# Run desktop application
python desktop_app/main.py
```

## 🔐 Login Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 🧪 Test the Application

### Option 1: Load Sample Data
1. Login to the web app
2. Click "Load Sample Data" button
3. View 30 chemical equipment records with charts

### Option 2: Upload Your Own CSV
1. Create a CSV file with columns: `Equipment Name,Type,Flowrate,Pressure,Temperature`
2. Upload via the web interface
3. View analytics and generate PDF reports

## 📊 Features to Explore
- ✅ Interactive charts (Chart.js + Matplotlib)
- ✅ Data tables with equipment records
- ✅ PDF report generation
- ✅ Dataset history (last 5 uploads)
- ✅ Cross-platform (Web + Desktop)

## 🔧 Troubleshooting
- **CORS Issues**: Make sure both servers are running
- **Login Problems**: Use the provided credentials
- **Desktop App**: Requires PyQt5 installation

## 📱 Demo
The application demonstrates:
- Full-stack development (Django + React + PyQt5)
- Data processing with Pandas
- Interactive visualizations
- PDF generation
- Authentication systems
- Hybrid architecture

Perfect for showcasing modern web development skills! 🎉

## 🧪 Integration Testing

### Run Comprehensive Tests
```bash
# Test both web and desktop functionality
python test_integration.py

# Test desktop connection only
python test_desktop_connection.py

# Test desktop upload only
python test_desktop_upload.py
```

## ✅ Status Verification
Both web and desktop applications are fully functional:
- ✅ Authentication working (admin/admin123)
- ✅ File upload working (CSV processing)
- ✅ Data visualization working (Charts & tables)
- ✅ History management working (Last 5 datasets)
- ✅ PDF report generation working
- ✅ Desktop app connection working
- ✅ Cross-platform compatibility verified

## 🎯 Project Completion
This hybrid application successfully demonstrates:
- **Backend**: Django REST API with authentication
- **Frontend**: React.js with Chart.js visualizations
- **Desktop**: PyQt5 with Matplotlib charts
- **Data Processing**: Pandas for CSV analysis
- **File Management**: Upload, storage, and cleanup
- **Reporting**: PDF generation with analytics
- **Testing**: Comprehensive integration tests

Perfect for internship screening - showcases full-stack development skills! 🚀