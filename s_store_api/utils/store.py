from django.contrib.auth.models import Group


def get_default_limited_customer_group():
    last_group = Group.objects.last()
    next_pk = 1 if not last_group else last_group.pk + 1
    group = Group()
    group.name = 'store__limited_customer_group__' + str(next_pk)
    group.save()
    return group.pk
