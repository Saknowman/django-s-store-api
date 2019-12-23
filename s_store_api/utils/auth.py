from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import exceptions

User = get_user_model()


def is_user_in_group(user: User, group: Group):
    return group in user.groups.all()


def get_user_or_raise_404(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise exceptions.NotFound()


def get_users_or_raise_404(pk_list):
    try:
        result = User.objects.filter(pk__in=pk_list).all()
        if len(result) == len(pk_list):
            return result
        raise exceptions.NotFound()
    except User.DoesNotExist:
        raise exceptions.NotFound()
