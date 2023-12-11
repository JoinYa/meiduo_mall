from rest_framework import permissions
from apps.users.models import User


# 自定义权限
class BasePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_superuser:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        if isinstance(obj, User):
            return obj == request.user
        return obj.user == request.user
