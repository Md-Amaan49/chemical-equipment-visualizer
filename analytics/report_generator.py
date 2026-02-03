import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from .models import Dataset, EquipmentRecord


class ReportGenerator:
    """
    PDF report generator for chemical equipment analytics
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
    
    def create_pie_chart(self, data_dict, title, width=400, height=300):
        """Create a pie chart for equipment type distribution"""
        drawing = Drawing(width, height)
        
        pie = Pie()
        pie.x = 50
        pie.y = 50
        pie.width = width - 100
        pie.height = height - 100
        
        # Prepare data
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        
        pie.data = values
        pie.labels = labels
        
        # Color scheme
        colors_list = [
            HexColor('#FF6B6B'), HexColor('#4ECDC4'), HexColor('#45B7D1'),
            HexColor('#96CEB4'), HexColor('#FFEAA7'), HexColor('#DDA0DD'),
            HexColor('#98D8C8'), HexColor('#F7DC6F')
        ]
        
        for i, color in enumerate(colors_list[:len(values)]):
            pie.slices[i].fillColor = color
        
        drawing.add(pie)
        return drawing
    
    def create_bar_chart_image(self, data_dict, title, filename):
        """Create a bar chart using matplotlib and save as image"""
        plt.figure(figsize=(10, 6))
        
        equipment_types = list(data_dict.keys())
        counts = list(data_dict.values())
        
        bars = plt.bar(equipment_types, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Equipment Type', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def generate_pdf_report(self, dataset_id, output_path=None):
        """
        Generate a comprehensive PDF report for a dataset
        
        Args:
            dataset_id: ID of the dataset to generate report for
            output_path: Optional path to save the PDF file
            
        Returns:
            Path to the generated PDF file
        """
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            equipment_records = EquipmentRecord.objects.filter(dataset=dataset)
            
            # Create output path if not provided
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"equipment_report_{dataset.id}_{timestamp}.pdf"
                output_path = os.path.join('media', 'reports', filename)
                
                # Create reports directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # Title
            title = Paragraph(
                f"Chemical Equipment Analysis Report<br/>{dataset.filename}",
                self.title_style
            )
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Report metadata
            metadata_data = [
                ['Report Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                ['Dataset File:', dataset.filename],
                ['Upload Date:', dataset.upload_timestamp.strftime("%Y-%m-%d %H:%M:%S")],
                ['Total Equipment Count:', str(dataset.record_count)],
                ['User:', dataset.user.username]
            ]
            
            metadata_table = Table(metadata_data, colWidths=[2*inch, 3*inch])
            metadata_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(metadata_table)
            story.append(Spacer(1, 30))
            
            # Summary Statistics
            story.append(Paragraph("Summary Statistics", self.heading_style))
            
            summary_data = [
                ['Parameter', 'Average Value', 'Unit'],
                ['Flowrate', f"{dataset.avg_flowrate:.2f}", 'L/min'],
                ['Pressure', f"{dataset.avg_pressure:.2f}", 'bar'],
                ['Temperature', f"{dataset.avg_temperature:.2f}", 'K']
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 30))
            
            # Equipment Type Distribution
            story.append(Paragraph("Equipment Type Distribution", self.heading_style))
            
            # Create pie chart
            pie_chart = self.create_pie_chart(
                dataset.type_distribution,
                "Equipment Type Distribution"
            )
            story.append(pie_chart)
            story.append(Spacer(1, 20))
            
            # Distribution table
            dist_data = [['Equipment Type', 'Count', 'Percentage']]
            total_count = sum(dataset.type_distribution.values())
            
            for eq_type, count in dataset.type_distribution.items():
                percentage = (count / total_count) * 100
                dist_data.append([eq_type, str(count), f"{percentage:.1f}%"])
            
            dist_table = Table(dist_data, colWidths=[2*inch, 1*inch, 1*inch])
            dist_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(dist_table)
            story.append(Spacer(1, 30))
            
            # Equipment Details (first 20 records to avoid overly long reports)
            story.append(Paragraph("Equipment Details (Sample)", self.heading_style))
            
            equipment_data = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
            
            for record in equipment_records[:20]:  # Limit to first 20 records
                equipment_data.append([
                    record.equipment_name,
                    record.equipment_type,
                    f"{record.flowrate:.1f}",
                    f"{record.pressure:.1f}",
                    f"{record.temperature:.1f}"
                ])
            
            if len(equipment_records) > 20:
                equipment_data.append(['...', '...', '...', '...', '...'])
                equipment_data.append([
                    f"Total: {len(equipment_records)} records",
                    '', '', '', ''
                ])
            
            equipment_table = Table(equipment_data, colWidths=[1.5*inch, 1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            equipment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(equipment_table)
            
            # Build PDF
            doc.build(story)
            
            return output_path
            
        except Dataset.DoesNotExist:
            raise ValueError(f"Dataset with ID {dataset_id} not found")
        except Exception as e:
            raise Exception(f"Error generating PDF report: {str(e)}")
    
    def generate_report_buffer(self, dataset_id):
        """
        Generate PDF report and return as BytesIO buffer for HTTP response
        
        Args:
            dataset_id: ID of the dataset to generate report for
            
        Returns:
            BytesIO buffer containing the PDF data
        """
        buffer = io.BytesIO()
        
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            equipment_records = EquipmentRecord.objects.filter(dataset=dataset)
            
            # Create PDF document in memory
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []
            
            # Title
            title = Paragraph(
                f"Chemical Equipment Analysis Report<br/>{dataset.filename}",
                self.title_style
            )
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Report metadata
            metadata_data = [
                ['Report Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                ['Dataset File:', dataset.filename],
                ['Upload Date:', dataset.upload_timestamp.strftime("%Y-%m-%d %H:%M:%S")],
                ['Total Equipment Count:', str(dataset.record_count)],
                ['User:', dataset.user.username]
            ]
            
            metadata_table = Table(metadata_data, colWidths=[2*inch, 3*inch])
            metadata_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(metadata_table)
            story.append(Spacer(1, 30))
            
            # Summary Statistics
            story.append(Paragraph("Summary Statistics", self.heading_style))
            
            summary_data = [
                ['Parameter', 'Average Value', 'Unit'],
                ['Flowrate', f"{dataset.avg_flowrate:.2f}", 'L/min'],
                ['Pressure', f"{dataset.avg_pressure:.2f}", 'bar'],
                ['Temperature', f"{dataset.avg_temperature:.2f}", 'K']
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 30))
            
            # Equipment Type Distribution
            story.append(Paragraph("Equipment Type Distribution", self.heading_style))
            
            # Create pie chart
            pie_chart = self.create_pie_chart(
                dataset.type_distribution,
                "Equipment Type Distribution"
            )
            story.append(pie_chart)
            story.append(Spacer(1, 20))
            
            # Build PDF
            doc.build(story)
            
            # Reset buffer position
            buffer.seek(0)
            return buffer
            
        except Dataset.DoesNotExist:
            raise ValueError(f"Dataset with ID {dataset_id} not found")
        except Exception as e:
            raise Exception(f"Error generating PDF report: {str(e)}")