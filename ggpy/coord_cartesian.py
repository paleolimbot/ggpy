
from .coord import Coord
from ._scales.ranges import rescale, squish_infinite, expand_range
from .position import transform_position
import numpy as np


class CoordCartesian(Coord):

    def __init__(self, xlim=None, ylim=None, expand=True):
        Coord.__init__(self)
        self.expand = expand
        self.limits = {"x": xlim, "y": ylim}

    def is_linear(self):
        return True

    def distance(self, x, y, scale_details):
        max_dist = np.linalg.norm(np.array((scale_details['x_range'][0], scale_details['y_range'][0])) -
                                  np.array((scale_details['x_range'][1], scale_details['y_range'][1])))
        return np.linalg.norm(np.array((x[0], y[0])) - np.array((x[1], y[1]))) / max_dist

    def transform(self, data, scale_details):
        data = transform_position(data,
                                  lambda x: rescale(x, from_=scale_details["x"]),
                                  lambda y: rescale(y, from_=scale_details["y"]))
        return transform_position(data, squish_infinite, squish_infinite)

    def train(self, scale_details):
        def train_cartesian(out, scale_details, limits, name):
            expand = self.expand if self.expand else (0, 0)
            if limits is None:
                range = scale_details.dimension(expand)
            else:
                range = expand_range(scale_details.transform(limits), expand[0], expand[1])
            for key, value in scale_details.break_info(range).items():
                out[name + "_" + key] = value

            out[name + "_arrange"] = scale_details.axis_order()

        out = {}
        train_cartesian(out, scale_details, self.limits["x"], "x")
        train_cartesian(out, scale_details, self.limits["y"], "y")
        return out

    def clone(self):
        return type(self)(xlim=self.limits["x"], ylim=self.limits["y"], expand=self.expand)
