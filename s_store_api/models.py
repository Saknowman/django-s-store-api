from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from s_store_api.settings import api_settings


class Store(models.Model):
    name = models.CharField(max_length=api_settings.STORE_MODEL['MAX_LENGTH'])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='stores', on_delete=models.CASCADE)

    def __str__(self):
        return "{user}: {name}".format(user=self.user, name=self.name)


class Item(models.Model):
    name = models.CharField(max_length=api_settings.ITEM_MODEL['MAX_LENGTH'])
    store = models.ForeignKey(to=Store, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return "{store}: {name}".format(store=self.store, name=self.name)
