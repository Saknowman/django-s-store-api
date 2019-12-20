from django.db import transaction

from s_store_api.models import Store, Item
from s_store_api.serialzers import ItemSerializer


def create_item(name: str, store: Store, prices_set=None) -> Item:
    with transaction.atomic():
        if prices_set is None:
            prices_set = []
        serializer = ItemSerializer(data={
            'name': name,
            'prices_set': prices_set
        })
        serializer.is_valid(raise_exception=True)
        return serializer.save(store=store)
