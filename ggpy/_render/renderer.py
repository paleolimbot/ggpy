
from .._grob.grob import PointsGrob, PolylineGrob, RectGrob, ZeroGrob, TextGrob, GTree


class Renderer(object):

    def __init__(self):
        pass

    def render_html(self, grob):
        raise NotImplementedError()

    def render_png(self, grob):
        raise NotImplementedError()

    def render_grob(self, grob):
        ty = type(grob)
        if ty == GTree:
            for child in grob.children:
                self.render_grob(child)
        elif ty == ZeroGrob:
            self.render_zero(grob)
        elif ty == TextGrob:
            self.render_title(grob)
        elif ty == RectGrob:
            self.render_rect(grob)
        elif ty == PolylineGrob:
            self.render_polyline(grob)
        elif ty == PointsGrob:
            self.render_points(grob)
        else:
            raise NotImplementedError("Don't know how to render a %s" % type(grob).__name__)

    def render_title(self, grob):
        raise NotImplementedError()

    def render_rect(self, grob):
        raise NotImplementedError()

    def render_polyline(self, grob):
        raise NotImplementedError()

    def render_zero(self, grob):
        pass

    def render_points(self, grob):
        raise NotImplementedError()