from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from s_store_api.settings import api_settings
from s_store_api.utils.auth import User
from s_store_api.utils.common import get_next_usable_pk


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


class Store(models.Model):
    name = models.CharField(max_length=api_settings.STORE_MODEL['MAX_LENGTH'])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='stores', on_delete=models.CASCADE)
    is_limited_access = models.BooleanField(default=False)
    limited_customer_group = models.OneToOneField(to=Group, related_name='customer_group_store',
                                                  on_delete=models.CASCADE, default=get_default_limited_customer_group)
    staff_group = models.OneToOneField(to=Group, related_name='staff_group_store',
                                       on_delete=models.CASCADE, default=get_default_staff_group)

    class Meta:
        permissions = (
            ('management_store', 'Can management store'),
        )
        unique_together = ('user', 'name')

    def __str__(self):
        return "{user}: {name}".format(user=self.user, name=self.name)


class Item(models.Model):
    name = models.CharField(max_length=api_settings.ITEM_MODEL['MAX_LENGTH'])
    store = models.ForeignKey(to=Store, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return "{store}: {name}".format(store=self.store, name=self.name)


class Coin(models.Model):
    name = models.CharField(max_length=api_settings.COIN_MODEL['MAX_LENGTH'])

    def __str__(self):
        return self.name


class Price(models.Model):
    item = models.ForeignKey(to=Item, related_name='prices', on_delete=models.CASCADE)
    coin = models.ForeignKey(to=Coin, related_name='prices', on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return "{coin}: {value}".format(coin=self.coin, value=self.value)


class Wallet(models.Model):
    user = models.ForeignKey(to=User, related_name='wallets', on_delete=models.CASCADE)
    coin = models.ForeignKey(to=Coin, related_name='wallets', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'coin')

    def __str__(self):
        return "{username}: {value}{coin_name}".format(username=self.user, value=self.value, coin_name=self.coin.name)


class CashRegister(models.Model):
    store = models.ForeignKey(to=Store, related_name='cash_registers', on_delete=models.CASCADE)
    coin = models.ForeignKey(to=Coin, related_name='cash_registers', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = ('store', 'coin')

    def __str__(self):
        return "{store_name}: {value}{coin_name}".format(store_name=self.store.name, value=self.value,
                                                         coin_name=self.coin.name)


class Receipt(models.Model):
    item = models.ForeignKey(to=Item, null=True, related_name='receipts', on_delete=models.SET_NULL)
    item_name = models.CharField(max_length=api_settings.ITEM_MODEL['MAX_LENGTH'])
    item_price = models.CharField(max_length=30)
    item_num = models.IntegerField(default=1)
    store = models.ForeignKey(to=Store, null=True, related_name='receipts', on_delete=models.SET_NULL)
    store_name = models.CharField(max_length=api_settings.STORE_MODEL['MAX_LENGTH'])
    user = models.ForeignKey(to=User, null=True, related_name='receipts', on_delete=models.SET_NULL)
    sold_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{store}:{item_name}:{value} x{num} ({datetime})".format(store=self.store_name,
                                                                        item_name=self.item_name,
                                                                        value=self.item_price, num=self.item_num,
                                                                        datetime=self.sold_date_time.strftime(
                                                                            "%d %b %Y %H:%M"), )


class Bag(models.Model):
    user = models.ForeignKey(to=User, related_name='bags', on_delete=models.CASCADE)
    item = models.ForeignKey(to=Item, related_name='bags', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return "{username}: {amount}{item_name}".format(username=self.user, amount=self.amount,
                                                        item_name=self.item.name)
