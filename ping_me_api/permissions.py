from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    For Channel: allows both channel owner and server owner.
    """

    owner_fields = ['owner', 'user', 'account']

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # For Channel: allow if channel owner or server owner
        if obj.__class__.__name__ == "Channel":
            # Check if request.user has an account
            account = getattr(request.user, "account", None)
            if not account:
                return False
            # Channel owner or server owner
            return obj.owner == account or getattr(obj.server, "owner", None) == account

        # For other models: check common owner fields (must compare to Account, not User)
        account = getattr(request.user, "account", None)
        for field in self.owner_fields:
            if hasattr(obj, field):
                return getattr(obj, field) == account
        return False
