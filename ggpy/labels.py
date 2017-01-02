
from ._component import Component
from .aes import rename_aes, is_function_aes
from .aes_calculated import is_calculated_aes, strip_dots


class Labels(Component):

    def __init__(self, **kwargs):
        super(Labels, self).__init__(**kwargs)


def labs(**kwargs):
    return Labels(**rename_aes(kwargs))


def make_labels(mapping):
    dlabs = {}
    for key, value in mapping:
        if is_function_aes(value):
            dlabs[key] = value
        elif is_calculated_aes(value):
            dlabs[key] = strip_dots(value)
        else:
            dlabs[key] = key
    return Labels(**dlabs)