from django.urls import reverse
from rest_framework import status

from s_store_api.models import Store, Item
from s_store_api.tests.utils import BaseAPITestCase


def _get_list_items_of_store_url(store):
    pk = store if not isinstance(store, Store) else store.pk
    return reverse('stores:items-list', kwargs={'store': pk})


class ItemsGetTest(BaseAPITestCase):
    def test_list_items___target_store_has_some_items___200(self):
        # Arrange
        expect_items = Item.objects.filter(store=self.default_store.pk).all()
        print(expect_items)
        # Act
        response = self.client.get(_get_list_items_of_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code, response)
        self.assertFalse(len(response.data) is 0)
        self.assertListEqual([item.pk for item in expect_items],
                             [item['pk'] for item in response.data], response.data)

    def test_list_items___with_out_authentication___404(self):
        # Arrange
        self.client.logout()
        # Act
        response = self.client.get(_get_list_items_of_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
