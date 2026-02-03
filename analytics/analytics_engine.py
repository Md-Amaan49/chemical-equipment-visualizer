import pandas as pd
from typing import Dict, Any, Tuple
from django.contrib.auth.models import User
from .models import Dataset, EquipmentRecord


class AnalyticsEngine:
    """
    Analytics engine for processing chemical equipment data
    """
    
    @staticmethod
    def validate_equipment_data(df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate equipment data structure and content
        
        Args:
            df: DataFrame containing equipment data
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        
        # Check required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Check for empty data
        if df.empty:
            return False, "Dataset is empty"
        
        # Check for null values in critical columns
        for col in ['Flowrate', 'Pressure', 'Temperature']:
            if df[col].isnull().any():
                return False, f"Null values found in {col} column"
        
        # Validate numeric ranges (basic sanity checks)
        if (df['Flowrate'] < 0).any():
            return False, "Negative flowrate values found"
        
        if (df['Pressure'] < 0).any():
            return False, "Negative pressure values found"
        
        if (df['Temperature'] < -273.15).any():  # Absolute zero check
            return False, "Temperature values below absolute zero found"
        
        return True, ""
    
    @staticmethod
    def calculate_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate summary statistics for equipment data
        
        Args:
            df: DataFrame containing equipment data
            
        Returns:
            Dictionary containing summary statistics
        """
        # Basic counts
        total_count = len(df)
        
        # Average values for numeric parameters
        avg_flowrate = float(df['Flowrate'].mean())
        avg_pressure = float(df['Pressure'].mean())
        avg_temperature = float(df['Temperature'].mean())
        
        # Equipment type distribution
        type_distribution = df['Type'].value_counts().to_dict()
        
        # Additional statistics
        flowrate_stats = {
            'min': float(df['Flowrate'].min()),
            'max': float(df['Flowrate'].max()),
            'std': float(df['Flowrate'].std())
        }
        
        pressure_stats = {
            'min': float(df['Pressure'].min()),
            'max': float(df['Pressure'].max()),
            'std': float(df['Pressure'].std())
        }
        
        temperature_stats = {
            'min': float(df['Temperature'].min()),
            'max': float(df['Temperature'].max()),
            'std': float(df['Temperature'].std())
        }
        
        return {
            'total_count': total_count,
            'averages': {
                'flowrate': avg_flowrate,
                'pressure': avg_pressure,
                'temperature': avg_temperature
            },
            'type_distribution': type_distribution,
            'detailed_stats': {
                'flowrate': flowrate_stats,
                'pressure': pressure_stats,
                'temperature': temperature_stats
            }
        }
    
    @staticmethod
    def process_csv(file_path: str, user: User, filename: str) -> Tuple[Dataset, Dict[str, Any]]:
        """
        Process CSV file and store data in database
        
        Args:
            file_path: Path to the CSV file
            user: User who uploaded the file
            filename: Original filename
            
        Returns:
            Tuple of (Dataset object, summary statistics)
        """
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Validate data
        is_valid, error_message = AnalyticsEngine.validate_equipment_data(df)
        if not is_valid:
            raise ValueError(error_message)
        
        # Clean and prepare data
        df = df.dropna()  # Remove any rows with null values
        
        # Ensure proper data types
        df['Flowrate'] = pd.to_numeric(df['Flowrate'], errors='coerce')
        df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
        df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
        
        # Remove any rows that couldn't be converted to numeric
        df = df.dropna()
        
        # Calculate summary statistics
        summary = AnalyticsEngine.calculate_summary(df)
        
        # Create Dataset record
        dataset = Dataset.objects.create(
            filename=filename,
            record_count=summary['total_count'],
            user=user,
            avg_flowrate=summary['averages']['flowrate'],
            avg_pressure=summary['averages']['pressure'],
            avg_temperature=summary['averages']['temperature'],
            type_distribution=summary['type_distribution']
        )
        
        # Create EquipmentRecord entries
        equipment_records = []
        for _, row in df.iterrows():
            equipment_records.append(
                EquipmentRecord(
                    dataset=dataset,
                    equipment_name=str(row['Equipment Name']),
                    equipment_type=str(row['Type']),
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature'])
                )
            )
        
        # Bulk create for efficiency
        EquipmentRecord.objects.bulk_create(equipment_records)
        
        return dataset, summary
    
    @staticmethod
    def cleanup_old_datasets(user: User, limit: int = 5):
        """
        Remove old datasets beyond the specified limit
        
        Args:
            user: User whose datasets to clean up
            limit: Maximum number of datasets to keep
        """
        user_datasets = Dataset.objects.filter(user=user).order_by('-upload_timestamp')
        
        if user_datasets.count() > limit:
            datasets_to_delete = user_datasets[limit:]
            for dataset in datasets_to_delete:
                dataset.delete()  # This will cascade delete related EquipmentRecords