from django.urls import path, include
from rest_framework import routers

from s_store_api.routers import CustomPostOnlyRouter
from s_store_api.views import ItemViewSet, PriceViewSet, StoreViewSet

default_router = routers.DefaultRouter()
default_router.register(r'', StoreViewSet, 'stores')

items_router = routers.DefaultRouter()
items_router.register(r'items', ItemViewSet, 'items')

prices_router = CustomPostOnlyRouter()
prices_router.register(r'prices', PriceViewSet, 'prices')


app_name = 'stores'

urlpatterns = [
    path(r'', include(default_router.urls)),
    path(r'<store>/', include(items_router.urls)),
    path(r'items/<item>/', include(prices_router.urls)),
]
