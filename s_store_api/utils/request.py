from django.urls import resolve


def is_request_allowed_only_staff(request):
    url_name = resolve(request.path_info).url_name
    table = {
        'POST': [
            'items-list',
            'prices-list'
        ]
    }
    return _is_request_match_the_pattern(request, table, url_name)


def is_request_allowed_only_management_store_group(request):
    url_name = resolve(request.path_info).url_name
    table = {
        'POST': [
            'stores-list',
        ],
        'PUT': [
            'stores-detail',
        ],
        'PATCH': [
            'stores-detail',
        ],
        'DELETE': [
            'stores-detail',
        ]
    }
    return _is_request_match_the_pattern(request, table, url_name)


def is_request_allowed_only_store_owner(request):
    url_name = resolve(request.path_info).url_name
    table = {
        'PUT': [
            'stores-detail',
        ],
        'PATCH': [
            'stores-detail',
        ],
        'DELETE': [
            'stores-detail',
        ]
    }
    return _is_request_match_the_pattern(request, table, url_name)


def _is_request_match_the_pattern(request, table, url_name):
    if request.method not in table:
        return False
    return url_name in table[request.method]
