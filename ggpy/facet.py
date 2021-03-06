
from .layout import scale_apply
from ._grob.grob import ZeroGrob
import numpy as np
import pandas as pd


class Facet(object):

    def __init__(self, shrink=False):
        self.shrink = shrink
        self.params = {}

    def train(self, data, params):
        return self.compute_layout(data, params)

    def map(self, data, layout):
        return self.map_data(data, layout, self.params)

    def render_back(self, data, layout, x_scales, y_scales, theme):
        self.draw_front(data, layout, x_scales, y_scales, theme, self.params)

    def render_panels(self, panels, layout, x_scales, y_scales, ranges, coord, data, theme, labels):
        panels = self.draw_panels(panels, layout, x_scales, y_scales, ranges, coord, data, theme, self.params)
        self.draw_labels(panels, layout, x_scales, y_scales, ranges, coord, data, theme, labels, self.params)

    def train_positions(self, x_scales, y_scales, layout, data):
        self.train_scales(x_scales, y_scales, layout, data, self.params)

    def compute_layout(self, data, params):
        raise NotImplementedError()

    def map_data(self, data, layout, params):
        raise NotImplementedError()

    def init_scales(self, layout, x_scale=None, y_scale=None, params=None):
        scales = {}
        # need to use zero-based indicies for scales, so therefore need max(scale_x)+1
        if x_scale is not None:
            scales["x"] = [x_scale.clone() for i in range(max(layout["SCALE_X"])+1)]
        if y_scale is not None:
            scales["y"] = [y_scale.clone() for i in range(max(layout["SCALE_Y"])+1)]
        return scales

    def train_scales(self, x_scales, y_scales, layout, data, params):
        layout_ids = list(layout["PANEL"])
        for layer_data in data:
            if len(data) == 0:
                match_id = []
            else:
                match_id = [layout_ids.index(el) for el in layer_data["PANEL"]]
            if x_scales is not None:
                x_vars = set(x_scales[0].aesthetics).intersection(set(layer_data.columns))
                SCALE_X = layout["SCALE_X"][match_id]
                scale_apply(layer_data, x_vars, "train", SCALE_X, x_scales)
            if y_scales is not None:
                y_vars = set(y_scales[0].aesthetics).intersection(set(layer_data.columns))
                SCALE_Y = layout["SCALE_Y"][match_id]
                scale_apply(layer_data, y_vars, "train", SCALE_Y, y_scales)

    def draw_back(self, data, layout, x_scales, y_scales, theme, params):
        return [ZeroGrob(), ] * len(set(layout["PANEL"]))

    def draw_front(self, data, layout, x_scales, y_scales, theme, params):
        return [ZeroGrob(), ] * len(set(layout["PANEL"]))

    def draw_panels(self, panels, layout, x_scales, y_scales, ranges, coord, data, theme, params):
        raise NotImplementedError()

    def draw_labels(self, panels, layout, x_scales, y_scales, ranges, coord, data, theme, labels, params):
        # it looks like the GTable panels is created by draw_panels and modified by this function

        xlab_height_top = labels["x"][0].height()
        panels.add_row(xlab_height_top, 0)
        panels.add_grob(labels["x"][0], l=-1, t=0, r=panels.ncol()-1, b=0,
                        clip="off", name="xlab-t")

        xlab_height_bottom = labels["x"][1].height()
        panels.add_row(xlab_height_bottom)
        panels.add_grob(labels["x"][1], l=-1, t=panels.nrow()-1, r=panels.ncol()-1, b=panels.nrow()-1,
                        clip="off", name="xlab-b")

        ylab_width_left = labels["y"][0].width()
        panels.add_col(ylab_width_left, 0)
        panels.add_grob(labels["y"][0], l=0, t=0, r=0, b=panels.nrow(),
                        clip="off", name="ylab-l")

        ylab_width_right = labels["y"][1].width()
        panels.add_col(ylab_width_right)
        panels.add_grob(labels["y"][1], l=panels.ncol()-1, t=0, r=panels.ncol()-1, b=panels.nrow(),
                        clip="off", name="ylab-r")

        return panels

    def setup_params(self, data, params):
        return params

    def setup_data(self, data, params):
        return data

    def finish_data(self, data, layout, x_scales, y_scales, params):
        return data

    def clone(self):
        newobj = type(self)(shrink=self.shrink)
        newobj.params = self.params.copy()
        return newobj


def layout_null():
    # need to use zero-based indicies or things get a little crazy
    return pd.DataFrame({"PANEL": [0, ], "ROW": [0, ], "COL": [0, ], "SCALE_X": [0, ], "SCALE_Y": [0, ]})
