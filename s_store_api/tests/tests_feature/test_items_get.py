from django.urls import reverse
from rest_framework import status

from s_store_api.models import Store, Item
from s_store_api.tests.utils import BaseAPITestCase


def _get_list_items_of_store_url(store):
    pk = store if not isinstance(store, Store) else store.pk
    return reverse('stores:items-list', kwargs={'store': pk})


def _get_detail_item_url(store, item):
    store_pk = store if not isinstance(store, Store) else store.pk
    item_pk = item if not isinstance(item, Item) else item.pk
    return reverse('stores:items-detail', kwargs={'store': store_pk, 'pk': item_pk})


class ItemsListTest(BaseAPITestCase):
    def test_list_items___target_store_has_some_items___200_and_each_items_has_name_and_pk(self):
        # Arrange
        expected_response_data_columns = ['pk', 'name', 'prices']
        expect_items = Item.objects.filter(store=self.default_store.pk).all()
        # Act
        response = self.client.get(_get_list_items_of_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code, response)
        self.assertFalse(len(response.data) is 0)
        self.assertListEqual([item.pk for item in expect_items],
                             [item['pk'] for item in response.data], response.data)
        print(response.data)
        for item in response.data:
            self.assertTrue(all([(column in item) for column in expected_response_data_columns]),
                            response.data)

    def test_list_items___store_is_limited_access_store_and_login_users_has_read_authorization_of_store___200(self):
        # Arrange
        self.default_store.is_limited_access = True
        self.user_a.groups.add(self.default_store.limited_customer_group)
        self.default_store.save()
        users = [self.default_user, self.user_a]
        for user in users:
            # Sub Test
            with self.subTest(user=user):
                self.client.force_login(user)
                # Act
                response = self.client.get(_get_list_items_of_store_url(self.default_store))
                # Assert
                self.assertEqual(status.HTTP_200_OK, response.status_code, response)

    def test_list_items___store_does_not_exists___404(self):
        # Arrange
        self.client.logout()
        # Act
        # noinspection PyTypeChecker
        response = self.client.get(_get_list_items_of_store_url(93939))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class ItemsDetailTest(BaseAPITestCase):
    def test_detail_item___has_authorization___200_and_item_has_pk_name_and_values(self):
        # Arrange
        expected_response_data_columns = ['pk', 'name', 'prices']
        # Act
        response = self.client.get(_get_detail_item_url(self.default_store, self.default_item1))
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertTrue(all([(column in response.data) for column in expected_response_data_columns]), response.data)
        for price in response.data['prices']:
            self.assertTrue(all([column in price] for column in ['pk', 'coin', 'value']))
            self.assertTrue(all([column in price['coin']] for column in ['pk', 'name']))

    def test_detail_items___store_does_not_exists___404(self):
        # Arrange
        self.client.logout()
        # Act
        # noinspection PyTypeChecker
        response = self.client.get(_get_detail_item_url(self.default_store, 90909))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class GetItemsPermissionTestCase(BaseAPITestCase):
    def test_get_items___with_out_authentication___404(self):
        # Arrange
        self.client.logout()
        # Act
        list_response = self.client.get(_get_list_items_of_store_url(self.default_store))
        detail_response = self.client.get(_get_list_items_of_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, list_response.status_code)
        self.assertEqual(status.HTTP_404_NOT_FOUND, detail_response.status_code)

    def test_get_items___store_is_limited_access_store_and_login_user_has_no_read_authorization_of_store___404(self):
        # Arrange
        self.default_store.is_limited_access = True
        self.default_store.save()
        self.client.force_login(self.user_a)
        # Arrange
        list_response = self.client.get(_get_list_items_of_store_url(self.default_store))
        detail_response = self.client.get(_get_detail_item_url(self.default_store, self.default_item1))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, list_response.status_code, list_response.data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, detail_response.status_code, detail_response.data)
