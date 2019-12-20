from django.contrib.auth.models import Group
from django.db import transaction

from s_store_api.utils.auth import User
from s_store_api.utils.bag import create_bag_if_user_has_not
from s_store_api.utils.common import get_next_usable_pk


def get_default_limited_customer_group():
    group = Group()
    group.name = 'store__limited_customer_group__' + str(get_next_usable_pk(Group))
    group.save()
    return group.pk


def get_default_staff_group():
    group = Group()
    group.name = 'store__staff_group__' + str(get_next_usable_pk(Group))
    group.save()
    return group.pk


def buy_item(user: User, item, price):
    wallet = user.wallets.get(coin=price.coin)
    if wallet.value < price.value:
        return False
    with transaction.atomic():
        wallet.value -= price.value
        wallet.save()
        bag = create_bag_if_user_has_not(user, item)
        bag.amount += 1
        bag.save()
    return True
