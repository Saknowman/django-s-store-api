
# Register your models here.
from django.contrib import admin

from s_store_api.models import Store, Item

admin.site.register(Store)
admin.site.register(Item)