from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    """User authentication endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
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
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    logout(request)
    return Response(
        {'message': 'Logout successful'}, 
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """Get current user information"""
    user = request.user
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_authenticated': True
        }
    }, status=status.HTTP_200_OK)