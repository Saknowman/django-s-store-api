from django.conf import settings

APP_SETTING_ROUTE_NAME = 'S_STORE_API'

DEFAULTS = {
    'STORE_MODEL': {
        'MAX_LENGTH': 20,
    },
    'ITEM_MODEL': {
        'MAX_LENGTH': 20,
    },
    'COIN_MODEL': {
        'MAX_LENGTH': 5,
    },
    'STORE_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        's_store_api.permissions.store_permissions.IsLimitedStoreUser',
        's_store_api.permissions.store_permissions.IsStaffAndActionIsAllowedOnlyStaff',
        's_store_api.permissions.store_permissions.IsInManagementStoreGroupAndActionIsAllowedOnlyManagementStoreGroup'
    ],
    'ITEM_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        's_store_api.permissions.item_permissions.IsLimitedStoreUser',
        's_store_api.permissions.item_permissions.IsStaffAndActionIsAllowedOnlyStaff',
    ],
}


class APISettings:
    """
    A settings object, that allows API settings to be accessed as properties.
    Set default settings in your app settings.py like this:
        from app_utils.setting import APISettings
        api_settings = APISettings('TODO_API', DEFAULTS)
    For example:
        from todo_api.settings import api_settings
        print(api_settings.TASK_STATUS_CHOICES)
    """

    def __init__(self, setting_root_name, defaults):
        self._setting_root_name = setting_root_name
        self._defaults = defaults
        self._user_settings = getattr(settings, self._setting_root_name, {})

    def __getattr__(self, item):
        if item not in self._defaults:
            raise AttributeError("Invalid {} setting: {}".format(self._setting_root_name, item))

        try:
            return self._user_settings[item]
        except KeyError:
            return self._defaults[item]


api_settings = APISettings(APP_SETTING_ROUTE_NAME, DEFAULTS)
