
import numpy as np
import pandas as pd

from ._na import NA
from .geom import Geom
from .geom_point import GeomPoint
from .stat import Stat, StatIdentity
from .aes import Mapping, aes, check_aesthetics, check_required_aesthetics
from .aes_calculated import is_calculated_aes, strip_dots
from .position import Position
from .position_identity import PositionIdentity
from .utilities import Waiver
from .grouping import add_group
from ._grob.grob import ZeroGrob


# these functions sanitise input to the Layer() constructor, making it possible to generate
# objects if a type/function, string, or instance is passed.
def _position(position_input, **kwargs):
    if position_input is None:
        return PositionIdentity()
    elif isinstance(position_input, Position):
        return position_input
    elif callable(position_input):
        newpos = position_input(**kwargs)
        if not isinstance(newpos, Position):
            raise TypeError("Position function returns non-position value")
        return newpos
    elif position_input == "identity":
        return PositionIdentity()
    else:
        raise ValueError("Could not find position object for input '%s'" % position_input)


def _stat(stat_input, **kwargs):
    if stat_input is None:
        return StatIdentity()
    elif isinstance(stat_input, Stat):
        return stat_input
    elif callable(stat_input):
        newstat = stat_input(stat_input, **kwargs)
        if not isinstance(newstat, Stat):
            raise TypeError("Stat function returns non-stat value")
        return newstat
    elif stat_input == "identity":
        return StatIdentity()
    else:
        raise ValueError("Could not find stat object for input '%s'" % stat_input)


def _geom(geom_input, **kwargs):
    if isinstance(geom_input, Geom):
        return geom_input
    elif callable(geom_input):
        newgeom = geom_input(geom_input, **kwargs)
        if not isinstance(newgeom, Geom):
            raise TypeError("Geom function returns non-geom value")
        return newgeom
    elif geom_input == "point":
        return GeomPoint()
    else:
        raise ValueError("Could not find stat object for input '%s'" % geom_input)


class Layer(object):

    def __init__(self, geom=None, geom_params=None, stat=None, stat_params=None,
                 data=Waiver(), aes_params=None, mapping=None, position=None, inherit_aes=False,
                 show_legend=NA):
        self.geom = _geom(geom)
        self.geom_params = geom_params if geom_params is not None else {}
        self.stat = _stat(stat)
        self.stat_params = stat_params if stat_params is not None else {}
        self.data = data
        self.aes_params = aes_params if aes_params is not None else {}
        if mapping is not None and not isinstance(mapping, Mapping):
            raise TypeError("parameter 'mapping' must be of type 'Mapping'")
        self.mapping = mapping if mapping is not None else aes()
        self.position = _position(position)
        self.inherit_aes = inherit_aes
        self.show_legend = show_legend

    def clone(self):
        return type(self)(geom=self.geom, geom_params=self.geom_params.copy(), stat=self.stat,
                          stat_params=self.stat_params.copy(), data=self.data,
                          aes_params=self.aes_params.copy(), mapping=self.mapping.copy(),
                          position=self.position, inherit_aes=self.inherit_aes, show_legend=self.show_legend)

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
