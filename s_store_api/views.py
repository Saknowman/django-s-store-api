from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from s_store_api.models import Item, Store, Price
from s_store_api.serialzers import ItemSerializer, PriceSerializer
from s_store_api.settings import api_settings
from s_store_api.utils.common import import_string_from_str_list
from s_store_api.utils.store import buy_item
from s_store_api.utils.views import multi_create, PermissionDeniedResponseConverterMixin
from s_store_api.utils.wallet import create_wallets_if_user_has_not_of_store


class ItemViewSet(PermissionDeniedResponseConverterMixin, viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = import_string_from_str_list(api_settings.ITEM_PERMISSION_CLASSES)

    def get_queryset(self):
        return Item.objects.filter(store=self.kwargs['store'])

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        create_wallets_if_user_has_not_of_store(request.user,
                                                Store.objects.get(pk=self.kwargs['store']))

    @action(detail=True, methods=['post'])
    def buy(self, request, *args, **kwargs):
        item = self.get_object()
        price = item.prices.get(pk=request.data['price'])
        fail_message = buy_item(request.user, item, price)
        if fail_message is None:
            return Response({'message': 'Complete'})
        return Response({'message': fail_message}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(store=Store.objects.get(pk=self.kwargs.get('store')))


class PriceViewSet(PermissionDeniedResponseConverterMixin, viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = import_string_from_str_list(api_settings.ITEM_PERMISSION_CLASSES)

    def initial(self, request, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs['item'])
        request.parser_context['kwargs']['store'] = item.store.pk
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(item=self.kwargs['item'])

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj.item)

    def create(self, request, *args, **kwargs):
        return multi_create(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(item=Item.objects.get(pk=self.kwargs['item']))
