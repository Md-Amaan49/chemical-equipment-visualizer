from rest_framework.permissions import BasePermission


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to only allow authenticated users to modify data.
    Read-only permissions are allowed for any request.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions are only allowed to authenticated users.
        return request.user and request.user.is_authenticated


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions are only allowed to the owner of the dataset.
        return obj.user == request.user