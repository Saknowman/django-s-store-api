from rest_framework import permissions

from s_store_api.models import Store
from s_store_api.utils.auth import is_user_in_group
from s_store_api.utils.request import is_request_allowed_only_staff, is_request_allowed_only_management_store_group
from s_store_api.utils.store import get_management_store_group


class IsLimitedStoreUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Store):
        if obj.user == request.user:
            return True
        if not obj.is_limited_access:
            return True
        return is_user_in_group(request.user, obj.limited_customer_group)


class IsStaffAndActionIsAllowedOnlyStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Store):
        if not is_request_allowed_only_staff(request):
            return True
        if obj.user == request.user:
            return True
        return is_user_in_group(request.user, obj.staff_group)


class IsInManagementStoreGroupAndActionIsAllowedOnlyManagementStoreGroup(permissions.BasePermission):
    message = "You don't have authority of store managements."

    def has_permission(self, request, view):
        if not is_request_allowed_only_management_store_group(request):
            return True
        return is_user_in_group(request.user, get_management_store_group())
