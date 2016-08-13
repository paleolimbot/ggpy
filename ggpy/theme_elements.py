
from ._component import Component


class Element(Component):
    def __init__(self, element_type=None, **kwargs):
        if element_type not in ("blank", "rect", "line", "text", None):
            raise ValueError("Invalid element type: %s" % element_type)
        Component.__init__(self, **kwargs)
        self.element_type = element_type

    def __add__(self, other):
        try:
            if self.element_type == "blank":
                return other
            elif other.element_type == "blank":
                return Element(self.element_type, **self)
            elif self.element_type != other.element_type:
                raise ValueError("Cannot add elements of different type")
        except AttributeError:
            pass
        return super(Element, self).__add__(other)

    def __radd__(self, other):
        try:
            if self.element_type == "blank":
                return other
            elif other.element_type == "blank":
                return Element(self.element_type, **self)
            elif self.element_type != other.element_type:
                raise ValueError("Cannot add elements of different type")
        except AttributeError:
            pass
        return super(Element, self).__radd__(other)

    def is_complete(self):
        if self.element_type == "rect":
            return all([e in self for e in ("fill", "colour", "size", "linetype")])
        elif self.element_type == "line":
            return all([e in self for e in ("colour", "size", "linetype", "lineend")])
        elif self.element_type == "text":
            return all([e in self for e in ("family", "face", "colour", "size", "hjust", "vjust"
                              "angle", "lineheight", "margin")])
        elif self.element_type == "blank":
            return True

    def __repr__(self):
        return "Element('%s', %s)" % (self.element_type,
                                      ", ".join(["%s='%s'" % (key, value) for key, value in self.items()]))


def element_blank():
    return Element("blank")

def element_rect(fill=None, colour=None, size=None, linetype=None):
    return Element("rect", fill=fill, colour=colour, size=size, linetype=linetype)

def element_line(colour=None, size=None, linetype=None, lineend=None):
    return Element("line", colour=colour, size=size, linetype=linetype, lineend=lineend)

def element_text(family=None, face=None, colour=None, size=None, hjust=None, vjust=None, 
                 angle=None, lineheight=None, margin=None):
    return Element("text", family=family, face=face, colour=colour, size=size, hjust=hjust,
                   vjust=vjust, angle=angle, lineheight=lineheight, margin=margin)



