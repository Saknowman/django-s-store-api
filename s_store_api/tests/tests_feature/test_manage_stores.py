from rest_framework import status

from s_store_api.models import Store
from s_store_api.tests.utils import BaseAPITestCase, STORE_LIST_URL, get_detail_store_url, validation_error_status, \
    get_hire_staff_url, get_dismiss_staff_url, get_invite_user_to_access_limited_store_url


class BaseStoreManagementTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.default_user.groups.add(self.management_store_group)


class OpenStoresTestCase(BaseStoreManagementTestCase):
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
        # Assert
        self.assertEqual(validation_error_status, response.status_code)


class CloseStoresTestCase(BaseStoreManagementTestCase):
    def test_close_store___has_permission_and_owner___201(self):
        # Act
        response = self.client.delete(get_detail_store_url(self.default_store))
        # Assert
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Store.objects.filter(pk=self.default_store.pk).exists())


class UpdateStoresTestCase(BaseStoreManagementTestCase):
    def test_update_store___has_permission_and_owner___200(self):
        # Arrange
        self.default_store.name = 'not changed'
        self.default_store.is_limited_access = False
        self.default_store.save()
        data = {'name': 'changed', 'is_limited_access': True}
        # Act
        put_response = self.client.put(get_detail_store_url(self.default_store), data)
        patch_response = self.client.put(get_detail_store_url(self.default_store), data)
        # Assert
        self.assertEqual(status.HTTP_200_OK, put_response.status_code)
        self.assertEqual(status.HTTP_200_OK, patch_response.status_code)
        updated_store = Store.objects.get(pk=self.default_store.pk)
        self.assertTrue('changed', updated_store.name)
        self.assertTrue(True, updated_store.is_limited_access)

    def test_hire_staff___has_permission_and_owner___200(self):
        # Act
        response = self.client.put(get_hire_staff_url(self.default_store), {'staff': self.user_a.pk})
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(self.default_store.staff_group in self.user_a.groups.all())

    def test_hire_staff___staff_already_exists___200(self):
        # Arrange
        self.user_a.groups.add(self.default_store.staff_group)
        # Act
        response = self.client.put(get_hire_staff_url(self.default_store), {'staff': self.user_a.pk})
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_dismiss_staff___staff_is_hired___200(self):
        # Arrange
        self.user_a.groups.add(self.default_store.staff_group)
        # Act
        response = self.client.put(get_dismiss_staff_url(self.default_store), {'staff': self.user_a.pk})
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertFalse(self.default_store.staff_group in self.user_a.groups.all())

    def test_dismiss_staff___target_user_is_not_staff___404(self):
        # Act
        response = self.client.put(get_dismiss_staff_url(self.default_store), {'staff': self.user_a.pk})
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_hire_and_dismiss_staff___user_is_not_exists___404(self):
        # Act
        hire_response = self.client.put(get_hire_staff_url(self.default_store), {'staff': 1231})
        dismiss_response = self.client.put(get_dismiss_staff_url(self.default_store), {'staff': 1231})
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, hire_response.status_code)
        self.assertEqual(status.HTTP_404_NOT_FOUND, dismiss_response.status_code)

    def test_invite_users_to_access_limited_store___is_staff___200(self):
        # Arrange
        self.store_a.is_limited_access = True
        self.store_a.save()
        self.default_user.groups.add(self.store_a.staff_group)
        # Act
        response = self.client.put(get_invite_user_to_access_limited_store_url(self.store_a),
                                   {'users': [self.un_relation_user.pk, self.un_relation_user2.pk]}, format='json')
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(self.store_a.limited_customer_group in self.un_relation_user.groups.all())
        self.assertTrue(self.store_a.limited_customer_group in self.un_relation_user2.groups.all())

    def test_invite_users_to_access_limited_store___some_user_is_not_exits___404(self):
        # Arrange
        self.default_store.is_limited_access = True
        self.default_store.save()
        # Act
        response = self.client.put(get_invite_user_to_access_limited_store_url(self.default_store),
                                   {'users': [self.un_relation_user.pk, 1232]}, format='json')
        # Assert
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertFalse(self.default_store.limited_customer_group in self.un_relation_user.groups.all())

