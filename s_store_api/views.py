from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from s_store_api.models import Item, Store, Price
from s_store_api.serialzers import ItemSerializer, PriceSerializer, StoreSerializer
from s_store_api.settings import api_settings
from s_store_api.utils.auth import get_user_or_raise_404, get_users_or_raise_404
from s_store_api.utils.cash_register import create_cash_register_if_store_has_not_each_coin
from s_store_api.utils.common import import_string_from_str_list
from s_store_api.utils.store import buy_item, list_stores, get_staff_user
from s_store_api.utils.views import multi_create, PermissionDeniedResponseConverterMixin
from s_store_api.utils.wallet import create_wallets_if_user_has_not_of_store


class StoreViewSet(PermissionDeniedResponseConverterMixin, viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = import_string_from_str_list(api_settings.STORE_PERMISSION_CLASSES)

    def get_queryset(self):
        return list_stores(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = serializer.data
        if request.GET.get('items', False) == 'true':
            items_serializer = ItemSerializer(instance=instance.items.all(), many=True)
            result['items'] = items_serializer.data
        return Response(result)

    @action(detail=True, methods=['put'])
    def hire_staff(self, request, *args, **kwargs):
        instance = self.get_object()
        staff = get_user_or_raise_404(request.data.get('staff'))
        staff.groups.add(instance.staff_group)
        return Response({'message': 'Success hire the staff.'}, status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def dismiss_staff(self, request, *args, **kwargs):
        instance = self.get_object()
        staff = get_staff_user(request.data.get('staff'), instance)
        staff.groups.remove(instance.staff_group)
        return Response({'message': 'Success dismiss the staff.'}, status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def invite_user_to_limited_access(self, request, *args, **kwargs):
        instance = self.get_object()
        users = get_users_or_raise_404(request.data.get('users'))
        for user in users:
            user.groups.add(instance.limited_customer_group)
        return Response({'message': 'Success invite the user to my store.'}, status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemViewSet(PermissionDeniedResponseConverterMixin, viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = import_string_from_str_list(api_settings.ITEM_PERMISSION_CLASSES)

    def get_queryset(self):
        return Item.objects.filter(store=self.kwargs['store'])

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        create_wallets_if_user_has_not_of_store(request.user,
                                                Store.objects.get(pk=self.kwargs['store']))
        create_cash_register_if_store_has_not_each_coin(Store.objects.get(pk=self.kwargs['store']))

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

    def create(self, request, *args, **kwargs):
        return multi_create(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(item=Item.objects.get(pk=self.kwargs['item']))
