
from ._component import Component
from .theme_elements import Element, TextElement, RectElement, LineElement, Rel


class Theme(Component):

    def __init__(self, complete=False, validate=True, **kwargs):
        super(Theme, self).__init__(**kwargs)
        self.complete = complete
        self.validate = validate

    def element(self, name):
        item = self[name]
        if type(item) == TextElement:
            return self["text"] + item
        elif type(item) == LineElement:
            return self["line"] + item
        elif type(item) == RectElement:
            return self["rect"] + item
        else:
            return item

    def _combine_items(self, item1, item2):
        if isinstance(item1, Element) and isinstance(item2, Element):
            return item1 + item2
        elif (type(item1) == Rel and item2 is not None) or type(item2) == Rel and item1 is not None:
            return item1 * item2
        else:
            return item2

    def __repr__(self):
        return "Theme(complete=%s, validate=%s, %s)" % \
               (self.complete, self.validate,
                ", ".join(["%s='%s'" % (key, value) for key, value in self.items()]))


def theme(**kwargs):
    return Theme(**kwargs)