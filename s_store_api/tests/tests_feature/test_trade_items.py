from rest_framework import status

from s_store_api.models import Wallet
from s_store_api.tests.utils import BaseAPITestCase, get_list_items_of_store_url, get_buy_item_url
from s_store_api.utils.coin import get_treated_coins_from_store
from s_store_api.utils.wallet import create_wallet_if_user_has_not


class BuyItemsTestCase(BaseAPITestCase):
    def test_access_store___has_no_wallet___wallet_created(self):
        # Arrange
        Wallet.objects.filter(user=self.default_user).delete()
        treated_coins = get_treated_coins_from_store(self.default_store)
        # Act
        response = self.client.get(get_list_items_of_store_url(self.default_store))
        # Assert
        wallets = Wallet.objects.filter(user=self.default_user).all()
        self.assertFalse(len(wallets) == 0, wallets)
        for wallet in wallets:
            self.assertTrue(wallet.coin in treated_coins)

    def test_access_store___permission_failed___wallet_not_created(self):
        # Arrange
        Wallet.objects.filter(user=self.default_user).delete()
        self.client.logout()
        # Act
        response = self.client.get(get_list_items_of_store_url(self.default_store))
        # Assert
        wallets = Wallet.objects.filter(user=self.default_user).all()
        self.assertTrue(len(wallets) == 0, wallets)

    def test_buy_item___has_enough_money___payed_and_get(self):
        # Arrange
        default_value = 1000000
        wallet = create_wallet_if_user_has_not(self.default_user, self.world_coin)
        wallet.value = default_value
        wallet.save()
        item_price = self.default_item1.prices.get(coin=self.world_coin.pk)
        # Act
        response, wallet = self._post_buy_item(wallet, item_price)
        bag = self.default_user.bags.get(item=self.default_item1.pk)
        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(default_value - item_price.value, wallet.value)
        self.assertEqual(1, bag.amount)

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
