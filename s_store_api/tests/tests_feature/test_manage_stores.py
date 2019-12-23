from rest_framework import status

from s_store_api.models import Store
from s_store_api.tests.utils import BaseAPITestCase, STORE_LIST_URL, get_detail_store_url, validation_error_status


class OpenStoresTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.default_user.groups.add(self.management_store_group)

    def test_open_store___has_permission___201(self):
        # Arrange
        data = {'name': 'new_store', 'is_limited_access': True}
        # Act
        response = self.client.post(STORE_LIST_URL, data)
        # Assert
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertTrue(Store.objects.filter(
            name='new_store', user=self.default_user, is_limited_access=True).exists())

    def test_open_store___open_same_name_store_of_myself___return_validation_error_code(self):
        # Arrange
        Store.objects.create(name='aaa', user=self.default_user)
        data = {'name': 'aaa'}
        # Act
        response = self.client.post(STORE_LIST_URL, data)
        print(response.data)
        # Assert
        self.assertEqual(validation_error_status, response.status_code)

