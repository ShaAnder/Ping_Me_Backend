from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Other users can only view it.
    """
    def has_object_permission(self, request, view, obj):
        # If the request method is a safe method (GET, HEAD, OPTIONS), grant permission
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise, check if the user is the owner
        return obj.user == request.user