from django.apps import AppConfig


class SStoreApiConfig(AppConfig):
    name = 's_store_api'

    def ready(self):
        from s_store_api.managements import set_default_groups
        set_default_groups()
