from typing import List

from rest_framework import permissions


class AndAll(permissions.BasePermission):
    message = None

    def __init__(self, my_permissions: List[permissions.BasePermission]):
        self._permissions = my_permissions

    def has_permission(self, request, view):
        for permission in self._permissions:
            if not permission.has_permission(request, view):
                if hasattr(permission, 'message'):
                    self.message = permission.message
                return False
        return True

    def has_object_permission(self, request, view, obj):
        for permission in self._permissions:
            if not permission.has_object_permission(request, view, obj):
                if hasattr(permission, 'message'):
                    self.message = permission.message
                return False
        return True
