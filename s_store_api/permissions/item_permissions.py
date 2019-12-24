from rest_framework import permissions

from s_store_api.models import Item, Store
from .common import AndAll
from .store_permissions import (IsLimitedStoreUser as StorePermissions_IsLimitedStoreUser,
                                IsStaffAndActionIsAllowedOnlyStaff as StorePermissions_IsStaffAndActionIsAllowedOnlyStaff)


class IsLimitedStoreUser(permissions.BasePermission):
    def __init__(self):
        self.store_permission = StorePermissions_IsLimitedStoreUser()

    def has_permission(self, request, view):
        store = Store.objects.get(pk=request.parser_context['kwargs']['store'])
        return self.store_permission.has_object_permission(request, view, store)

    def has_object_permission(self, request, view, obj: Item):
        return self.store_permission.has_object_permission(request, view, obj.store)


class IsStaffAndActionIsAllowedOnlyStaff(permissions.BasePermission):
    def __init__(self):
        self.store_permission = StorePermissions_IsStaffAndActionIsAllowedOnlyStaff()

    def has_permission(self, request, view):
        store = Store.objects.get(pk=request.parser_context['kwargs']['store'])
        return self.store_permission.has_object_permission(request, view, store)

    def has_object_permission(self, request, view, obj: Item):
        return self.store_permission.has_object_permission(request, view, obj.store)


class DefaultItemPermissions(AndAll):
    def __init__(self):
        super().__init__([
            permissions.IsAuthenticated(),
            IsLimitedStoreUser(),
            IsStaffAndActionIsAllowedOnlyStaff()
        ])
