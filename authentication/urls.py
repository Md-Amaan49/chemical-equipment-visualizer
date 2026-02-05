from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_auth, name='test_auth'),  # Test endpoint
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_info, name='user_info'),
]