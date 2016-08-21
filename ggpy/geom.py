
from .aes import aes
from .legend_draw import draw_key_point
from .utilities import remove_missing
from ._grob.grob import ZeroGrob, GTree
import numpy as np
import pandas as pd


class Geom(object):

    def __init__(self, required_aes=(), non_missing_aes=(), default_aes=None,
                 extra_params=('na_rm',), draw_key=draw_key_point):
        self.required_aes = required_aes
        self.non_missing_aes = non_missing_aes
        self.default_aes = aes() if default_aes is None else default_aes
        self.extra_params = extra_params
        self.draw_key = draw_key

    def handle_na(self, data, params):
        return remove_missing(data, params['na_rm'],
                              np.concatenate((self.required_aes, self.non_missing_aes)), type(self).__name__)

    def draw_layer(self, data, params, panel, coord):
        if len(data) == 0:
            n = len(np.unique(data['PANEL']))
            return [ZeroGrob(),] * n
        newpars = {}
        parnames = [p for p in self.parameters() if p in params]
        for p in parnames:
            newpars[p] = params[p]
        grobs = {}
        for panelname, paneldata in data.groupby('PANEL'):
            grobs[panelname] = self.draw_panel(paneldata, panel.ranges[panelname], coord, newpars)
        return grobs

    def draw_panel(self, data, panel_scales, coord, params):
        grobs = []
        for group, groupdata in data.groupby('group'):
            grobs.append(self.draw_group(groupdata, panel_scales, coord, params))
        return GTree(*grobs, name=type(self).__name__)

    def draw_group(self, data, panel_scales, coord, params):
        pass

    def setup_data(self, data, params):
        return data

    def use_defaults(self, data, params=None):
        if params is None:
            params = {}
        missing = set(self.default_aes.keys()).difference(data.columns)
        if len(data) == 0:
            cols = {}
            for key, value in self.default_aes.items():
                if key in missing:
                    cols[key] = value
            data = pd.DataFrame(cols) # returns data frame of length 1?
        else:
            for key, value in self.default_aes.items():
                if key in missing:
                    data[key] = value

        aes_params = set(self.aesthetics()).intersection(set(params.keys()))
        for key, value in aes_params:
            try:
                if len(value) != len(data) and type(value) != str:
                    raise ValueError("Aesthetic %s must have length of data or length of 1" % key)
            except TypeError:
                pass
            data[key] = value
        return data

    def parameters(self):
        return self.extra_params

    def aesthetics(self):
        return tuple(set(self.default_aes.keys()).union(set(self.required_aes)))

