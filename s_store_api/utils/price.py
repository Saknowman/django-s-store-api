from s_store_api.serialzers import PriceSerializer


def create_prices(prices_set, item):
    validated_data_list_for_price = []
    for price_set in prices_set:
        if 'coin_id' in price_set:
            validated_data_list_for_price.append(price_set)
            continue
        validated_data_list_for_price.append({'value': price_set['value'], 'coin_id': price_set['coin'].pk})
    price_serializer = PriceSerializer(data=validated_data_list_for_price, many=True)
    price_serializer.is_valid(raise_exception=True)
    price_serializer.save(item=item)
