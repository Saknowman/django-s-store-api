from django.http import Http404
from django.utils.module_loading import import_string
from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from s_store_api.models import Item, Store, Price
from s_store_api.serialzers import ItemSerializer, PriceSerializer
from s_store_api.settings import api_settings
from s_store_api.utils.store import buy_item
from s_store_api.utils.views import multi_create
from s_store_api.utils.wallet import create_wallets_if_user_has_not_of_store


def _array_permission_classes(permission_str_classes: list) -> list:
    return [import_string(permission_str_class) for permission_str_class in permission_str_classes]


class Response403To401Mixin:
    # noinspection PyMethodMayBeStatic
    def permission_denied(self, request, message=None):
        if message is None:
            raise Http404
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message)


class ItemViewSet(Response403To401Mixin, viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = _array_permission_classes(api_settings.ITEM_PERMISSION_CLASSES)

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
        success = buy_item(request.user, item, price)
        if success:
            return Response({'message': 'success'})
        return Response({'message': "That's not enough."}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(store=Store.objects.get(pk=self.kwargs.get('store')))


class PriceViewSet(Response403To401Mixin, viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = _array_permission_classes(api_settings.ITEM_PERMISSION_CLASSES)

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
