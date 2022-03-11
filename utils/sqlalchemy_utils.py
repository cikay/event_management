
def generate_field_value_func(field):
    def get_default(context):
        return context.get_current_parameters()[field]

    return get_default
