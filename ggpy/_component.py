

class Component(dict):

    def __init__(self, **kwargs):
        super(dict, self).__init__()
        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key, value):
        if value is not None:
            super(Component, self).__setitem__(key, value)
        elif value is None and key in self:
            del self[key]
        else:
            pass

    def _combine_items(self, item1, item2):
        return item2

    def __add__(self, other):
        if not (type(other) == dict or type(self) == type(other)):
            raise ValueError("Cannot add %s to type %s" % (type(self).__name__, type(other).__name__))
        nd = dict(self)
        for key, value in other.items():
            newval = self._combine_items(nd[key] if key in nd else None, value)
            if newval is not None:
                nd[key] = newval
        return type(self)(**nd)

    def __radd__(self, other):
        if not (type(other) == dict or type(self) == type(other)):
            raise ValueError("Cannot add %s to type %s" % (type(self).__name__, type(other).__name__))
        nd = dict(other)
        for key, value in self.items():
            newval = self._combine_items(nd[key] if key in nd else None, value)
            if newval is not None:
                nd[key] = newval
        return type(self)(**nd)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, ", ".join(["%s='%s'" % (key, value) for key, value in self.items()]))