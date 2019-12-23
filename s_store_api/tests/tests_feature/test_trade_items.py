from rest_framework import status

from s_store_api.models import Wallet, Item
from s_store_api.settings import api_settings
from s_store_api.tests.utils import BaseAPITestCase, get_list_items_of_store_url, get_buy_item_url, \
    get_list_prices_of_item_url, validation_error_status
from s_store_api.utils.bag import create_bag_if_user_has_not
from s_store_api.utils.coin import get_treated_coins_from_store
from s_store_api.utils.item import create_item
from s_store_api.utils.wallet import create_wallet_if_user_has_not


class BuyItemsTestCase(BaseAPITestCase):
    def test_access_store___has_no_wallet___wallet_created(self):
        # Arrange
        Wallet.objects.filter(user=self.default_user).delete()
        treated_coins = get_treated_coins_from_store(self.default_store)
        # Act
        self.client.get(get_list_items_of_store_url(self.default_store))
        # Assert
        wallets = Wallet.objects.filter(user=self.default_user).all()
        self.assertFalse(len(wallets) == 0, wallets)
        for wallet in wallets:
            self.assertTrue(wallet.coin in treated_coins)

    def test_access_store___already_has_wallet___wallet_not_created(self):
        # Arrange
        target_coin = get_treated_coins_from_store(self.default_store)[0]
        expected_wallet = create_wallet_if_user_has_not(self.default_user, target_coin)
        # Act
        self.client.get(get_list_items_of_store_url(self.default_store))
        # Assert
        wallet = Wallet.objects.get(user=self.default_user, coin=target_coin)
        self.assertEqual(expected_wallet.pk, wallet.pk)

    def test_access_store___permission_failed___wallet_not_created(self):
        # Arrange
        Wallet.objects.filter(user=self.default_user).delete()
        self.client.logout()
        # Act
        self.client.get(get_list_items_of_store_url(self.default_store))
        # Assert
        wallets = Wallet.objects.filter(user=self.default_user).all()
        self.assertTrue(len(wallets) == 0, wallets)

    def test_buy_item___has_enough_money___payed_and_get(self):
        # Arrange
        default_value = 1000000
        wallet = create_wallet_if_user_has_not(self.default_user, self.world_coin)
        wallet.value = default_value
        wallet.save()
        target_price = self.default_item1.prices.get(coin=self.world_coin.pk)
        # Act
        response, wallet = self._post_buy_item(wallet, target_price)
        bag = self.default_user.bags.get(item=self.default_item1.pk)
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(default_value - target_price.value, wallet.value)
        self.assertEqual(1, bag.amount)

    def test_buy_item___already_has_bag___use_same_bag(self):
        # Arrange
        wallet = create_wallet_if_user_has_not(self.default_user, self.world_coin)
        wallet.value = 1000000
        wallet.save()
        target_price = self.default_item1.prices.get(coin=self.world_coin.pk)
        my_bag = create_bag_if_user_has_not(self.default_user, self.default_item1)
        # Act
        response, wallet = self._post_buy_item(wallet, target_price)
        bag = self.default_user.bags.get(item=self.default_item1.pk)
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(my_bag.pk, bag.pk)
        self.assertTrue(1, bag.amount)

    def test_buy_item___has_not_enough_money___400(self):
        # Arrange
        wallet = create_wallet_if_user_has_not(self.default_user, self.world_coin)
        wallet.value = 0
        wallet.save()
        item_price = self.default_item1.prices.get(coin=self.world_coin.pk)
        # Act
        response, wallet = self._post_buy_item(wallet, item_price)
        # Assert
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
        self.assertEqual(wallet.value, 0)

    def _post_buy_item(self, wallet, item_price):
        data = {'price': item_price.pk}
        response = self.client.post(get_buy_item_url(self.default_store, self.default_item1), data)
        wallet = Wallet.objects.get(pk=wallet.pk)
        return response, wallet


class SellItemsTestCase(BaseAPITestCase):
    def test_sell_item___store_owner_and_store_staff_user_even_limited_access___201_added_item_at_store(self):
        # Arrange
        self.default_store.is_limited_access = True
        self.default_store.save()
        self.user_a.groups.add(self.default_store.staff_group)
        users = [self.default_user, self.user_a]
        data = {
            'name': 'new_item',
            'prices_set': [
                {'coin_id': self.world_coin.pk, 'value': 100},
                {'coin_id': self.dollar_coin.pk, 'value': 10},
            ]
        }
        # Sub Test
        for user in users:
            with self.subTest(user=user):
                self.client.force_login(user)
                # Act
                response = self.client.post(get_list_items_of_store_url(self.default_store), data, format='json')
                # Assert
                self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
                self.assertTrue('pk' in response.data, response.data)
                new_item = Item.objects.get(pk=response.data['pk'])
                self.assertEqual(data['name'], new_item.name)
                self.assertEqual(self.default_store.pk, new_item.store.pk)
                self.assertEqual(len(data['prices_set']), len(new_item.prices.all()))
                for i in range(len(data['prices_set'])):
                    self.assertEqual(data['prices_set'][i]['coin_id'], new_item.prices.all()[i].coin.pk)
                    self.assertEqual(data['prices_set'][i]['value'], new_item.prices.all()[i].value)

    def test_add_new_price_for_item___one_price___201(self):
        self.user_a.groups.add(self.default_store.staff_group)
        users = [self.default_user, self.user_a]
        target_item = create_item('target_item', self.default_store, [{'coin_id': self.world_coin.pk, 'value': 100}])
        data = {'coin_id': self.yen_coin.pk, 'value': 1000}
        # Sub Test
        for user in users:
            with self.subTest(user=user):
                self.client.force_login(user)
                target_item.prices.filter(coin=data['coin_id']).delete()
                # Act
                response = self.client.post(get_list_prices_of_item_url(target_item), data, format='json')
                # Assert
                self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
                self.assertEqual(data['value'], target_item.prices.get(coin=data['coin_id']).value)

    def test_add_new_price_for_item___some_prices___201(self):
        # Arrange
        target_item = create_item('target_item', self.default_store, [{'coin_id': self.world_coin.pk, 'value': 100}])
        data = [
            {'coin_id': self.yen_coin.pk, 'value': 1000},
            {'coin_id': self.pond_coin.pk, 'value': 11},
        ]
        target_item.prices.filter(coin__in=[data[0]['coin_id'], data[1]['coin_id']]).delete()
        # Act
        response = self.client.post(get_list_prices_of_item_url(target_item), data, format='json')
        # Assert
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(data[0]['value'], target_item.prices.get(coin=data[0]['coin_id']).value)
        self.assertEqual(data[1]['value'], target_item.prices.get(coin=data[1]['coin_id']).value)

    def test_sell_item___send_invalid_parameters___validation_failed(self):
        # Arrange
        test_parameters = [
            {'parameters': {},
             'errors': {'name': 'required', 'prices_set': 'required'}},
            {'parameters': {'name': '', 'prices_set': []},
             'errors': {'name': 'blank'}},
            {'parameters': {'name': {'aa': 'bb'}, 'prices_set': {}},
             'errors': {'name': 'invalid', 'prices_set': {'non_field_errors': 'not_a_list'}}},
            {'parameters': {'name': 'a' * (api_settings.ITEM_MODEL['MAX_LENGTH'] + 1), 'prices_set': []},
             'errors': {'name': 'max_length'}}
        ]
        # Sub Test
        for test_parameter in test_parameters:
            parameters = test_parameter['parameters']
            errors = test_parameter['errors']
            with self.subTest(parameters=parameters, errors=errors):
                # Act
                response = self.client.post(get_list_items_of_store_url(self.default_store), parameters, format='json')
                # Assert
                self.assertEqual(validation_error_status, response.status_code)
                for column, error in response.data.items():
                    self.assertTrue(column in errors.keys(), "{column}: {error}".format(column=column, error=error))
                    if isinstance(errors[column], str):
                        self.assertEqual(error[0].code, errors[column])
                    elif isinstance(errors[column], dict):
                        for key, code in errors[column].items():
                            self.assertEqual(error[key][0].code, code)

    def test_sell_item___send_invalid_prices_set_parameters___validation_failed(self):
        # Arrange
        test_parameters = [
            {'prices_set': [{}, {'value': 1}, {'coin_id': self.world_coin.pk}],
             'errors': [{'value': 'required', 'coin_id': 'required'}, {'coin_id': 'required'}, {'value': 'required'}]},
            {'prices_set': [{'value': 1, 'coin_id': 92929}],
             'errors': [{'coin_id': 'does_not_exist'}]},
            {'prices_set': [{'value': 'a', 'coin_id': self.world_coin.pk}],
             'errors': [{'value': 'invalid'}]}
        ]
        # Sub Test
        for test_parameter in test_parameters:
            parameters = {'name': 'aaa', 'prices_set': test_parameter['prices_set']}
            errors = test_parameter['errors']
            with self.subTest(parameters=parameters, errors=errors):
                # Act
                response = self.client.post(get_list_items_of_store_url(self.default_store), parameters, format='json')
                # Assert
                self.assertEqual(validation_error_status, response.status_code)
                self.assertTrue('prices_set' in response.data)
                for i, error in enumerate(errors):
                    for column, code in error.items():
                        self.assertTrue(column in response.data['prices_set'][i], response.data)
                        self.assertEqual(code, response.data['prices_set'][i][column][0].code, response.data)
