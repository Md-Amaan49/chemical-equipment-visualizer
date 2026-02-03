from functools import wraps
from django.http import JsonResponse
from rest_framework import status


def require_authentication(view_func):
    """
    Decorator to ensure user is authenticated before accessing the view
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)
    return wrapper


def handle_api_errors(view_func):
    """
    Decorator to handle common API errors and return consistent responses
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(
                {'error': 'Internal server error', 'details': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper