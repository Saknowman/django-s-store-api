from rest_framework import status

from s_store_api.tests.utils import BaseAPITestCase, STORE_LIST_URL, get_detail_store_url


class GetStoresPermissionTestCase(BaseAPITestCase):
    def test_get_stores___with_out_authentication___404(self):
        # Arrange
        self.client.logout()
        # Act
        list_response = self.client.get(STORE_LIST_URL)
        detail_response = self.client.get(get_detail_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, list_response.status_code)
        self.assertEqual(status.HTTP_404_NOT_FOUND, detail_response.status_code)

    def test_get_stores___to_limited_access_store___404(self):
        # Arrange
        self.store_a.is_limited_access = True
        self.store_a.save()
        # Act
        detail_response = self.client.get(get_detail_store_url(self.store_a))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, detail_response.status_code)


class OpenStoresPermissionTestCase(BaseAPITestCase):
    def test_open_stores___with_out_authentication__404(self):
        # Arrange
        self.client.logout()
        # Act
        response = self.client.post(STORE_LIST_URL, {})
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_open_store___has_not_permission___403(self):
        # Arrange
        self.default_user.groups.remove(self.management_store_group)
        # Act
        response = self.client.post(STORE_LIST_URL, {})
        # Assert
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class CloseStoresPermissionTestCase(BaseAPITestCase):
    def test_close_stores___without_authentication__404(self):
        # Arrange
        self.client.logout()
        # Act
        response = self.client.delete(get_detail_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_close_store___has_not_permission___403(self):
        # Arrange
        self.default_user.groups.remove(self.management_store_group)
        # Act
        response = self.client.delete(get_detail_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_close_store___store_is_not_users_store___403(self):
        # Arrange
        self.default_user.groups.add(self.management_store_group)
        # Act
        response = self.client.delete(get_detail_store_url(self.store_a))
        # Assert
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
