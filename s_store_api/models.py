from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from s_store_api.settings import api_settings
from s_store_api.utils.store import get_default_limited_customer_group


class Store(models.Model):
    name = models.CharField(max_length=api_settings.STORE_MODEL['MAX_LENGTH'])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='stores', on_delete=models.CASCADE)
    is_limited_access = models.BooleanField(default=False)
    limited_customer_group = models.OneToOneField(to=Group, related_name='customer_group_store',
                                                  on_delete=models.CASCADE, default=get_default_limited_customer_group)

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
