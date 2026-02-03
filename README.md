# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for analyzing and visualizing chemical equipment data. Built with Django REST API backend, React.js web frontend, and PyQt5 desktop application.

## 🚀 Features

- **Hybrid Architecture**: Both web and desktop interfaces using the same backend API
- **CSV Data Processing**: Upload and analyze chemical equipment data with Pandas
- **Interactive Visualizations**: Charts and tables using Chart.js (web) and Matplotlib (desktop)
- **History Management**: Automatic storage of last 5 uploaded datasets
- **PDF Report Generation**: Comprehensive reports with statistics and charts
- **Authentication**: Session-based authentication for secure access
- **Sample Data**: Pre-loaded demonstration data for testing

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   React.js      │    │   PyQt5         │
│   Web App       │    │   Desktop App   │
│   (Chart.js)    │    │   (Matplotlib)  │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
          ┌─────────────────┐
          │   Django REST   │
          │   Framework     │
          │   Backend API   │
          └─────────┬───────┘
                    │
          ┌─────────────────┐
          │   SQLite        │
          │   Database      │
          │   + Analytics   │
          └─────────────────┘
```

## 📋 Requirements

### Backend
- Python 3.8+
- Django 4.2+
- Django REST Framework
- Pandas
- ReportLab
- Matplotlib

### Frontend (Web)
- Node.js 16+
- React.js 18+
- Chart.js
- Axios

### Frontend (Desktop)
- Python 3.8+
- PyQt5
- Matplotlib
- Requests

## 🛠️ Installation & Setup

### 1. Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd chemical-equipment-visualizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 2. Web Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 3. Desktop Application Setup

```bash
# Install PyQt5 dependencies
pip install PyQt5 matplotlib requests

# Run desktop application
python desktop_app/main.py
```

## 📊 Sample Data

The project includes `sample_equipment_data.csv` with 30 chemical equipment records:
- **Equipment Types**: Pumps, Valves, Heat Exchangers, Reactors, Compressors
- **Parameters**: Flowrate (L/min), Pressure (bar), Temperature (K)
- **Realistic Values**: Based on typical chemical plant equipment

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/user/` - Current user info

### Data Management
- `POST /api/upload/` - Upload CSV file
- `GET /api/analytics/{id}/` - Get dataset analytics
- `GET /api/datasets/` - List all datasets
- `GET /api/history/` - Get last 5 datasets
- `DELETE /api/datasets/{id}/` - Delete dataset

### Reports
- `POST /api/reports/generate/` - Generate PDF report
- `GET /api/reports/{id}/download/` - Download PDF report

### Sample Data
- `POST /api/sample/load/` - Load sample data
- `GET /api/sample/info/` - Get sample data info

## 🧪 Testing

Run the integration test suite:

```bash
python test_integration.py
```

This tests:
- User management
- CSV data processing
- Analytics calculations
- Database operations
- History management
- PDF report generation
- Data validation

## 📱 Usage

### Web Application
1. Open browser to `http://localhost:3000`
2. Login with your credentials
3. Upload CSV file or load sample data
4. View interactive charts and data tables
5. Generate and download PDF reports
6. Access dataset history

### Desktop Application
1. Run `python desktop_app/main.py`
2. Login with your credentials
3. Same functionality as web app with native desktop interface
4. Matplotlib-based charts and Qt widgets

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/
│   ├── chemical_equipment_visualizer/  # Django project
│   ├── api/                           # API endpoints
│   ├── authentication/                # Auth views
│   ├── analytics/                     # Data models & processing
│   └── manage.py
├── frontend/                          # React.js web app
│   ├── src/
│   │   ├── components/               # React components
│   │   ├── services/                 # API client
│   │   └── App.js
│   └── package.json
├── desktop_app/                       # PyQt5 desktop app
│   ├── main.py                       # Main application
│   ├── widgets/                      # UI widgets
│   └── services/                     # API client
├── sample_equipment_data.csv          # Sample data
├── test_integration.py               # Integration tests
└── README.md
```

## 🔒 Security Features

- Session-based authentication
- CSRF protection
- File upload validation
- SQL injection prevention
- Input sanitization
- Error handling with secure responses

## 📈 Performance

- Efficient CSV processing with Pandas
- Database query optimization
- File size limits (10MB)
- Rolling dataset history (5 datasets max)
- Bulk database operations
- Memory-efficient PDF generation

## 🎯 Key Features Demonstrated

1. **Full-Stack Development**: Django backend + React frontend + PyQt5 desktop
2. **Data Processing**: CSV parsing, validation, and analytics with Pandas
3. **API Design**: RESTful endpoints with proper HTTP status codes
4. **Database Design**: Relational models with proper relationships
5. **Authentication**: Session-based auth with protected endpoints
6. **File Handling**: Upload, validation, and processing
7. **Report Generation**: PDF creation with charts and statistics
8. **Cross-Platform**: Same backend serving multiple frontend types
9. **Error Handling**: Comprehensive error responses and validation
10. **Testing**: Integration test suite covering all components

## 🚀 Deployment

For production deployment:

1. Configure environment variables
2. Use PostgreSQL instead of SQLite
3. Set up static file serving
4. Configure CORS for production domains
5. Use production WSGI server (Gunicorn)
6. Set up reverse proxy (Nginx)

## 📝 License

This project is created for internship screening purposes and demonstrates full-stack development capabilities with hybrid web/desktop architecture.

## 🤝 Contributing

This is a demonstration project. For improvements or questions, please contact the developer.

---

**Built with ❤️ for internship screening - demonstrating full-stack development skills with modern web technologies and desktop application development.**