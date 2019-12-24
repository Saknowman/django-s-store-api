from s_store_api.models import Store, Item


def get_treated_coins_from_store(store: Store):
    result = []
    items = store.items.all()
    for item in items:
        result.extend(get_treated_coins_from_item(item))
    return list(set(result))


def get_treated_coins_from_item(item: Item):
    result = []
    prices = item.prices.all()
    for price in prices:
        result.append(price.coin)
    return list(set(result))



