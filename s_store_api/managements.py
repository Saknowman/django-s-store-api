from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from s_store_api.models import Store
from s_store_api.utils.store import get_management_store_group


def set_default_groups():
    get_management_store_group()
