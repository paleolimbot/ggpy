
import numpy as np

class Facet(object):

    def __init__(self):
        self.shrink = False
        self.params = {}

    def train(self, data, layout):
        self.compute_layout(data, layout, self.params)

    def map(self, data, layout):
        self.map_data(data, layout)

    def render_back(self, data, layout, x_scales, y_scales, theme):
        self.draw_front(data, layout, x_scales, y_scales, theme, self.params)

    def render_panels(self, panels, layout, x_scales, y_scales, ranges, coord, data, theme, labels):
        panels = self.draw_panels(panels, layout, x_scales, y_scales, ranges, coord, data, theme, self.params)
        self.draw_labels(panels, layout, x_scales, y_scales, ranges, coord, data, theme, labels, self.params)

    def train_positions(self, x_scales, y_scales, layout, data):
        self.train_scales(x_scales, y_scales, layout, data, self.params)

    def compute_layout(self, data, params):
        raise NotImplementedError()

    def map_data(self, data, params):
        raise NotImplementedError()

    def init_scales(self, layout, x_scale=None, y_scale=None, params=None):
        scales = {}
        if x_scale is not None:
            scales["x"] = [x_scale.clone() for i in range(max(layout["SCALE_X"]))]
        if y_scale is not None:
            scales["y"] = [y_scale.clone() for i in range(max(layout["SCALE_Y"]))]
        return scales

    def train_scales(self, x_scales, y_scales, layout, data, params):
        layout_ids = np.array(layout["PANEL"])
        for layer_data in data:
            match_id = int(np.argwhere(layout_ids == layer_data["PANEL"]))
            if x_scales is not None:
                x_vars = set(x_scales[0].aesthetics).intersection(set(layer_data.columns))
                


