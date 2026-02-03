"""
Login widget for desktop application
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import requests


class LoginWidget(QWidget):
    """Login widget for user authentication"""
    
    login_successful = pyqtSignal(dict)  # Emitted when login succeeds
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create login form container
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.Box)
        form_frame.setMaximumWidth(400)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        
        # Title
        title_label = QLabel("Chemical Equipment Visualizer")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        form_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Please login to access the application")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 20px;")
        form_layout.addWidget(subtitle_label)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-weight: bold; color: #333;")
        form_layout.addWidget(username_label)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your username")
        self.username_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """)
        form_layout.addWidget(self.username_edit)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: bold; color: #333; margin-top: 10px;")
        form_layout.addWidget(password_label)
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter your password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """)
        form_layout.addWidget(self.password_edit)
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #5a6fd8;
            }
            QPushButton:pressed {
                background-color: #4c63d2;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        form_layout.addWidget(self.login_btn)
        
        # Demo credentials info
        demo_frame = QFrame()
        demo_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 10px;
                margin-top: 15px;
            }
        """)
        demo_layout = QVBoxLayout(demo_frame)
        
        demo_title = QLabel("Demo Credentials:")
        demo_title.setStyleSheet("font-weight: bold; color: #333;")
        demo_layout.addWidget(demo_title)
        
        demo_username = QLabel("Username: admin")
        demo_username.setStyleSheet("color: #666; font-size: 12px;")
        demo_layout.addWidget(demo_username)
        
        demo_password = QLabel("Password: admin123")
        demo_password.setStyleSheet("color: #666; font-size: 12px;")
        demo_layout.addWidget(demo_password)
        
        form_layout.addWidget(demo_frame)
        
        # Add form to main layout
        layout.addWidget(form_frame, alignment=Qt.AlignCenter)
        
        # Connect Enter key to login
        self.username_edit.returnPressed.connect(self.handle_login)
        self.password_edit.returnPressed.connect(self.handle_login)
        
        # Set initial focus
        self.username_edit.setFocus()
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both username and password.")
            return
        
        # Disable login button during request
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")
        
        try:
            response = self.api_client.login(username, password)
            user_data = response.get('user', {})
            self.login_successful.emit(user_data)
            
        except requests.RequestException as e:
            error_msg = self.api_client.handle_request_error(e)
            QMessageBox.critical(self, "Login Failed", f"Login failed: {error_msg}")
            
        except Exception as e:
            QMessageBox.critical(self, "Login Error", f"An unexpected error occurred: {str(e)}")
        
        finally:
            # Re-enable login button
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Login")
            self.password_edit.clear()  # Clear password for security