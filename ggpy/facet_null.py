
from .facet import Facet, layout_null
from ._grob.gtable import GTable
from ._grob.grob import ZeroGrob
from ._grob.unit import concatenate_units, Unit
import pandas as pd


class FacetNull(Facet):

    def __init__(self, shrink=True):
        Facet.__init__(self, shrink=shrink)

    def compute_layout(self, data, params):
        return layout_null()

    def map_data(self, data, layout, params):
        if len(data) > 0:
            data["PANEL"] = 1
        else:
            pd.DataFrame({}, columns=list(data.columns) + ["PANEL", ])

    def draw_panels(self, panels, layout, x_scales, y_scales, ranges, coord, data, theme, params):
        range = ranges[0]
        aspect_ratio = getattr(theme, "aspect_ratio", default=coord.aspect(range))
        if aspect_ratio is None:
            aspect_ratio = 1
            respect = False
        else:
            respect = True

        axis_h = coord.render_axis_h(range, theme)
        axis_v = coord.render_axis_v(range, theme)

        grb = [[ZeroGrob(), axis_h["top"], ZeroGrob()],
               [axis_v["left"], ZeroGrob(), axis_v["right"]],
               [[ZeroGrob(), axis_h["bottom"], ZeroGrob()]]]
        z = [[5, 6, 4],
             [7, 1, 8],
             [3, 9, 2]]
        widths = concatenate_units(axis_v["left"].width(), Unit(1, "null"), axis_v["right"])
        heights = concatenate_units(axis_h["top"].height(), Unit(aspect_ratio, "null"), axis_h["bottom"].height())
        names = [["spacer", "axis-l", "spacer"],
                 ["axis-t", "panel", "axis-b"],
                 ["spacer", "axis-r", "spacer"]]
        clip = [["off", "off", "off"],
                ["off", "off", "off"],
                ["off", "off", "off"]]
        layout = GTable.matrix("layout", grb, names=names, widths=widths,
                        heights=heights, respect=respect, clip=clip, z=z)
        return layout

    def vars(self):
        return ""
