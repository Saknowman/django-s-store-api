from s_store_api.models import Receipt, Price, Store


def issue_receipt(price: Price, store: Store, user=None, num: int = 1):
    item = price.item
    receipt = Receipt(item=item, store=store, store_name=store.name, user=user)
    receipt.item_name = item.name
    receipt.item_num = num
    receipt.item_price = "{value}{coin}".format(value=price.value, coin=price.coin.name)
    receipt.save()
    return receipt
