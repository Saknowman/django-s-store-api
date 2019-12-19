from rest_framework import permissions

from s_store_api.models import Store
from s_store_api.utils.auth import is_user_in_group


class IsLimitedStoreUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Store):
        if obj.user == request.user:
            return True
        if not obj.is_limited_access:
            return True
        return is_user_in_group(request.user, obj.limited_customer_group)
