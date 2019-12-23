from django.urls import resolve


def is_request_allowed_only_staff(request):
    url_name = resolve(request.path_info).url_name
    table = {
        'POST': [
            'items-list',
            'prices-list'
        ]
    }
    if request.method not in table:
        return False
    return url_name in table[request.method]


def is_request_allowed_only_management_store_group(request):
    url_name = resolve(request.path_info).url_name
    table = {
        'POST': [
            'stores-list',
        ]
    }
    if request.method not in table:
        return False
    return url_name in table[request.method]
