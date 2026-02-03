#!/usr/bin/env python
"""
Integration test script for Chemical Equipment Parameter Visualizer
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_equipment_visualizer.settings')
django.setup()

from django.contrib.auth.models import User
from analytics.models import Dataset, EquipmentRecord
from analytics.analytics_engine import AnalyticsEngine
from analytics.report_generator import ReportGenerator


def test_integration():
    """Test the complete workflow"""
    print("🧪 Starting Integration Tests...")
    
    # Test 1: User creation
    print("\n1. Testing User Management...")
    try:
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        print("✅ User management working")
    except Exception as e:
        print(f"❌ User management failed: {e}")
        return False
    
    # Test 2: Sample data processing
    print("\n2. Testing Sample Data Processing...")
    try:
        sample_file = 'sample_equipment_data.csv'
        if os.path.exists(sample_file):
            dataset, summary = AnalyticsEngine.process_csv(
                sample_file, user, 'test_sample.csv'
            )
            print(f"✅ Sample data processed: {summary['total_count']} records")
            print(f"   Equipment types: {list(summary['type_distribution'].keys())}")
        else:
            print("❌ Sample data file not found")
            return False
    except Exception as e:
        print(f"❌ Sample data processing failed: {e}")
        return False
    
    # Test 3: Analytics calculations
    print("\n3. Testing Analytics Calculations...")
    try:
        avg_flow = dataset.avg_flowrate
        avg_pressure = dataset.avg_pressure
        avg_temp = dataset.avg_temperature
        print(f"✅ Analytics calculated:")
        print(f"   Avg Flowrate: {avg_flow:.2f}")
        print(f"   Avg Pressure: {avg_pressure:.2f}")
        print(f"   Avg Temperature: {avg_temp:.2f}")
    except Exception as e:
        print(f"❌ Analytics calculation failed: {e}")
        return False
    
    # Test 4: Database storage
    print("\n4. Testing Database Storage...")
    try:
        equipment_count = EquipmentRecord.objects.filter(dataset=dataset).count()
        print(f"✅ Database storage working: {equipment_count} equipment records stored")
    except Exception as e:
        print(f"❌ Database storage failed: {e}")
        return False
    
    # Test 5: History management
    print("\n5. Testing History Management...")
    try:
        user_datasets = Dataset.objects.filter(user=user).count()
        print(f"✅ History management working: {user_datasets} datasets for user")
    except Exception as e:
        print(f"❌ History management failed: {e}")
        return False
    
    # Test 6: PDF report generation
    print("\n6. Testing PDF Report Generation...")
    try:
        report_generator = ReportGenerator()
        report_buffer = report_generator.generate_report_buffer(dataset.id)
        report_size = len(report_buffer.getvalue())
        print(f"✅ PDF report generated: {report_size} bytes")
    except Exception as e:
        print(f"❌ PDF report generation failed: {e}")
        return False
    
    # Test 7: Data validation
    print("\n7. Testing Data Validation...")
    try:
        import pandas as pd
        df = pd.read_csv(sample_file)
        is_valid, error_msg = AnalyticsEngine.validate_equipment_data(df)
        if is_valid:
            print("✅ Data validation working")
        else:
            print(f"❌ Data validation failed: {error_msg}")
            return False
    except Exception as e:
        print(f"❌ Data validation test failed: {e}")
        return False
    
    print("\n🎉 All Integration Tests Passed!")
    print("\n📊 System Summary:")
    print(f"   - Total Datasets: {Dataset.objects.count()}")
    print(f"   - Total Equipment Records: {EquipmentRecord.objects.count()}")
    print(f"   - Total Users: {User.objects.count()}")
    
    return True


if __name__ == '__main__':
    success = test_integration()
    sys.exit(0 if success else 1)