import os
import pandas as pd
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from analytics.models import Dataset, EquipmentRecord
from analytics.analytics_engine import AnalyticsEngine
from analytics.report_generator import ReportGenerator
from .decorators import handle_api_errors


@csrf_exempt
def upload_csv(request):
    """
    Upload and process CSV file containing equipment data - using plain Django view
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    print(f"Upload request from user: {request.user.username}")
    print(f"Request method: {request.method}")
    print(f"Request content type: {request.content_type}")
    print(f"Files in request: {list(request.FILES.keys())}")
    print(f"POST data keys: {list(request.POST.keys())}")
    print(f"Request META encoding: {request.META.get('CONTENT_TYPE', 'Not set')}")
    
    if 'file' not in request.FILES:
        print("❌ No 'file' key found in request.FILES")
        print(f"Available keys in request.FILES: {list(request.FILES.keys())}")
        print(f"Raw request body length: {len(request.body) if hasattr(request, 'body') else 'No body'}")
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    uploaded_file = request.FILES['file']
    
    # Validate file extension
    if not uploaded_file.name.endswith('.csv'):
        return JsonResponse({'error': 'File must be a CSV file'}, status=400)
    
    # Validate file size (10MB limit)
    if uploaded_file.size > 10 * 1024 * 1024:
        return JsonResponse({'error': 'File size exceeds 10MB limit'}, status=400)
    
    try:
        # Save file temporarily
        file_path = default_storage.save(
            f'temp/{uploaded_file.name}', 
            ContentFile(uploaded_file.read())
        )
        full_path = default_storage.path(file_path)
        
        # Process CSV using analytics engine
        dataset, summary = AnalyticsEngine.process_csv(
            full_path, 
            request.user, 
            uploaded_file.name
        )
        
        # Clean up old datasets (keep only last 5)
        AnalyticsEngine.cleanup_old_datasets(request.user, limit=5)
        
        # Clean up temporary file
        default_storage.delete(file_path)
        
        return JsonResponse({
            'message': 'File uploaded and processed successfully',
            'dataset_id': dataset.id,
            'filename': dataset.filename,
            'record_count': dataset.record_count,
            'summary': {
                'total_count': summary['total_count'],
                'averages': summary['averages'],
                'type_distribution': summary['type_distribution']
            }
        }, status=201)
        
    except ValueError as e:
        # Clean up temporary file if it exists
        try:
            if 'file_path' in locals():
                default_storage.delete(file_path)
        except:
            pass
        
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        # Clean up temporary file if it exists
        try:
            if 'file_path' in locals():
                default_storage.delete(file_path)
        except:
            pass
        
        return JsonResponse({'error': f'File processing error: {str(e)}'}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@handle_api_errors
def get_analytics(request, dataset_id):
    """
    Get analytics summary for a specific dataset
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get equipment records for this dataset
    equipment_records = EquipmentRecord.objects.filter(dataset=dataset)
    
    # Prepare response data
    response_data = {
        'dataset_id': dataset.id,
        'summary': {
            'total_count': dataset.record_count,
            'averages': {
                'flowrate': dataset.avg_flowrate,
                'pressure': dataset.avg_pressure,
                'temperature': dataset.avg_temperature
            },
            'type_distribution': dataset.type_distribution
        },
        'metadata': {
            'filename': dataset.filename,
            'upload_time': dataset.upload_timestamp.isoformat(),
            'record_count': dataset.record_count
        },
        'equipment_records': [
            {
                'equipment_name': record.equipment_name,
                'equipment_type': record.equipment_type,
                'flowrate': record.flowrate,
                'pressure': record.pressure,
                'temperature': record.temperature
            }
            for record in equipment_records
        ]
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@handle_api_errors
def get_dataset_list(request):
    """
    Get list of all datasets for the current user
    """
    datasets = Dataset.objects.filter(user=request.user).order_by('-upload_timestamp')
    
    dataset_list = [
        {
            'id': dataset.id,
            'filename': dataset.filename,
            'upload_time': dataset.upload_timestamp.isoformat(),
            'record_count': dataset.record_count,
            'summary': {
                'total_count': dataset.record_count,
                'avg_flowrate': dataset.avg_flowrate,
                'avg_pressure': dataset.avg_pressure,
                'avg_temperature': dataset.avg_temperature,
                'type_distribution': dataset.type_distribution
            }
        }
        for dataset in datasets
    ]
    
    return Response({
        'datasets': dataset_list,
        'total_datasets': len(dataset_list)
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@handle_api_errors
def get_history(request):
    """
    Get history of last 5 uploaded datasets with summaries
    """
    datasets = Dataset.objects.filter(user=request.user).order_by('-upload_timestamp')[:5]
    
    history_data = [
        {
            'id': dataset.id,
            'filename': dataset.filename,
            'upload_time': dataset.upload_timestamp.isoformat(),
            'record_count': dataset.record_count,
            'summary': {
                'total_count': dataset.record_count,
                'avg_flowrate': dataset.avg_flowrate,
                'avg_pressure': dataset.avg_pressure,
                'avg_temperature': dataset.avg_temperature,
                'type_distribution': dataset.type_distribution
            }
        }
        for dataset in datasets
    ]
    
    return Response({
        'datasets': history_data,
        'total_in_history': len(history_data)
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@handle_api_errors
def delete_dataset(request, dataset_id):
    """
    Delete a specific dataset
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        dataset_name = dataset.filename
        dataset.delete()  # This will cascade delete related EquipmentRecords
        
        return Response({
            'message': f'Dataset "{dataset_name}" deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
from django.http import HttpResponse
from analytics.report_generator import ReportGenerator


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@handle_api_errors
def generate_report(request):
    """
    Generate PDF report for a dataset
    """
    dataset_id = request.data.get('dataset_id')
    
    if not dataset_id:
        return Response(
            {'error': 'Dataset ID is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Check if dataset exists and belongs to user
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        
        # Generate report
        report_generator = ReportGenerator()
        report_buffer = report_generator.generate_report_buffer(dataset_id)
        
        # Create HTTP response with PDF
        response = HttpResponse(
            report_buffer.getvalue(),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.filename}_{dataset.id}.pdf"'
        
        return response
        
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Report generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@handle_api_errors
def download_report(request, dataset_id):
    """
    Download PDF report for a dataset
    """
    try:
        # Check if dataset exists and belongs to user
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        
        # Generate report
        report_generator = ReportGenerator()
        report_buffer = report_generator.generate_report_buffer(dataset_id)
        
        # Create HTTP response with PDF
        response = HttpResponse(
            report_buffer.getvalue(),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.filename}_{dataset.id}.pdf"'
        
        return response
        
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Report generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
import os
from django.conf import settings


@csrf_exempt
def load_sample_data(request):
    """
    Load sample equipment data for demonstration - using plain Django view
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    print(f"Sample data request from user: {request.user.username}")
    
    try:
        # Path to sample data file
        sample_file_path = os.path.join(settings.BASE_DIR, 'sample_equipment_data.csv')
        
        if not os.path.exists(sample_file_path):
            return JsonResponse({'error': 'Sample data file not found'}, status=404)
        
        # Process sample data using analytics engine
        dataset, summary = AnalyticsEngine.process_csv(
            sample_file_path, 
            request.user, 
            'sample_equipment_data.csv'
        )
        
        # Clean up old datasets (keep only last 5)
        AnalyticsEngine.cleanup_old_datasets(request.user, limit=5)
        
        return JsonResponse({
            'message': 'Sample data loaded successfully',
            'dataset_id': dataset.id,
            'filename': dataset.filename,
            'record_count': dataset.record_count,
            'summary': {
                'total_count': summary['total_count'],
                'averages': summary['averages'],
                'type_distribution': summary['type_distribution']
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': f'Failed to load sample data: {str(e)}'}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sample_info(request):
    """
    Get information about the sample data without authentication
    """
    try:
        sample_file_path = os.path.join(settings.BASE_DIR, 'sample_equipment_data.csv')
        
        if not os.path.exists(sample_file_path):
            return Response(
                {'error': 'Sample data file not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Read sample data to get basic info
        import pandas as pd
        df = pd.read_csv(sample_file_path)
        
        # Basic statistics
        equipment_types = df['Type'].value_counts().to_dict()
        
        return Response({
            'filename': 'sample_equipment_data.csv',
            'description': 'Sample chemical equipment data for demonstration',
            'record_count': len(df),
            'equipment_types': equipment_types,
            'columns': list(df.columns),
            'sample_records': df.head(5).to_dict('records')
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to read sample data info: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )