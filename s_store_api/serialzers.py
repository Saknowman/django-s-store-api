from rest_framework import serializers

from .models import Store, Item, Price, Coin


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('pk', 'name')
        read_only_fields = ['pk']


class PriceSerializer(serializers.ModelSerializer):
    coin = CoinSerializer()

    class Meta:
        model = Price
        fields = ('pk', 'item', 'coin', 'value')
        read_only_fields = ('pk', 'item')


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('pk', 'name', 'user')
        read_only_fields = ('pk', 'user')


class ItemSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('pk', 'name', 'store', 'prices')
        read_only_fields = ('pk', 'user', 'prices')

    @staticmethod
    def get_prices(obj: Item):
        price_serializer = PriceSerializer(instance=obj.prices.filter(), many=True)
        return price_serializer.data
