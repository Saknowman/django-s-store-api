from s_store_api.models import Coin, Store, Wallet
from s_store_api.utils.auth import User
from s_store_api.utils.coin import get_treated_coins_from_store


def create_wallet_if_user_has_not(user: User, coin: Coin):
    if Wallet.objects.filter(user=user, coin=coin).exists():
        return
    wallet = Wallet(user=user, coin=coin)
    wallet.save()
    return wallet


def create_wallets_if_user_has_not_of_store(user: User, store: Store):
    coins = get_treated_coins_from_store(store)
    for coin in coins:
        create_wallet_if_user_has_not(user, coin)

