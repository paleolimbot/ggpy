
from ._component import Component


class Theme(Component):

    def __init__(self, complete=False, validate=True, **kwargs):
        super(Theme, self).__init__(**kwargs)
        self.complete = complete
        self.validate = validate

    def __repr__(self):
        return "Theme(complete=%s, validate=%s, %s)" % \
               (self.complete, self.validate,
                ", ".join(["%s='%s'" % (key, value) for key, value in self.items()]))


def theme(**kwargs):
    return Theme(**kwargs)