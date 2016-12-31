
from .geom import Geom
from .stat import Stat, StatIdentity
from .aes import Mapping, aes, check_aesthetics
from .aes_calculated import is_calculated_aes
from .position import Position
from .position_identity import PositionIdentity
from .utilities import Waiver
from .grouping import add_group

import pandas as pd
import numpy as np


class Layer(object):

    def __init__(self, geom=None, geom_params=None, stat=None, stat_params=None,
                 data=None, aes_params=None, mapping=None, position=None, inherit_aes=False):
        if not isinstance(geom, Geom):
            raise TypeError("parameter 'geom' must inherit from type Geom")
        self.geom = geom
        self.geom_params = geom_params if geom_params is not None else {}
        if stat is not None and not isinstance(stat, Stat):
            raise TypeError("parameter 'stat' must inherit from type Stat")
        self.stat = stat if stat is not None else StatIdentity()
        self.stat_params = stat_params if stat_params is not None else {}
        self.data = data
        self.aes_params = aes_params if aes_params is not None else aes_params
        if mapping is not None and not isinstance(mapping, Mapping):
            raise TypeError("parameter 'mapping' must be of type 'Mapping'")
        self.mapping = mapping if mapping is not None else aes()
        if position is not None and not isinstance(position, Position):
            raise TypeError("parameter 'position' must be of type 'Position'")
        self.position = position if position is not None else PositionIdentity()
        self.inherit_aes = inherit_aes

    def __repr__(self):
        return "Mapping: %s\nGeom: %s\nStat: %s" % (repr(self.geom), repr(self.stat), repr(self.position))

    def layer_data(self, plot_data):
        if isinstance(self.data, Waiver):
            return plot_data
        elif callable(self.data):
            data = self.data(plot_data)
            if not isinstance(data, pd.DataFrame):
                raise TypeError("Data function must return a pandas.DataFrame")
            return data
        else:
            return self.data

    def compute_aesthetics(self, data, plot):
        if self.inherit_aes:
            aesthetics = plot.mapping + self.mapping
        else:
            aesthetics = self.mapping

        # remove calculated or set aesthetics
        for key in aesthetics.keys():
            if key in self.aes_params or is_calculated_aes(aesthetics[key]):
                del aesthetics[key]
        if "group" in self.geom_params:
            aesthetics["group"] = self.geom_params["group"]

        # add default aesthetics
        plot.scales.add_defaults(data, aesthetics)

        # evaluate aesthetics
        evaled = aesthetics.map_df(data)

        n = len(data)
        if n == 0:
            if len(evaled) == 0:
                n = 0
            else:
                shapes = [np.shape(val) for val in evaled.values()]
                lengths = [item for sublist in shapes for item in sublist]
                n = max(lengths)

        # check for length/shape
        check_aesthetics(evaled, n)

        if len(data) == 0 and n > 0:
            evaled["PANEL"] = 1
        else:
            evaled["PANEL"] = data["PANEL"]

        return add_group(pd.DataFrame(evaled))

    def compute_statistic(self, data, plot):
        # todo: stub
        pass

    def map_statistic(self, data, plot):
        # todo: stub
        pass

    def compute_geom_1(self, data):
        # todo: stub
        pass

    def compute_position(self, data, layout):
        # todo: stub
        pass

    def compute_geom_2(self, data):
        # todo: stub
        pass

    def finish_statistics(self, data):
        # todo: stub
        pass

    def draw_geom(self, data, layout, coord):
        # todo: stub
        pass
