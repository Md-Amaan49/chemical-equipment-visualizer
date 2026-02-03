from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('analytics/<int:dataset_id>/', views.get_analytics, name='get_analytics'),
    path('datasets/', views.get_dataset_list, name='get_dataset_list'),
    path('history/', views.get_history, name='get_history'),
    path('datasets/<int:dataset_id>/', views.delete_dataset, name='delete_dataset'),
    path('reports/generate/', views.generate_report, name='generate_report'),
    path('reports/<int:dataset_id>/download/', views.download_report, name='download_report'),
    path('sample/load/', views.load_sample_data, name='load_sample_data'),
    path('sample/info/', views.get_sample_info, name='get_sample_info'),
]