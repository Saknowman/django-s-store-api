from rest_framework import test
from django.urls import reverse
from rest_framework.exceptions import ValidationError

from s_store_api.models import Store, Item, Coin
from s_store_api.utils.auth import User

validation_error_status = ValidationError.status_code


class BaseAPITestCase(test.APITestCase):
    fixtures = ['test_users.json', 'test_data.json']

    admin: User
    staff_user: User
    default_user: User
    user_a: User
    default_store: Store
    store_a: Store
    default_item1: Item
    default_item2: Item
    a_item1: Item
    a_item2: Item
    world_coin: Coin
    dollar_coin: Coin

    def setUp(self) -> None:
        super().setUp()
        self._set_members()
        self._set_stores()
        self._set_items()
        self._set_coins()
        self.client.force_login(self.default_user)

    def _set_members(self):
        self.admin = User.objects.get(username='admin')
        self.staff_user = User.objects.get(username='staff_user')
        self.default_user = User.objects.get(username='default_user')
        self.user_a = User.objects.get(username='user_a')
        self.un_relation_user = User.objects.get(username='un_relation_user')

    def _set_stores(self):
        self.default_store = Store.objects.filter(user=self.default_user.pk).first()
        self.default_store2 = Store.objects.get(name='default_store_2')
        self.store_a = Store.objects.filter(user=self.user_a.pk).first()

    def _set_items(self):
        self.default_item1 = Item.objects.get(store=self.default_store.pk, name='item1')
        self.default_item2 = Item.objects.get(store=self.default_store.pk, name='item2')
        self.a_item1 = Item.objects.get(store=self.store_a.pk, name='item1')
        self.a_item2 = Item.objects.get(store=self.store_a.pk, name='item2')

    def _set_coins(self):
        self.world_coin = Coin.objects.get(name='world')
        self.dollar_coin = Coin.objects.get(name='$')
        self.yen_coin = Coin.objects.get(name='yen')
        self.pond_coin = Coin.objects.get(name='pond')


STORE_LIST_URL = reverse('stores:stores-list')


def get_list_items_of_store_url(store):
    pk = store if not isinstance(store, Store) else store.pk
    return reverse('stores:items-list', kwargs={'store': pk})


def get_detail_item_url(store, item):
    store_pk = store if not isinstance(store, Store) else store.pk
    item_pk = item if not isinstance(item, Item) else item.pk
    return reverse('stores:items-detail', kwargs={'store': store_pk, 'pk': item_pk})


def get_buy_item_url(store, item):
    store_pk = store if not isinstance(store, Store) else store.pk
    item_pk = item if not isinstance(item, Item) else item.pk
    return reverse('stores:items-buy', kwargs={'store': store_pk, 'pk': item_pk})


def get_list_prices_of_item_url(item):
    item_pk = item if not isinstance(item, Item) else item.pk
    return reverse('stores:prices-list', kwargs={'item': item_pk})


def get_detail_store_url(store):
    store_pk = store if not isinstance(store, Store) else store.pk
    return reverse('stores:stores-detail', kwargs={'pk': store_pk})
