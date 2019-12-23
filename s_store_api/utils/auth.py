from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import exceptions

User = get_user_model()


def is_user_in_group(user: User, group: Group):
    return group in user.groups.all()


def get_user_or_raise_404(pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise exceptions.NotFound()
    return user
