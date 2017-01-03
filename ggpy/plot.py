
from .layer import Layer
from .scale import Scale
from .scales import ScalesList
from .facet import Facet
from .facet_null import FacetNull
from .coord import Coord
from .coord_cartesian import CoordCartesian
from .theme import Theme
from .theme_default import get_default_theme
from .labels import make_labels, labs, Labels


class ggplot(object):

    def __init__(self, data=None, mapping=None, local_vars=None, global_vars=None):
        self._data = data
        self._mapping = mapping
        self._layers = []
        self._scales = ScalesList()
        self._theme = get_default_theme()
        self._coordinates = CoordCartesian()
        self._facet = FacetNull()
        self._labels = make_labels(self._mapping)
        # this is kind of like "plot_env". these are passed to 'eval' in Mapping.map()
        self._local_vars = local_vars if local_vars is not None else {}  # todo: don't know if these are needed yet
        self._global_vars = global_vars if global_vars is not None else {}

    def layer(self, layer=None, **kwargs):
        if layer is None:
            self._layers.append(Layer(**kwargs))
        elif callable(layer):
            newlayer = layer(**kwargs)
            if not isinstance(newlayer, Layer):
                raise TypeError("layer must return value of type Layer")
            self._layers.append(newlayer)
        elif isinstance(layer, Layer):
            if kwargs:
                raise ValueError("layer is not callable, kwargs were ignored")
            self._layers.append(layer)
        else:
            raise TypeError("Layer to be added must be of type Layer")
        return self

    def theme(self, theme=None, **kwargs):
        if theme is None:
            self._theme = self._theme + Theme(**kwargs)
        elif callable(theme):
            newtheme = self._theme + theme(**kwargs)
            if not isinstance(newtheme, Theme):
                raise TypeError("theme must return value of type Theme")
            self._theme = newtheme
        elif isinstance(theme, Theme):
            if kwargs:
                raise ValueError("theme is not callable, kwargs were ignored")
            self._theme = self._theme + theme
        else:
            raise TypeError("Theme to be added must be of type Theme")
        return self

    def coord(self, coord=None, **kwargs):
        if coord is None:
            self._coordinates = CoordCartesian(**kwargs)
        elif callable(coord):
            newcoord = coord(**kwargs)
            if not isinstance(coord, Coord):
                raise TypeError("coord must return value of type Coord")
            self._coordinates = newcoord
        elif isinstance(coord, Coord):
            if kwargs:
                raise ValueError("coord is not callable, kwargs were ignored")
            self._coordinates = coord
        else:
            raise TypeError("Coordinates object must be of type Coord")
        return self

    def facet(self, facet, **kwargs):
        if facet == "null":
            self._facet = FacetNull(**kwargs)
        elif facet is None:
            self._facet = FacetNull(**kwargs)
        elif callable(facet):
            newfacet = facet(**kwargs)
            if not isinstance(facet, Facet):
                raise TypeError("facet must return value of type Facet")
            self._facet = newfacet
        elif isinstance(facet, Facet):
            if kwargs:
                raise ValueError("facet is not callable, kwargs were ignored")
            self._facet = facet
        else:
            raise TypeError("facet must be of type Facet or one of 'null', 'wrap', or 'grid'")
        return self

    def scale(self, scale, **kwargs):
        if callable(scale):
            newscale = scale(**kwargs)
            if not isinstance(newscale, Scale):
                raise TypeError("Scale function must return object of type Scale")
            self._scales.add(newscale)
        elif isinstance(scale, Scale):
            if kwargs:
                raise ValueError("scale is not callable, kwargs were ignored")
            self._scales.add(scale)
        else:
            raise TypeError("scale must be of type Scale")
        return self

    def scales(self, *scales, **kwargs):
        for scale in scales:
            self.scale(scale, **kwargs)
        return self

    def labs(self, **kwargs):
        self._labels = self._labels + labs(**kwargs)
        return self

    def clone(self):
        newobj = ggplot(data=self._data, local_vars=self._local_vars, global_vars=self._global_vars)
        newobj._mapping = self._mapping.copy()  # shallow copy is fine?
        newobj._layers = [layer.clone() for layer in self._layers]
        newobj._scales = self._scales.clone()
        newobj._theme = self._theme.copy()  # shallow copy is fine?
        newobj._coordinates = newobj._coordinates.clone()
        newobj._facet = self._facet.clone()
        newobj._labels = self._labels.copy()
        return newobj

    def __iadd__(self, other):
        if isinstance(other, list):
            for obj in other:
                self.__iadd__(obj)
        elif isinstance(other, Scale):
            self.scale(other)
        elif isinstance(other, Layer):
            self.layer(other)
        elif isinstance(other, Coord):
            self.coord(other)
        elif isinstance(other, Labels):
            self.labs(**other)
        elif isinstance(other, Theme):
            self.theme(other)
        elif isinstance(other, Facet):
            self.facet(other)
        else:
            raise TypeError("Don't know how to add type %s to ggplot" % type(other).__name__)
        return self

    def __add__(self, other):
        newobj = self.clone()
        if isinstance(other, list):
            for obj in other:
                newobj.__iadd__(obj)
        elif False:
            pass
        else:
            raise TypeError("Don't know how to add type %s to ggplot" % type(other).__name__)
        return newobj
