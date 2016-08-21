
from ._component import Component
from ._grob.grob import gpar, ZeroGrob, RectGrob, PolylineGrob, TextGrob, _pt


class Element(Component):

    def __init__(self, **kwargs):
        Component.__init__(self, **kwargs)

    def render(self, **kwargs):
        raise NotImplementedError()

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

    def render(self, **kwargs):
        return ZeroGrob()


class LineElement(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

    def render(self, x=(0, 1), y=(0, 1), colour=None, size=None, linetype=None, lineend=None,
               default_units="npc", id_lengths=None, **kwargs):
        gp = gpar(lwd=None if size is None else size * _pt, col=colour, lty=linetype, lineend=lineend)
        element_gp = gpar(lwd=None if self['size'] is None else self['size'] * _pt, col=self['colour'],
                          lty=self['linetype'], lineend=self['lineend'])
        return PolylineGrob(x, y, default_units=default_units, gp=element_gp + gp,
                            id_lengths=id_lengths)

    def is_complete(self):
        return all([e in self for e in ("colour", "size", "linetype", "lineend")])


class RectElement(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

    def render(self, x=0.5, y=0.5, width=1, height=1, fill=None, colour=None, size=None, linetype=None, **kwargs):
        gp = gpar(lwd=None if size is None else size * _pt, col=colour, fill=fill, lty=linetype)
        element_gp = gpar(lwd=None if self['size'] is None else self['size']*_pt, col=self['colour'],
                          fill=self['fill'], lty=self['linetype'])
        return RectGrob(x, y, width, height, gp=element_gp + gp)

    def is_complete(self):
        return all([e in self for e in ("fill", "colour", "size", "linetype")])


class TextElement(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

    def render(self, label = "", x = 0, y = 0, family = None, face = None, colour = None,
               size = None, hjust = None, vjust = None, angle = None, lineheight = None,
               margin = None, expand_x = False, expand_y = False, **kwargs):
        if label is None:
            return ZeroGrob()
        gp = gpar(fontsize=size, col=colour, fontfamily=family, fontface=face, lineheight=lineheight)
        element_gp = gpar(fontsize=self['size'], col=self['colour'], fontfamily=self['family'],
                          fontface=self['face'], lineheight=self['lineheight'])
        hjust = self['hjust'] if hjust is None else hjust
        vjust = self['vjust'] if vjust is None else vjust
        angle = self['angle'] if angle is None else angle

        return TextGrob(label, x, y, hjust=hjust, vjust=vjust, angle=angle, gp=element_gp + gp,
                        expand_x=expand_x, expand_y=expand_y)

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
