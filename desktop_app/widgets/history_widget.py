"""
History widget for managing dataset history
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QMessageBox, QFrame, QScrollArea,
                            QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont
import requests


class HistoryLoadThread(QThread):
    """Thread for loading history data"""
    
    data_loaded = pyqtSignal(dict)  # Success signal
    load_error = pyqtSignal(str)    # Error signal
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
    
    def run(self):
        """Load history data in background"""
        try:
            response = self.api_client.get_history()
            self.data_loaded.emit(response)
        except requests.RequestException as e:
            error_msg = self.api_client.handle_request_error(e)
            self.load_error.emit(error_msg)
        except Exception as e:
            self.load_error.emit(str(e))


class DeleteDatasetThread(QThread):
    """Thread for deleting dataset"""
    
    delete_finished = pyqtSignal(int)  # Success signal with dataset_id
    delete_error = pyqtSignal(str)     # Error signal
    
    def __init__(self, api_client, dataset_id):
        super().__init__()
        self.api_client = api_client
        self.dataset_id = dataset_id
    
    def run(self):
        """Delete dataset in background"""
        try:
            self.api_client.delete_dataset(self.dataset_id)
            self.delete_finished.emit(self.dataset_id)
        except requests.RequestException as e:
            error_msg = self.api_client.handle_request_error(e)
            self.delete_error.emit(error_msg)
        except Exception as e:
            self.delete_error.emit(str(e))


class DatasetCard(QFrame):
    """Individual dataset card widget"""
    
    dataset_selected = pyqtSignal(dict)  # Emitted when dataset is selected
    dataset_deleted = pyqtSignal(int)    # Emitted when dataset is deleted
    
    def __init__(self, dataset_data, api_client):
        super().__init__()
        self.dataset_data = dataset_data
        self.api_client = api_client
        self.delete_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the card UI"""
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }
            QFrame:hover {
                background-color: #f0f0f0;
                border-color: #667eea;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Header with filename and actions
        header_layout = QHBoxLayout()
        
        filename_label = QLabel(self.dataset_data['filename'])
        filename_font = QFont()
        filename_font.setPointSize(12)
        filename_font.setBold(True)
        filename_label.setFont(filename_font)
        filename_label.setStyleSheet("color: #333;")
        header_layout.addWidget(filename_label)
        
        header_layout.addStretch()
        
        # Action buttons
        view_btn = QPushButton("📊")
        view_btn.setToolTip("View this dataset")
        view_btn.clicked.connect(self.select_dataset)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #bbdefb;
            }
        """)
        header_layout.addWidget(view_btn)
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Delete this dataset")
        delete_btn.clicked.connect(self.delete_dataset)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffebee;
                border: 1px solid #ffcdd2;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ffcdd2;
            }
        """)
        header_layout.addWidget(delete_btn)
        
        layout.addLayout(header_layout)
        
        # Dataset info
        info_layout = QVBoxLayout()
        
        record_count_label = QLabel(f"Records: {self.dataset_data['record_count']}")
        record_count_label.setStyleSheet("color: #666; margin: 2px 0;")
        info_layout.addWidget(record_count_label)
        
        upload_time = self.dataset_data['upload_time'][:10]  # Just the date part
        upload_label = QLabel(f"Uploaded: {upload_time}")
        upload_label.setStyleSheet("color: #666; margin: 2px 0;")
        info_layout.addWidget(upload_label)
        
        layout.addLayout(info_layout)
        
        # Summary statistics
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 10px;
                margin-top: 10px;
            }
        """)
        
        summary_layout = QVBoxLayout(summary_frame)
        
        summary_title = QLabel("Summary Statistics")
        summary_title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 5px;")
        summary_layout.addWidget(summary_title)
        
        # Statistics grid
        stats_grid = QGridLayout()
        
        summary = self.dataset_data['summary']
        stats_data = [
            ("Avg Flowrate", f"{summary['avg_flowrate']:.2f}"),
            ("Avg Pressure", f"{summary['avg_pressure']:.2f}"),
            ("Avg Temperature", f"{summary['avg_temperature']:.2f}")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #666; font-size: 11px;")
            value_widget = QLabel(value)
            value_widget.setStyleSheet("color: #333; font-weight: bold; font-size: 11px;")
            
            row = i // 2
            col = (i % 2) * 2
            stats_grid.addWidget(label_widget, row, col)
            stats_grid.addWidget(value_widget, row, col + 1)
        
        summary_layout.addLayout(stats_grid)
        
        # Equipment types
        if 'type_distribution' in summary:
            types_label = QLabel("Equipment Types")
            types_label.setStyleSheet("font-weight: bold; color: #333; margin-top: 10px; margin-bottom: 5px;")
            summary_layout.addWidget(types_label)
            
            types_layout = QHBoxLayout()
            for eq_type, count in summary['type_distribution'].items():
                type_badge = QLabel(f"{eq_type}: {count}")
                type_badge.setStyleSheet("""
                    QLabel {
                        background-color: #667eea;
                        color: white;
                        padding: 2px 6px;
                        border-radius: 10px;
                        font-size: 10px;
                        margin: 1px;
                    }
                """)
                types_layout.addWidget(type_badge)
            
            types_layout.addStretch()
            summary_layout.addLayout(types_layout)
        
        layout.addWidget(summary_frame)
    
    def select_dataset(self):
        """Handle dataset selection"""
        self.dataset_selected.emit(self.dataset_data)
    
    def delete_dataset(self):
        """Handle dataset deletion"""
        reply = QMessageBox.question(
            self, 'Delete Dataset',
            f'Are you sure you want to delete "{self.dataset_data["filename"]}"?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.delete_thread and self.delete_thread.isRunning():
                return
            
            self.delete_thread = DeleteDatasetThread(self.api_client, self.dataset_data['id'])
            self.delete_thread.delete_finished.connect(self.on_delete_success)
            self.delete_thread.delete_error.connect(self.on_delete_error)
            self.delete_thread.start()
    
    @pyqtSlot(int)
    def on_delete_success(self, dataset_id):
        """Handle successful deletion"""
        self.dataset_deleted.emit(dataset_id)
    
    @pyqtSlot(str)
    def on_delete_error(self, error_message):
        """Handle deletion error"""
        QMessageBox.critical(self, "Delete Error", f"Failed to delete dataset: {error_message}")


class HistoryWidget(QWidget):
    """Widget for managing dataset history"""
    
    dataset_selected = pyqtSignal(dict)  # Emitted when dataset is selected
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.datasets = []
        self.dataset_cards = []
        self.load_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Dataset History")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Description
        self.desc_label = QLabel("Your recent datasets")
        self.desc_label.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(self.desc_label)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_history)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #5a6fd8;
            }
        """)
        layout.addWidget(refresh_btn, alignment=Qt.AlignLeft)
        
        # Scroll area for dataset cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(scroll_area)
        
        # Initially show empty state
        self.show_empty_state()
    
    def show_empty_state(self):
        """Show empty state when no datasets are available"""
        self.clear_cards()
        
        empty_label = QLabel("No datasets uploaded yet.\nUpload your first CSV file to get started!")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 14px;
                padding: 40px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
        """)
        self.scroll_layout.addWidget(empty_label)
    
    def show_loading_state(self):
        """Show loading state"""
        self.clear_cards()
        
        loading_label = QLabel("Loading history...")
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 14px;
                padding: 40px;
            }
        """)
        self.scroll_layout.addWidget(loading_label)
    
    def clear_cards(self):
        """Clear all dataset cards"""
        for card in self.dataset_cards:
            card.deleteLater()
        self.dataset_cards.clear()
        
        # Clear scroll layout
        for i in reversed(range(self.scroll_layout.count())):
            child = self.scroll_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
    
    def load_history(self):
        """Load dataset history"""
        if self.load_thread and self.load_thread.isRunning():
            self.load_thread.quit()
            self.load_thread.wait()
        
        self.show_loading_state()
        
        self.load_thread = HistoryLoadThread(self.api_client)
        self.load_thread.data_loaded.connect(self.on_data_loaded)
        self.load_thread.load_error.connect(self.on_load_error)
        self.load_thread.start()
    
    @pyqtSlot(dict)
    def on_data_loaded(self, data):
        """Handle successful data loading"""
        self.datasets = data.get('datasets', [])
        self.update_display()
    
    @pyqtSlot(str)
    def on_load_error(self, error_message):
        """Handle data loading error"""
        QMessageBox.critical(self, "Load Error", f"Failed to load history: {error_message}")
        self.show_empty_state()
    
    def update_display(self):
        """Update the display with loaded datasets"""
        self.clear_cards()
        
        if not self.datasets:
            self.show_empty_state()
            return
        
        self.desc_label.setText(f"Your last {len(self.datasets)} uploaded datasets")
        
        # Create dataset cards
        for dataset in self.datasets:
            card = DatasetCard(dataset, self.api_client)
            card.dataset_selected.connect(self.dataset_selected.emit)
            card.dataset_deleted.connect(self.on_dataset_deleted)
            
            self.dataset_cards.append(card)
            self.scroll_layout.addWidget(card)
        
        # Add stretch to push cards to top
        self.scroll_layout.addStretch()
    
    @pyqtSlot(int)
    def on_dataset_deleted(self, dataset_id):
        """Handle dataset deletion"""
        # Remove from datasets list
        self.datasets = [d for d in self.datasets if d['id'] != dataset_id]
        
        # Update display
        self.update_display()
        
        QMessageBox.information(self, "Dataset Deleted", "Dataset deleted successfully.")