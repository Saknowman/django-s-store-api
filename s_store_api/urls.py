from django.urls import path, include
from rest_framework import routers

from s_store_api.views import ItemViewSet

router = routers.DefaultRouter()
router.register(r'items', ItemViewSet, 'items')

app_name = 'stores'

urlpatterns = [
    path(r'<store>/', include(router.urls))
]
