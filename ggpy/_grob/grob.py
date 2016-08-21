
from .._component import Component
import numpy as np
import tkinter.font as font

_pt = 72.27 / 25.4
_stroke = 96 / 25.4


class GPar(Component):
    def __init__(self, **kwargs):
        Component.__init__(self, **kwargs)


def gpar(**kwargs):
    return GPar(**kwargs)


class Grob(object):

    def __init__(self):
        pass

    def width(self):
        mn, mx = self.range_x()
        return mx - mn

    def height(self):
        mn, mx = self.range_y()
        return mx - mn

    def range_x(self):
        raise NotImplementedError()

    def range_y(self):
        raise NotImplementedError()

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, repr(self.__dict__))


class GTree(Grob):

    def __init__(self, *children, name=None):
        Grob.__init__(self)
        self.children = children
        self.name = name

    def range_x(self):
        pass

    def range_y(self):
        pass

class ZeroGrob(Grob):

    def __init__(self):
        Grob.__init__(self)

    def range_x(self):
        return 0, 0

    def range_y(self):
        return 0, 0

    def draw_details(self, recording):
        return None


class PointsGrob(Grob):

    def __init__(self, x, y, pch, gp):
        Grob.__init__(self)
        self.x = x
        self.y = y
        self.pch = pch
        self.gp = gp


class RectGrob(Grob):

    def __init__(self, x, y, width, height, gp):
        Grob.__init__(self)
        self.x = x
        self.y = y
        self.width_ = width
        self.height_ = height
        self.gp = gp

    def range_x(self):
        return self.x, self.x + self.width_

    def range_y(self):
        return self.y, self.y + self.height_


class PolylineGrob(Grob):

    def __init__(self, x, y, default_units, gp, id_lengths):
        Grob.__init__(self)
        self.x = x
        self.y = y
        self.default_units = default_units
        self.gp = gp
        self.id_lengths = id_lengths

    def range_x(self):
        return np.nanmin(self.x), np.nanmax(self.x)

    def range_y(self):
        return np.nanmin(self.y), np.nanmax(self.y)


class TextGrob(Grob):

    def __init__(self, label, x, y, hjust, vjust, angle, gp, expand_x, expand_y):
        Grob.__init__(self)
        self.x = x
        self.y = y
        self.label = label
        self.hjust = hjust
        self.vjust = vjust
        self.angle = angle
        self.gp = gp
        self.expand_x = expand_x
        self.expand_y = expand_y
        # need fonts for measuring
        self._tkfont = font.Font(family=gp['family'], size=gp['fontsize'])
        self._width = self._height = None
        self._measure()

    def _measure(self):
        # probably need to correct for DPI...
        self._width, self._height = self._tkfont.measure(self.label), self._tkfont.metrics('linespace')

    def height(self):
        return self._height

    def width(self):
        return self._width

    def range_x(self):
        w = self._width
        mx = self.x - self.hjust * w
        return mx, mx + w

    def range_y(self):
        h = self._height
        my = self.y - self.vjust * h
        return my, my + h