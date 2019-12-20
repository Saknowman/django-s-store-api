from s_store_api.utils.auth import User


def create_bag_if_user_has_not(user: User, item):
    from s_store_api.models import Bag
    query = Bag.objects.filter(user=user, item=item)
    if query.exists():
        return query.get()
    bag = Bag(user=user, item=item)
    bag.save()
    return bag
