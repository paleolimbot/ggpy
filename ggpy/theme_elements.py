
from ._component import Component


class Element(Component):
    def __init__(self, **kwargs):
        Component.__init__(self, **kwargs)

    def _combine_items(self, item1, item2):
        if (type(item1) == Rel and item2 is not None) or type(item2) == Rel and item1 is not None:
            return item1 * item2
        else:
            return item2

    def __radd__(self, other):
        if type(self) == BlankElement:
            return other
        elif type(other) == BlankElement:
            return self
        else:
            return Component.__radd__(self, other)

    def __add__(self, other):
        if type(self) == BlankElement:
            return other
        elif type(other) == BlankElement:
            return self
        else:
            return Component.__add__(self, other)

    def is_complete(self):
        return True


class BlankElement(Element):
    def __init__(self):
        Element.__init__(self)


class LineElement(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

    def is_complete(self):
        return all([e in self for e in ("colour", "size", "linetype", "lineend")])


class RectElement(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

    def is_complete(self):
        return all([e in self for e in ("fill", "colour", "size", "linetype")])


class TextElement(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

    def is_complete(self):
        return all([e in self for e in ("family", "face", "colour", "size", "hjust", "vjust"
                                        "angle", "lineheight", "margin")])


class Rel(float):
    def __new__(cls, val):
        return float.__new__(Rel, val)

    def __mul__(self, other):
        return Rel(float(self) * other) if type(other) == Rel else float(self) * other

    def __rmul__(self, other):
        return self * other

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Rel(%s)" % float(self)


def element_blank():
    return BlankElement()


def element_rect(fill=None, colour=None, size=None, linetype=None):
    # TODO validate types of things that get passed into element_
    return RectElement(fill=fill, colour=colour, size=size, linetype=linetype)


def element_line(colour=None, size=None, linetype=None, lineend=None):
    return LineElement(colour=colour, size=size, linetype=linetype, lineend=lineend)


def element_text(family=None, face=None, colour=None, size=None, hjust=None, vjust=None, 
                 angle=None, lineheight=None, margin=None):
    return TextElement(family=family, face=face, colour=colour, size=size, hjust=hjust,
                       vjust=vjust, angle=angle, lineheight=lineheight, margin=margin)



