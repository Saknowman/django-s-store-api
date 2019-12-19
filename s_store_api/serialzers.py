from rest_framework import serializers

from .models import Store, Item


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('pk', 'name', 'user')
        read_only_fields = ('pk', 'user')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('pk', 'name', 'store')
        read_only_fields = ('pk', 'user')
