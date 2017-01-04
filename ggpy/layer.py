
from .geom import Geom
from .stat import Stat, StatIdentity
from .aes import Mapping, aes, check_aesthetics, check_required_aesthetics
from .aes_calculated import is_calculated_aes, strip_dots
from .position import Position
from .position_identity import PositionIdentity
from .utilities import Waiver
from .grouping import add_group
from ._grob.grob import ZeroGrob

import pandas as pd
import numpy as np


class Layer(object):

    def __init__(self, geom=None, geom_params=None, stat=None, stat_params=None,
                 data=Waiver(), aes_params=None, mapping=None, position=None, inherit_aes=False):
        if not isinstance(geom, Geom):
            raise TypeError("parameter 'geom' must inherit from type Geom")
        self.geom = geom
        self.geom_params = geom_params if geom_params is not None else {}
        if stat is not None and not isinstance(stat, Stat):
            raise TypeError("parameter 'stat' must inherit from type Stat")
        self.stat = stat if stat is not None else StatIdentity()
        self.stat_params = stat_params if stat_params is not None else {}
        self.data = data
        self.aes_params = aes_params if aes_params is not None else {}
        if mapping is not None and not isinstance(mapping, Mapping):
            raise TypeError("parameter 'mapping' must be of type 'Mapping'")
        self.mapping = mapping if mapping is not None else aes()
        if position is not None and not isinstance(position, Position):
            raise TypeError("parameter 'position' must be of type 'Position'")
        self.position = position if position is not None else PositionIdentity()
        self.inherit_aes = inherit_aes

    def clone(self):
        return type(self)(geom=self.geom, geom_params=self.geom_params.copy(), stat=self.stat,
                          stat_params=self.stat_params.copy(), data=self.data,
                          aes_params=self.aes_params.copy(), mapping=self.mapping.copy(),
                          position=self.position, inherit_aes=self.inherit_aes)

    def __repr__(self):
        return "Mapping: %s\nGeom: %s\nStat: %s\nPosition: %s" % (repr(self.mapping), repr(self.geom),
                                                                  repr(self.stat), repr(self.position))

    def layer_data(self, plot_data):
        if self.data is None:
            return pd.DataFrame()
        elif isinstance(self.data, Waiver):
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
            aesthetics = plot._mapping + self.mapping
        else:
            aesthetics = self.mapping

        # remove calculated or set aesthetics
        for key in aesthetics.keys():
            if key in self.aes_params or is_calculated_aes(aesthetics[key]):
                del aesthetics[key]
        if "group" in self.geom_params:
            aesthetics["group"] = self.geom_params["group"]

        # add default aesthetics
        plot._scales.add_defaults(data, aesthetics, plot._global_vars, plot._local_vars)

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

    def compute_statistic(self, data, layout):
        if len(data) == 0:
            return pd.DataFrame()
        params = self.stat.setup_params(data, self.stat_params)
        data = self.stat.setup_data(data, params)
        return self.stat.compute_layer(data, params, layout)

    def map_statistic(self, data, plot):
        # this does calculates aesthetics (whatever those are)
        if len(data) == 0:
            return pd.DataFrame()
        aesthetics = self.mapping
        if self.inherit_aes:
            aesthetics = plot._mapping + aesthetics
        aesthetics = self.stat.default_aes + aesthetics
        newaes = aes()
        for key in aesthetics.keys():
            if is_calculated_aes(key):
                newaes[key] = strip_dots(aesthetics[key])
        if len(newaes):
            return data
        # Add map stat output to aesthetics
        stat_data = newaes.map_df(data)
        # add new scales (if necessary)
        plot._scales.add_defaults(data, newaes, plot._global_vars, plot._local_vars)

        # re-transform
        if self.stat.retransform:
            stat_data = plot._scales.transform_df(stat_data)

        # recombine (stat_data is a 'dict' not a df)
        for col in data:
            if col not in stat_data:
                stat_data[col] = data[col]
        return data

    def compute_geom_1(self, data):
        if len(data) == 0:
            return pd.DataFrame()
        data = self.geom.setup_data(data, self.geom_params + aes(**self.aes_params))
        check_required_aesthetics(self.geom.required_aes, list(data.columns) + list(self.aes_params.keys()),
                                  type(self.geom).__name__)
        return data

    def compute_position(self, data, layout):
        if len(data) == 0:
            return pd.DataFrame()
        params = self.position.setup_params(data)
        data = self.position.setup_data(data, params)
        return self.position.compute_layer(data, params, layout)

    def compute_geom_2(self, data):
        # Combine aesthetics, defaults, & params
        if len(data) == 0:
            return data  # not sure why this is data and not pd.DataFrame()
        return self.geom.use_defaults(data, self.aes_params)

    def finish_statistics(self, data):
        return self.stat.finish_layer(data)

    def draw_geom(self, data, layout, coord):
        if len(data) == 0:
            n = len(layout.panel_layout)
            return [ZeroGrob(), ] * n
        data = self.geom.handle_na(data, self.geom_params)
        return self.geom.draw_layer(data, self.geom_params, layout, coord)
