#!/usr/bin/env python3
"""
Chemical Equipment Parameter Visualizer - Desktop Application
PyQt5-based desktop interface for the hybrid application
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTabWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

# Import custom widgets
from widgets.login_widget import LoginWidget
from widgets.upload_widget import UploadWidget
from widgets.visualization_widget import VisualizationWidget
from widgets.history_widget import HistoryWidget
from services.api_client import APIClient


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.user = None
        self.current_dataset = None
        
        self.init_ui()
        self.show_login()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application icon (if available)
        try:
            self.setWindowIcon(QIcon('assets/icon.png'))
        except:
            pass
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create header
        self.create_header()
        
        # Create tab widget (initially hidden)
        self.create_tabs()
        
        # Apply styles
        self.apply_styles()
    
    def create_header(self):
        """Create application header"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Title
        title_label = QLabel("Chemical Equipment Parameter Visualizer")
        title_label.setObjectName("title")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # User info (initially hidden)
        self.user_label = QLabel()
        self.user_label.hide()
        
        # Logout button (initially hidden)
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn.hide()
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.user_label)
        header_layout.addWidget(self.logout_btn)
        
        self.main_layout.addWidget(header_widget)
    
    def create_tabs(self):
        """Create tab widget with main functionality"""
        self.tab_widget = QTabWidget()
        self.tab_widget.hide()  # Initially hidden until login
        
        # Upload tab
        self.upload_widget = UploadWidget(self.api_client)
        self.upload_widget.dataset_uploaded.connect(self.on_dataset_uploaded)
        self.tab_widget.addTab(self.upload_widget, "Upload Data")
        
        # Visualization tab
        self.visualization_widget = VisualizationWidget(self.api_client)
        self.tab_widget.addTab(self.visualization_widget, "Visualization")
        
        # History tab
        self.history_widget = HistoryWidget(self.api_client)
        self.history_widget.dataset_selected.connect(self.on_dataset_selected)
        self.tab_widget.addTab(self.history_widget, "History")
        
        self.main_layout.addWidget(self.tab_widget)
    
    def show_login(self):
        """Show login widget"""
        self.login_widget = LoginWidget(self.api_client)
        self.login_widget.login_successful.connect(self.on_login_successful)
        
        # Clear main layout and add login widget
        for i in reversed(range(self.main_layout.count())):
            child = self.main_layout.itemAt(i).widget()
            if child != self.central_widget.children()[0]:  # Keep header
                child.hide()
        
        self.main_layout.addWidget(self.login_widget)
    
    def on_login_successful(self, user_data):
        """Handle successful login"""
        self.user = user_data
        self.user_label.setText(f"Welcome, {user_data['username']}")
        self.user_label.show()
        self.logout_btn.show()
        
        # Hide login widget and show tabs
        self.login_widget.hide()
        self.tab_widget.show()
        
        # Load initial data
        self.history_widget.load_history()
    
    def on_dataset_uploaded(self, dataset_data):
        """Handle dataset upload"""
        self.current_dataset = dataset_data
        self.visualization_widget.load_dataset(dataset_data['id'])
        self.tab_widget.setCurrentIndex(1)  # Switch to visualization tab
        self.history_widget.load_history()  # Refresh history
    
    def on_dataset_selected(self, dataset_data):
        """Handle dataset selection from history"""
        self.current_dataset = dataset_data
        self.visualization_widget.load_dataset(dataset_data['id'])
        self.tab_widget.setCurrentIndex(1)  # Switch to visualization tab
    
    def logout(self):
        """Handle logout"""
        try:
            self.api_client.logout()
        except Exception as e:
            print(f"Logout error: {e}")
        
        self.user = None
        self.current_dataset = None
        
        # Hide user info and tabs
        self.user_label.hide()
        self.logout_btn.hide()
        self.tab_widget.hide()
        
        # Show login again
        self.show_login()
    
    def apply_styles(self):
        """Apply application styles"""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QLabel#title {
            color: #333;
            padding: 10px;
        }
        
        QTabWidget::pane {
            border: 1px solid #ddd;
            background-color: white;
        }
        
        QTabBar::tab {
            background-color: #f8f9fa;
            padding: 8px 16px;
            margin-right: 2px;
            border: 1px solid #ddd;
            border-bottom: none;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: 1px solid white;
        }
        
        QPushButton {
            background-color: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #5a6fd8;
        }
        
        QPushButton:pressed {
            background-color: #4c63d2;
        }
        """
        self.setStyleSheet(style)
    
    def closeEvent(self, event):
        """Handle application close"""
        reply = QMessageBox.question(
            self, 'Exit Application',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setApplicationVersion("1.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()