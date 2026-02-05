from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_auth(request):
    """Test endpoint to verify auth app is working"""
    return Response({'message': 'Authentication app is working'}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User authentication endpoint - using DRF view"""
    try:
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return Response({'error': 'Internal server error'}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        logout(request)
        return Response({'message': 'Logout successful'}, status=200)
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response({'error': 'Internal server error'}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """Get current user information"""
    try:
        user = request.user
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_authenticated': True
            }
        }, status=200)
    except Exception as e:
        logger.error(f"User info error: {str(e)}")
        return Response({'error': 'Internal server error'}, status=500)