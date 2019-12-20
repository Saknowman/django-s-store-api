def get_next_usable_pk(model):
    last_model = model.objects.last()
    result = 1 if not last_model else last_model.pk + 1
    return result
