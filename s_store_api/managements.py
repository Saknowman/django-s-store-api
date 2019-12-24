from s_store_api.utils.store import get_management_store_group


def set_default_groups():
    try:
        get_management_store_group()
    except Exception:
        pass
