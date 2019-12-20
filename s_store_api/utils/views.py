from django.db import transaction
from rest_framework import status
from rest_framework.response import Response


def multi_create(view_set, request, *args, **kwargs):
    with transaction.atomic():
        serializer = view_set.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        view_set.perform_create(serializer)
        headers = view_set.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
