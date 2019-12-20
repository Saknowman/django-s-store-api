from django.utils.module_loading import import_string


def get_next_usable_pk(model):
    last_model = model.objects.last()
    result = 1 if not last_model else last_model.pk + 1
    return result


def import_string_from_str_list(str_classes: list) -> list:
    return [import_string(permission_str_class) for permission_str_class in str_classes]
