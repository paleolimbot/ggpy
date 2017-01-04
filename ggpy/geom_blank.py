
from .geom import Geom
from ._grob.grob import NullGrob


class GeomBlank(Geom):

    def __init__(self):
        Geom.__init__(self)

    def handle_na(self, data, params):
        return data

    def draw_panel(self, data, panel_scales, coord, params):
        return NullGrob()