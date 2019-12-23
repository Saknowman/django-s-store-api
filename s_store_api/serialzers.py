from django.db import transaction
from rest_framework import serializers

from .models import Store, Item, Price, Coin
from .utils.auth import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')
        read_only_fields = ['pk', 'username']


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('pk', 'name')
        read_only_fields = ['pk']


class PriceSerializer(serializers.ModelSerializer):
    coin = CoinSerializer(read_only=True)
    coin_id = serializers.PrimaryKeyRelatedField(
        queryset=Coin.objects.filter(), source='coin', write_only=True)

    class Meta:
        model = Price
        fields = ('pk', 'item', 'coin', 'value', 'coin_id')
        read_only_fields = ('pk', 'item', 'coin')


class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Store
        fields = ('pk', 'name', 'user', 'is_limited_access')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        if Store.objects.filter(name=validated_data['name'], user=validated_data['user']).exists():
            raise serializers.ValidationError("Same name store is already exists in your stores.")
        return super().create(validated_data)


class ItemSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()
    prices_set = PriceSerializer(many=True, write_only=True)

    class Meta:
        model = Item
        fields = ('pk', 'name', 'store', 'prices', 'prices_set')
        read_only_fields = ('pk', 'user', 'store', 'prices')

    def create(self, validated_data):
        with transaction.atomic():
            validated_data_for_item = {
                'name': validated_data.get('name'),
                'store': validated_data.get('store'),
            }
            result = super().create(validated_data_for_item)
            from s_store_api.utils.price import create_prices
            create_prices(validated_data.get('prices_set'), result)
            return result

    @staticmethod
    def get_prices(obj: Item):
        price_serializer = PriceSerializer(instance=obj.prices.filter(), many=True)
        return price_serializer.data
