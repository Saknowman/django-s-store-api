from rest_framework import status

from s_store_api.tests.utils import BaseAPITestCase, get_list_items_of_store_url, get_detail_item_url, get_buy_item_url


class GetItemsPermissionTestCase(BaseAPITestCase):
    def test_get_items___with_out_authentication___404(self):
        # Arrange
        self.client.logout()
        # Act
        list_response = self.client.get(get_list_items_of_store_url(self.default_store))
        detail_response = self.client.get(get_detail_item_url(self.default_store, self.default_item1))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, list_response.status_code)
        self.assertEqual(status.HTTP_404_NOT_FOUND, detail_response.status_code)

    def test_get_items___store_is_limited_access_store_and_login_user_has_no_read_authorization_of_store___404(self):
        # Arrange
        self.default_store.is_limited_access = True
        self.default_store.save()
        self.client.force_login(self.user_a)
        # Arrange
        list_response = self.client.get(get_list_items_of_store_url(self.default_store))
        detail_response = self.client.get(get_detail_item_url(self.default_store, self.default_item1))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, list_response.status_code, list_response.data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, detail_response.status_code, detail_response.data)


class PostItemsPermissionTestCase(BaseAPITestCase):
    def test_buy_items___without_authentication___404(self):
        # Arrange
        self.client.logout()
        data = {'price': self.default_item1.prices.first().pk}
        # Act
        response = self.client.post(get_buy_item_url(self.default_store, self.default_item1), data)
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_buy_items___store_is_limited_access_store_and_login_user_has_no_read_authorization_of_store___404(self):
        # Arrange
        self.default_store.is_limited_access = True
        self.default_store.save()
        self.client.force_login(self.user_a)
        data = {'price': self.default_item1.prices.first().pk}
        # Act
        response = self.client.post(get_buy_item_url(self.default_store, self.default_item1), data)
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
