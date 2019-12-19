from rest_framework import test

from s_store_api.models import Store, Item
from s_store_api.utils.auth import User


class BaseAPITestCase(test.APITestCase):
    fixtures = ['test_users.json', 'test_stores_and_items.json']

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

    def setUp(self) -> None:
        super().setUp()
        self._set_members()
        self._set_stores()
        self._set_items()
        self.client.force_login(self.default_user)

    def _set_members(self):
        self.admin = User.objects.get(username='admin')
        self.staff_user = User.objects.get(username='staff_user')
        self.default_user = User.objects.get(username='default_user')
        self.user_a = User.objects.get(username='user_a')

    def _set_stores(self):
        self.default_store = Store.objects.filter(user=self.default_user.pk).first()
        self.store_a = Store.objects.filter(user=self.user_a.pk).first()

    def _set_items(self):
        self.default_item1 = Item.objects.get(store=self.default_store.pk, name='item1')
        self.default_item2 = Item.objects.get(store=self.default_store.pk, name='item2')
        self.a_item1 = Item.objects.get(store=self.store_a.pk, name='item1')
        self.a_item2 = Item.objects.get(store=self.store_a.pk, name='item2')
