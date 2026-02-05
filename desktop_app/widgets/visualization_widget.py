"""
Data visualization widget using matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QMessageBox, QFrame, QButtonGroup, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont
import requests


class AnalyticsLoadThread(QThread):
    """Thread for loading analytics data"""
    
    data_loaded = pyqtSignal(dict)  # Success signal
    load_error = pyqtSignal(str)    # Error signal
    
    def __init__(self, api_client, dataset_id):
        super().__init__()
        self.api_client = api_client
        self.dataset_id = dataset_id
    
    def run(self):
        """Load analytics data in background"""
        try:
            response = self.api_client.get_analytics(self.dataset_id)
            self.data_loaded.emit(response)
        except requests.RequestException as e:
            error_msg = self.api_client.handle_request_error(e)
            self.load_error.emit(error_msg)
        except Exception as e:
            self.load_error.emit(str(e))


class MatplotlibCanvas(FigureCanvas):
    """Matplotlib canvas for embedding plots in PyQt5"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        
        # Configure matplotlib style
        plt.style.use('default')
        self.fig.patch.set_facecolor('white')


class VisualizationWidget(QWidget):
    """Widget for data visualization using matplotlib"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.analytics_data = None
        self.current_chart = 'averages'
        self.load_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Dataset info area
        self.create_dataset_info_area(layout)
        
        # Summary cards
        self.create_summary_cards(layout)
        
        # Chart controls
        self.create_chart_controls(layout)
        
        # Chart area
        self.create_chart_area(layout)
        
        # Equipment table
        self.create_equipment_table(layout)
        
        # Initially show empty state
        self.show_empty_state()
    
    def create_dataset_info_area(self, layout):
        """Create dataset information display"""
        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 15px;
                margin-bottom: 10px;
            }
        """)
        
        info_layout = QVBoxLayout(self.info_frame)
        
        self.dataset_title = QLabel("No dataset selected")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.dataset_title.setFont(title_font)
        self.dataset_title.setStyleSheet("color: #333;")
        info_layout.addWidget(self.dataset_title)
        
        self.dataset_metadata = QLabel()
        self.dataset_metadata.setStyleSheet("color: #666; margin-top: 5px;")
        info_layout.addWidget(self.dataset_metadata)
        
        layout.addWidget(self.info_frame)
    
    def create_summary_cards(self, layout):
        """Create summary statistics cards"""
        self.summary_frame = QFrame()
        summary_layout = QHBoxLayout(self.summary_frame)
        
        # Create summary cards
        self.total_card = self.create_summary_card("Total Equipment", "0")
        self.flowrate_card = self.create_summary_card("Avg Flowrate", "0.00")
        self.pressure_card = self.create_summary_card("Avg Pressure", "0.00")
        self.temperature_card = self.create_summary_card("Avg Temperature", "0.00")
        
        for card in [self.total_card, self.flowrate_card, self.pressure_card, self.temperature_card]:
            summary_layout.addWidget(card)
        
        layout.addWidget(self.summary_frame)
    
    def create_summary_card(self, title, value):
        """Create individual summary card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-left: 4px solid #667eea;
                border-radius: 4px;
                padding: 15px;
                margin: 5px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 12px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #333; font-size: 24px; font-weight: bold; margin-top: 5px;")
        value_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(value_label)
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def create_chart_controls(self, layout):
        """Create chart type selection controls"""
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        
        self.chart_button_group = QButtonGroup()
        
        self.averages_btn = QPushButton("Parameter Averages")
        self.averages_btn.setCheckable(True)
        self.averages_btn.setChecked(True)
        self.averages_btn.clicked.connect(lambda: self.switch_chart('averages'))
        
        self.distribution_btn = QPushButton("Equipment Distribution")
        self.distribution_btn.setCheckable(True)
        self.distribution_btn.clicked.connect(lambda: self.switch_chart('distribution'))
        
        self.chart_button_group.addButton(self.averages_btn)
        self.chart_button_group.addButton(self.distribution_btn)
        
        for btn in [self.averages_btn, self.distribution_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #ddd;
                    padding: 8px 16px;
                    border-radius: 4px;
                    margin-right: 5px;
                }
                QPushButton:checked {
                    background-color: #667eea;
                    color: white;
                    border-color: #667eea;
                }
                QPushButton:hover:!checked {
                    background-color: #f8f9fa;
                }
            """)
            controls_layout.addWidget(btn)
        
        controls_layout.addStretch()
        layout.addWidget(controls_frame)
    
    def create_chart_area(self, layout):
        """Create matplotlib chart area"""
        self.chart_frame = QFrame()
        self.chart_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        
        chart_layout = QVBoxLayout(self.chart_frame)
        
        # Create matplotlib canvas
        self.canvas = MatplotlibCanvas(self.chart_frame, width=8, height=5)
        chart_layout.addWidget(self.canvas)
        
        layout.addWidget(self.chart_frame)
    
    def create_equipment_table(self, layout):
        """Create equipment records table"""
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 10px;
                margin-top: 10px;
            }
        """)
        
        table_layout = QVBoxLayout(table_frame)
        
        table_title = QLabel("Equipment Records")
        table_title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 10px;")
        table_layout.addWidget(table_title)
        
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(5)
        self.equipment_table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        
        # Style the table
        self.equipment_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e9ecef;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 4px;
                border: 1px solid #e9ecef;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
        """)
        
        table_layout.addWidget(self.equipment_table)
        layout.addWidget(table_frame)
    
    def show_empty_state(self):
        """Show empty state when no dataset is loaded"""
        self.dataset_title.setText("No dataset selected")
        self.dataset_metadata.setText("Upload a CSV file or select from history to view analytics")
        
        # Clear summary cards
        for card in [self.total_card, self.flowrate_card, self.pressure_card, self.temperature_card]:
            card.value_label.setText("0")
        
        # Clear chart
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'No data to display\nUpload a CSV file to get started', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=14, color='#666')
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
        
        # Clear table
        self.equipment_table.setRowCount(0)
    
    def load_dataset(self, dataset_id):
        """Load dataset analytics"""
        if self.load_thread and self.load_thread.isRunning():
            self.load_thread.quit()
            self.load_thread.wait()
        
        self.load_thread = AnalyticsLoadThread(self.api_client, dataset_id)
        self.load_thread.data_loaded.connect(self.on_data_loaded)
        self.load_thread.load_error.connect(self.on_load_error)
        self.load_thread.start()
        
        # Show loading state
        self.dataset_title.setText("Loading dataset...")
        self.dataset_metadata.setText("Please wait while we load the analytics data")
    
    @pyqtSlot(dict)
    def on_data_loaded(self, data):
        """Handle successful data loading"""
        self.analytics_data = data
        self.update_display()
    
    @pyqtSlot(str)
    def on_load_error(self, error_message):
        """Handle data loading error"""
        QMessageBox.critical(self, "Load Error", f"Failed to load analytics: {error_message}")
        self.show_empty_state()
    
    def update_display(self):
        """Update all display elements with loaded data"""
        if not self.analytics_data:
            return
        
        summary = self.analytics_data['summary']
        metadata = self.analytics_data['metadata']
        equipment_records = self.analytics_data['equipment_records']
        
        # Update dataset info
        self.dataset_title.setText(f"Dataset Analysis: {metadata['filename']}")
        self.dataset_metadata.setText(
            f"Records: {metadata['record_count']} | "
            f"Uploaded: {metadata['upload_time'][:10]}"
        )
        
        # Update summary cards
        self.total_card.value_label.setText(str(summary['total_count']))
        self.flowrate_card.value_label.setText(f"{summary['averages']['flowrate']:.2f}")
        self.pressure_card.value_label.setText(f"{summary['averages']['pressure']:.2f}")
        self.temperature_card.value_label.setText(f"{summary['averages']['temperature']:.2f}")
        
        # Update chart
        self.update_chart()
        
        # Update table
        self.update_equipment_table(equipment_records)
    
    def update_chart(self):
        """Update the matplotlib chart"""
        if not self.analytics_data:
            return
        
        summary = self.analytics_data['summary']
        
        # Clear previous plot
        self.canvas.fig.clear()
        
        if self.current_chart == 'averages':
            self.plot_averages_chart(summary)
        else:
            self.plot_distribution_chart(summary)
        
        self.canvas.draw()
    
    def plot_averages_chart(self, summary):
        """Plot parameter averages bar chart"""
        ax = self.canvas.fig.add_subplot(111)
        
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            summary['averages']['flowrate'],
            summary['averages']['pressure'],
            summary['averages']['temperature']
        ]
        colors = ['#3498db', '#e74c3c', '#f39c12']
        
        bars = ax.bar(parameters, values, color=colors, alpha=0.7)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Average Parameter Values', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel('Value')
        ax.grid(True, alpha=0.3)
        
        # Improve layout
        self.canvas.fig.tight_layout()
    
    def plot_distribution_chart(self, summary):
        """Plot equipment type distribution pie chart"""
        ax = self.canvas.fig.add_subplot(111)
        
        types = list(summary['type_distribution'].keys())
        counts = list(summary['type_distribution'].values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(types)))
        
        wedges, texts, autotexts = ax.pie(counts, labels=types, colors=colors, 
                                         autopct='%1.1f%%', startangle=90)
        
        # Improve text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=20)
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        
        # Improve layout
        self.canvas.fig.tight_layout()
    
    def update_equipment_table(self, equipment_records):
        """Update equipment records table"""
        self.equipment_table.setRowCount(len(equipment_records))
        
        for row, record in enumerate(equipment_records):
            items = [
                record['equipment_name'],
                record['equipment_type'],
                f"{record['flowrate']:.2f}",
                f"{record['pressure']:.2f}",
                f"{record['temperature']:.2f}"
            ]
            
            for col, item_text in enumerate(items):
                item = QTableWidgetItem(item_text)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # Read-only
                self.equipment_table.setItem(row, col, item)
        
        # Resize columns to content
        self.equipment_table.resizeColumnsToContents()
    
    def switch_chart(self, chart_type):
        """Switch between chart types"""
        self.current_chart = chart_type
        self.update_chart()