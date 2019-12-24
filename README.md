# django-s-store-api

**django-s-store-api** is a simple store rest api of django.

## Installation
To install django-s-store-api like this:
```shell script
pip install django-s-store-api 
```

## Configuration
We need to hook **django-s-store-api** into our project.
1. Put s_store_api into your INSTALLED_APPS at settings module:
    ```python:project/settings.py
    INSTALLED_APPS = (
        ...,
        's_store_api',
    )
    ```
   
2. Create **s_store_api** database table by running:
    ```shell script
    python manage.py migrate
    ```
   
3. Add url patterns at project.urls module:
    ```python:project/urls.py
    from s_store_api import urls as s_store_api_urls

    urlpatterns = [
        ...,
        path(r'api/stores/', include(s_store_api_urls))
    ]
    ```
   
## API
### List stores
Show list stores which are allowed to access by login user.
 
```text
method: GET
url: /api/stores/
name: s-stores:stores-list
view: StoreViewSet
```

### Detail store
Show detail of target store.  
Show detail with store items, if items parameter is true.
```text
method: GET
url: /api/stores/<pk>/[?items=true]
name: s-stores:stores-detail
view: StoreViewSet
```

### Open store
Open your store.  
Invite user to allow access store, when set true at is_limited_access

```text
method: POST
url: /api/stores/
parameters: 
{
    'name': 'store name', 
    'is_limited_access': True
}
name: s-stores:stores-list
view: StoreViewSet
```

### Close store
Close your store.
```text
method: DELETE
url: /api/stores/<pk>/
name: s-stores:stores-detail
view: StoreViewSet
```

### Update store's info
Update your store's information
```text
method: PUT/PATCH
url: /api/stores/<pk>/
parameters: 
{
    'name': 'changed store name', 
    'is_limited_access': False
}
name: s-stores:stores-detail
view: StoreViewSet
```


### Hire staff
Hire staff.
```text
method: PUT
url: /api/stores/<pk>/hire_staff/
parameters: 
{
    'staff': 2 (user's id)
}
name: s-stores:stores-hire-staff
view: StoreViewSet
```

### Dismiss staff
Dismiss staff.
```text
method: PUT
url: /api/stores/<pk>/dismiss_staff/
parameters: 
{
    'staff': 2 (user's id)
}
name: s-stores:stores-dismiss-staff
view: StoreViewSet
```

### Invite user
Invite user to limited access store  
Request parameter's format should be json.
```text
method: PUT
url: /api/stores/<pk>/invite_user_to_limited_access/
parameters: 
{
    'users': [
        2 (user's id),
        4
    ]
}
name: s-stores:stores-invite-user-to-limited-access
view: StoreViewSet
```

### List items
List items at store
```text
method: GET
url: /api/stores/<store>/items/
name: s-stores:items-list
view: ItemViewSet
```


### Detail item
Detail item at store
```text
method: GET
url: /api/stores/<store>/items/<pk>/
name: s-stores:items-detail
view: ItemViewSet
```


### Buy item
Buy item from store.
You received item in bag and receipt.
```text
method: POST
url: /api/stores/<store>/items/{pk}/buy/
parameters: 
{
    'price': 2 (item.price.pk)
}
name: s-stores:items-buy
view: ItemViewSet
```

### Sell item
Sell item to store.
Request parameter's format should be json.
```text
method: POST
url: /api/stores/<store>/items/
parameters: 
{
    'name': 'new_item',
    'prices_set': [
        {'coin_id': 2 (coin.pk), 'value': 100},
        {'coin_id': 3 (coin.pk), 'value': 10},
    ]
}
name: stores:items-list
view: ItemViewSet
```


### Set prices
Set prices to exists item.
Request parameter's format should be json.
```text
method: POST
url: /api/stores/items/<item>/prices
parameters: 
[
    {'coin_id': 4 (coin.pk), 'value': 1000},
    {'coin_id': 5 (coin.pk), 'value': 11},
]
name: s-stores:prices-list
view: PriceViewSet
```
