from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


def is_user_in_group(user: User, group: Group):
    return group in user.groups.all()
