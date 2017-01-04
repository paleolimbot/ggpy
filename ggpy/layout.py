
from .coord_flip import CoordFlip
from .coord_polar import CoordPolar
from ._grob.grob import GTree, ZeroGrob
from ._na import is_nan
from .utilities import Waiver
import numpy as np


class Layout(object):

    def __init__(self, facet, panel_layout=None, panel_scales=None, panel_ranges=None):
        self.facet = facet
        self.panel_layout = panel_layout
        self.panel_scales = panel_scales if panel_scales is not None else {}
        self.panel_ranges = panel_ranges

    def setup(self, data, plot_data, plot_globals, plot_locals, plot_coord):
        # data is a list here
        # not sure if this is necessary
        data.insert(0, plot_data)

        # the R implementation has self.facet.params containing references to everything
        # in the plot environment (plot.global_vars, plot.local_vars)
        # skipping this
        self.facet.params = self.facet.setup_params(data, self.facet.params)
        data = self.facet.setup_data(data, self.facet.params)
        self.panel_layout = self.facet.train(data, self.facet.params)
        missingcols = [col for col in ("PANEL", "SCALE_X", "SCALE_Y") if col not in self.panel_layout.columns]
        if missingcols:
            raise ValueError("Facet panel layout has bad format. Missing columns: " + ", ".join(missingcols))
        # Special case of CoordFlip - switch the layout scales
        if isinstance(plot_coord, CoordFlip):
            scales = self.panel_layout[["SCALE_X", "SCALE_Y"]]
            self.panel_layout["SCALE_X"] = scales["SCALE_Y"]
            self.panel_layout["SCALE_Y"] = scales["SCALE_X"]

        return data[1:]

    def map(self, data):
        # is a list of DataFrames here (one for each layer)
        return [self.facet.map(d, self.panel_layout) for d in data]

    def render(self, panels, data, coord, theme, labels):
        below = self.facet.render_back(data, self.panel_layout, self.panel_scales["x"], self.panel_scales["y"], theme)
        above = self.facet.render_front(data, self.panel_layout, self.panel_scales["x"], self.panel_scales["y"], theme)

        newpanels = []
        for i in range(len(panels[0])):
            fg = coord.render_fg(self.panel_ranges[i], theme)
            bg = coord.render_fg(self.panel_ranges[i], theme)
            panel = [panel[i] for panel in panels]
            panel = [below[i], ] + panel + [above[i], ]
            if theme["panel_ontop"]:
                panel = panel + [bg, ] + [fg, ]
            else:
                panel = [bg, ] + panel + [fg, ]
            newpanels.append(GTree(*panel, name="panel-%s" % i))
        labels = coord.labels({"x": self.xlabel(labels), "y": self.ylabel(labels)})
        labels = self.render_labels(labels, theme)
        return self.facet.render_panels(panels, self.panel_layout, self.panel_scales["x"],
                                        self.panel_scales["y"], self.panel_ranges, coord, data, theme, labels)

    def train_position(self, data, x_scale, y_scale):
        layout = self.panel_layout
        if "x" not in self.panel_scales:
            self.panel_scales["x"] = self.facet.init_scales(layout, x_scale=x_scale, params=self.facet.params)["x"]
        if "y" not in self.panel_scales:
            self.panel_scales["y"] = self.facet.init_scales(layout, y_scale=y_scale, params=self.facet.params)["y"]
        return self.facet.train_positions(self.panel_scales["x"], self.panel_scales["y"], layout, data)

    def reset_scales(self):
        if self.facet.shrink:
            return
        if "x" in self.panel_scales:
            for s in self.panel_scales["x"]:
                s.reset()
        if "y" in self.panel_scales:
            for s in self.panel_scales["y"]:
                s.reset()

    def map_position(self, data):
        layout = self.panel_layout

        for layer_data in data:
            xvars = set(self.panel_scales["x"][0].aesthetics).intersection(set(layer_data.columns))
            yvars = set(self.panel_scales["y"][0].aesthetics).intersection(set(layer_data.columns))
            panels = list(layout["PANEL"])
            match_id = [panels.index(el) for el in layer_data["PANEL"]]
            pieces_x = scale_apply(layer_data, xvars, "map", layout["SCALE_X"][match_id], self.panel_scales["x"])
            pieces_y = scale_apply(layer_data, xvars, "map", layout["SCALE_Y"][match_id], self.panel_scales["y"])
            # todo: currently modifies data
            for col in pieces_x.keys():
                layer_data[col] = np.concatenate(*pieces_x[col])
            for col in pieces_y.keys():
                layer_data[col] = np.concatenate(*pieces_y[col])

        return data

    def finish_data(self, data):
        return [self.facet.finish_data(layer_data, self.panel_layout, self.panel_scales["x"],
                                       self.panel_scales["y"], self.facet.params) for layer_data in data]

    def get_scales(self, i):
        for p in range(len(self.panel_layout)):
            if self.panel_layout["PANEL"][p] == i:
                # scales may not exist yet? the call to scales_add_missing comes after the first call
                # to this
                sx = self.panel_scales["x"][self.panel_layout["SCALE_X"][p]] if "x" in self.panel_scales else None
                sy = self.panel_scales["y"][self.panel_layout["SCALE_Y"][p]] if "y" in self.panel_scales else None
                return {"x": sx, "y": sy}
        return {"x": None, "y": None}

    def train_ranges(self, coord):
        def compute_range(ix, iy):
            return coord.train({"x": self.panel_scales["x"][[ix]], "y": self.panel_scales["y"][[iy]]})
        # Switch position of all scales if CoordFlip
        if isinstance(coord, CoordFlip) or (isinstance(coord, CoordPolar) and coord.theta == "y"):
            for scale in self.panel_scales["x"]:
                scale.position = "bottom" if scale.position == "top" else "bottom"
            for scale in self.panel_scales["y"]:
                scale.position = "right" if scale.position == "left" else "right"
        self.panel_ranges = [compute_range(self.panel_layout["SCALE_X"][i], self.panel_layout["SCALE_X"][i])
                             for i in range(len(self.panel_layout))]

    def xlabel(self, labels):
        xname = self.panel_scales["x"][0].name
        primary = labels["x"] if isinstance(xname, Waiver) else xname
        primary = self.panel_scales["x"][0].make_title(primary)
        # todo: not dealing with secondary axes now
        return [primary, None]

    def ylabel(self, labels):
        yname = self.panel_scales["y"][0].name
        primary = labels["y"] if isinstance(yname, Waiver) else yname
        primary = self.panel_scales["y"][0].make_title(primary)
        # todo: not dealing with secondary axes now
        return [primary, None]

    def render_labels(self, labels, theme):
        label_grobs = {}
        for label in labels.keys():
            labelgrobgrobs = []
            for i in (0, 1):
                modify = ".right" if (i == 1 and label == "y") else ".top" if (i == 1 and label == "x") else ""
                deflab = labels[label][i]
                if deflab is None or isinstance(deflab, Waiver):
                    grob = ZeroGrob()
                else:
                    grob = theme.render_element("axis.title." + label + modify, label=deflab,
                                         expand_x=label == "y", expand_y=label == "x")
                labelgrobgrobs.append(grob)
            label_grobs[label] = labelgrobgrobs
        return label_grobs


def scale_apply(data, variables, method, scale_id, scales):
    if len(variables) == 0:
        return {}
    if len(data) == 0:
        return {}
    if any(is_nan(scale_id)):
        raise ValueError("NA scale ID in scale_apply()")

    pieces = {}
    scale_id = np.array(scale_id)
    for var in variables:
        piece = []
        for i in range(len(scales)):
            scale = scales[i]
            piece.append(getattr(scale, method)(data[var][scale_id == i]))
        pieces[var] = piece

    return pieces

