from rest_framework import status

from s_store_api.models import Store
from s_store_api.tests.utils import BaseAPITestCase, STORE_LIST_URL, get_detail_store_url


class StoreListTest(BaseAPITestCase):
    def test_list_store___there_are_some_stores___200_and_response_data_has_expect_columns(self):
        # Arrange
        expect_columns_in_response_data = ['pk', 'name', 'user']
        expect_columns_in_store_user_data = ['pk', 'username']
        self.client.force_login(self.un_relation_user)
        expected_stores = Store.objects.filter(is_limited_access=False).all()
        # Act
        response = self.client.get(STORE_LIST_URL)
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertListEqual([store.pk for store in expected_stores],
                             [store['pk'] for store in response.data], response.data)
        for store_data in response.data:
            self.assertTrue(all(column in store_data for column in expect_columns_in_response_data))
            self.assertTrue(all(column in store_data['user'] for column in expect_columns_in_store_user_data))

    def test_list_store___some_stores_are_access_limited___list_only_stores_allowed_to_access(self):
        # Arrange
        self.client.force_login(self.user_a)
        self.default_store.is_limited_access = True
        self.default_store.save()
        self.default_store2.is_limited_access = True
        self.default_store2.save()
        self.user_a.groups.add(self.default_store2.limited_customer_group)
        expected_stores = [self.store_a, self.default_store2]
        # Act
        response = self.client.get(STORE_LIST_URL)
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertListEqual(
            [store.pk for store in expected_stores],
            [store['pk'] for store in response.data])

    def test_detail_store___items_parameter_is_false___200_get_with_out_items(self):
        # Arrange
        expected_columns = ['pk', 'name', 'user']
        # Act
        response = self.client.get(get_detail_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(all([column in response.data for column in expected_columns]), response.data)
        self.assertFalse('items' in response.data)

    def test_detail_store____items_parameter_is_true___200_get_with_items(self):
        # Arrange
        expected_columns = ['pk', 'name', 'user', 'items']
        # Act
        response = self.client.get(get_detail_store_url(self.default_store) + "?items=true")
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(all([column in response.data for column in expected_columns]), response.data)

    def test_detail_store___store_is_limited_access_store_and_login_users_has_read_authorization_of_store___200(self):
        # Arrange
        self.default_store.is_limited_access = True
        self.user_a.groups.add(self.default_store.limited_customer_group)
        self.default_store.save()
        self.client.force_login(self.user_a)
        # Act
        response = self.client.get(get_detail_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
