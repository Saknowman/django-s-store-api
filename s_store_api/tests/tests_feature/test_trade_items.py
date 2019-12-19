from django.urls import reverse
from rest_framework import status

from s_store_api.models import Store, Item, Wallet
from s_store_api.tests.utils import BaseAPITestCase, get_list_items_of_store_url, get_detail_item_url
from s_store_api.utils.coin import get_treated_coins_from_store


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
