from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q

from s_store_api.utils.auth import User
from s_store_api.utils.bag import create_bag_if_user_has_not
from s_store_api.utils.common import get_next_usable_pk


def list_stores(user: User):
    from s_store_api.models import Store
    my_stores = Store.objects.filter(user=user)
    unlimited_access_stores = Store.objects.filter(is_limited_access=False)
    limited_access_and_has_permission_stores = Store.objects.filter(is_limited_access=True,
                                                                    limited_customer_group__in=user.groups.all())
    return my_stores | unlimited_access_stores | limited_access_and_has_permission_stores


def get_default_limited_customer_group() -> int:
    group = Group()
    group.name = 'store__limited_customer_group__' + str(get_next_usable_pk(Group))
    group.save()
    return group.pk


def get_default_staff_group() -> int:
    group = Group()
    group.name = 'store__staff_group__' + str(get_next_usable_pk(Group))
    group.save()
    return group.pk


def buy_item(user: User, item, price):
    """
    Returns:
        str: return None if the trade is completed
         or return message if failed the trade
    """
    wallet = user.wallets.get(coin=price.coin)
    if wallet.value < price.value:
        return "That's not enough."
    with transaction.atomic():
        wallet.value -= price.value
        wallet.save()
        bag = create_bag_if_user_has_not(user, item)
        bag.amount += 1
        bag.save()
    return None
