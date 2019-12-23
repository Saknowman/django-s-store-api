from django.contrib.auth.models import Group, Permission
from django.db import transaction
from rest_framework import exceptions

from s_store_api.models import CashRegister
from s_store_api.utils.auth import User
from s_store_api.utils.bag import create_bag_if_user_has_not


def list_stores(user: User):
    from s_store_api.models import Store
    my_stores = Store.objects.filter(user=user)
    unlimited_access_stores = Store.objects.filter(is_limited_access=False)
    staff_stores = Store.objects.filter(staff_group__in=user.groups.all())
    limited_access_and_has_permission_stores = Store.objects.filter(is_limited_access=True,
                                                                    limited_customer_group__in=user.groups.all())
    return my_stores | unlimited_access_stores | staff_stores | limited_access_and_has_permission_stores


def buy_item(user: User, item, price):
    """
    Returns:
        str: return None if the trade is completed
         or return message if failed the trade
    """
    wallet = user.wallets.get(coin=price.coin)
    if wallet.value < price.value:
        return "That's not enough."
    cash_register = CashRegister.objects.get(store=item.store, coin=price.coin)
    with transaction.atomic():
        wallet.value -= price.value
        wallet.save()
        cash_register.value += price.value
        cash_register.save()
        bag = create_bag_if_user_has_not(user, item)
        bag.amount += 1
        bag.save()
    return None


def get_management_store_group():
    try:
        return Group.objects.get(name='management_store_group')
    except Group.DoesNotExist:
        pass
    group = Group()
    group.name = 'management_store_group'
    group.save()

    from s_store_api.models import Store
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(Store)
    permissions = Permission.objects.filter(
        content_type=content_type,
        codename__in=['add_store', 'change_store', 'delete_store', 'management_store']).all()
    for permission in permissions:
        group.permissions.add(permission)
    return group


def get_staff_user(user_pk, store):
    try:
        user = User.objects.get(pk=user_pk)
        if is_staff(user, store):
            return user
        raise exceptions.NotFound
    except User.DoesNotExist:
        raise exceptions.NotFound


def is_staff(user, store):
    return store.staff_group in user.groups.all()
