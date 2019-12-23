from s_store_api.models import Coin, Store, CashRegister
from s_store_api.utils.coin import get_treated_coins_from_store


def create_cash_register_if_store_has_not(store: Store, coin: Coin):
    if CashRegister.objects.filter(store=store, coin=coin).exists():
        return
    cash_register = CashRegister(store=store, coin=coin)
    cash_register.save()
    return cash_register


def create_cash_register_if_store_has_not_each_coin(store: Store):
    coins = get_treated_coins_from_store(store)
    for coin in coins:
        create_cash_register_if_store_has_not(store, coin)
