# Register your models here.
from django.contrib import admin

from s_store_api.models import Store, Item, Coin, Price

admin.site.register(Coin)
admin.site.register(Price)


class PriceInline(admin.TabularInline):
    model = Price


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'store']
    inlines = [PriceInline]


class ItemInline(admin.TabularInline):
    model = Item


class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    inlines = [ItemInline]


admin.site.register(Item, ItemAdmin)

admin.site.register(Store, StoreAdmin)
