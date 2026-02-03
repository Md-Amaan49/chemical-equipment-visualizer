"""
File upload widget for desktop application
"""

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFileDialog, QMessageBox, QTextEdit,
                            QProgressBar, QFrame, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
import requests


class FileUploadThread(QThread):
    """Thread for handling file upload to avoid blocking UI"""
    
    upload_finished = pyqtSignal(dict)  # Success signal
    upload_error = pyqtSignal(str)      # Error signal
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        """Run the upload in background thread"""
        try:
            response = self.api_client.upload_csv(self.file_path)
            self.upload_finished.emit(response)
        except requests.RequestException as e:
            error_msg = self.api_client.handle_request_error(e)
            self.upload_error.emit(error_msg)
        except Exception as e:
            self.upload_error.emit(str(e))


class UploadWidget(QWidget):
    """Widget for CSV file upload functionality"""
    
    dataset_uploaded = pyqtSignal(dict)  # Emitted when dataset is uploaded
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.selected_file = None
        self.upload_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Upload Equipment Data")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Upload a CSV file containing chemical equipment data with columns: "
            "Equipment Name, Type, Flowrate, Pressure, Temperature"
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # File selection area
        self.create_file_selection_area(layout)
        
        # File info area
        self.create_file_info_area(layout)
        
        # Upload controls
        self.create_upload_controls(layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Status area
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        self.status_text.hide()
        layout.addWidget(self.status_text)
        
        # Sample data format
        self.create_sample_format_area(layout)
        
        layout.addStretch()
    
    def create_file_selection_area(self, layout):
        """Create file selection drop area"""
        self.drop_frame = QFrame()
        self.drop_frame.setFrameStyle(QFrame.Box)
        self.drop_frame.setAcceptDrops(True)
        self.drop_frame.setMinimumHeight(150)
        self.drop_frame.setStyleSheet("""
            QFrame {
                border: 2px dashed #ddd;
                border-radius: 8px;
                background-color: #fafafa;
            }
            QFrame:hover {
                border-color: #667eea;
                background-color: #f8f9ff;
            }
        """)
        
        drop_layout = QVBoxLayout(self.drop_frame)
        drop_layout.setAlignment(Qt.AlignCenter)
        
        # Drop icon/text
        drop_label = QLabel("📁")
        drop_label.setAlignment(Qt.AlignCenter)
        drop_label.setStyleSheet("font-size: 48px; margin-bottom: 10px;")
        drop_layout.addWidget(drop_label)
        
        drop_text = QLabel("Drag and drop your CSV file here, or click to browse")
        drop_text.setAlignment(Qt.AlignCenter)
        drop_text.setStyleSheet("color: #666; font-size: 14px;")
        drop_layout.addWidget(drop_text)
        
        requirements_text = QLabel("Max file size: 10MB | Format: CSV")
        requirements_text.setAlignment(Qt.AlignCenter)
        requirements_text.setStyleSheet("color: #999; font-size: 12px; margin-top: 5px;")
        drop_layout.addWidget(requirements_text)
        
        # Make frame clickable
        self.drop_frame.mousePressEvent = self.browse_file
        
        layout.addWidget(self.drop_frame)
    
    def create_file_info_area(self, layout):
        """Create file information display area"""
        self.file_info_frame = QFrame()
        self.file_info_frame.setFrameStyle(QFrame.Box)
        self.file_info_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        self.file_info_frame.hide()
        
        info_layout = QVBoxLayout(self.file_info_frame)
        
        info_title = QLabel("Selected File:")
        info_title.setStyleSheet("font-weight: bold; color: #333;")
        info_layout.addWidget(info_title)
        
        self.file_name_label = QLabel()
        self.file_size_label = QLabel()
        self.file_type_label = QLabel()
        
        for label in [self.file_name_label, self.file_size_label, self.file_type_label]:
            label.setStyleSheet("color: #666; margin: 2px 0;")
            info_layout.addWidget(label)
        
        layout.addWidget(self.file_info_frame)
    
    def create_upload_controls(self, layout):
        """Create upload control buttons"""
        controls_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton("Upload and Process")
        self.upload_btn.clicked.connect(self.handle_upload)
        self.upload_btn.setEnabled(False)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #5a6fd8;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        controls_layout.addWidget(self.upload_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_selection)
        self.clear_btn.setEnabled(False)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #5a6268;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        controls_layout.addWidget(self.clear_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
    
    def create_sample_format_area(self, layout):
        """Create sample data format display"""
        sample_frame = QFrame()
        sample_frame.setFrameStyle(QFrame.Box)
        sample_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 15px;
            }
        """)
        
        sample_layout = QVBoxLayout(sample_frame)
        
        sample_title = QLabel("Sample Data Format:")
        sample_title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 10px;")
        sample_layout.addWidget(sample_title)
        
        # Create sample table
        sample_table = QTableWidget(2, 5)
        sample_table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        
        # Add sample data
        sample_data = [
            ["Pump-001", "Pump", "45.2", "12.5", "298.15"],
            ["Valve-001", "Valve", "0.0", "15.2", "295.0"]
        ]
        
        for row, row_data in enumerate(sample_data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemIsEnabled)  # Make read-only
                sample_table.setItem(row, col, item)
        
        sample_table.resizeColumnsToContents()
        sample_table.setMaximumHeight(120)
        sample_layout.addWidget(sample_table)
        
        layout.addWidget(sample_frame)
    
    def browse_file(self, event=None):
        """Open file browser dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            self.select_file(file_path)
    
    def select_file(self, file_path):
        """Handle file selection"""
        if not file_path.lower().endswith('.csv'):
            QMessageBox.warning(self, "Invalid File", "Please select a CSV file.")
            return
        
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            QMessageBox.warning(self, "File Too Large", "File size must be less than 10MB.")
            return
        
        self.selected_file = file_path
        
        # Update file info display
        file_name = os.path.basename(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        self.file_name_label.setText(f"Name: {file_name}")
        self.file_size_label.setText(f"Size: {file_size_mb:.2f} MB")
        self.file_type_label.setText("Type: CSV")
        
        self.file_info_frame.show()
        self.upload_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
    
    def clear_selection(self):
        """Clear file selection"""
        self.selected_file = None
        self.file_info_frame.hide()
        self.upload_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.status_text.hide()
        self.progress_bar.hide()
    
    def handle_upload(self):
        """Handle file upload"""
        if not self.selected_file:
            QMessageBox.warning(self, "No File Selected", "Please select a file first.")
            return
        
        # Show progress and disable controls
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.upload_btn.setEnabled(False)
        self.upload_btn.setText("Uploading...")
        
        # Start upload thread
        self.upload_thread = FileUploadThread(self.api_client, self.selected_file)
        self.upload_thread.upload_finished.connect(self.on_upload_success)
        self.upload_thread.upload_error.connect(self.on_upload_error)
        self.upload_thread.start()
    
    @pyqtSlot(dict)
    def on_upload_success(self, response):
        """Handle successful upload"""
        self.progress_bar.hide()
        self.upload_btn.setEnabled(True)
        self.upload_btn.setText("Upload and Process")
        
        # Show success message
        message = f"File uploaded successfully!\n{response.get('record_count', 0)} records processed."
        self.status_text.setPlainText(message)
        self.status_text.setStyleSheet("background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;")
        self.status_text.show()
        
        # Emit signal with dataset info
        dataset_info = {
            'id': response.get('dataset_id'),
            'filename': response.get('filename'),
            'record_count': response.get('record_count'),
            'summary': response.get('summary', {})
        }
        self.dataset_uploaded.emit(dataset_info)
        
        # Clear selection
        self.clear_selection()
    
    @pyqtSlot(str)
    def on_upload_error(self, error_message):
        """Handle upload error"""
        self.progress_bar.hide()
        self.upload_btn.setEnabled(True)
        self.upload_btn.setText("Upload and Process")
        
        # Show error message
        self.status_text.setPlainText(f"Upload failed: {error_message}")
        self.status_text.setStyleSheet("background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;")
        self.status_text.show()
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.select_file(files[0])