
from .layer import Layer
from .scale import Scale
from .scales import ScalesList
from .facet import Facet
from .facet_null import FacetNull
from .coord import Coord
from .coord_cartesian import CoordCartesian
from .theme import Theme
from .labels import make_labels, labs, Labels
from .plot_build import BuiltGGPlot
from . import _interface as interface


# this function allows regular objects/modules to function as interfaces by filtering out only their methods
# and skipping protected methods that may provide confusing functionality. The None object can be used as interface
def _interface_dir(interface_obj):
    return [obj for obj in dir(interface_obj) if not obj.startswith("_") and callable(getattr(interface_obj, obj))]


# this sets the default build method
_build_method = BuiltGGPlot


def set_build_method(method):
    global _build_method
    _build_method = method


class ggplot(object):

    def __init__(self, data=None, mapping=None, local_vars=None, global_vars=None):
        self._data = data
        self._mapping = mapping
        self._layers = []
        self._scales = ScalesList()
        self._theme = Theme()
        self._coordinates = CoordCartesian()
        self._facet = FacetNull()
        self._labels = make_labels(self._mapping)
        # this is kind of like "plot_env". these are passed to 'eval' in Mapping.map()
        self._local_vars = local_vars if local_vars is not None else {}  # todo: don't know if these are needed yet
        self._global_vars = global_vars if global_vars is not None else {}

        # this is only in the Python edition (self._built must be set to None whenever this object
        # is modified
        self._built = None
        self._build_method = _build_method
        self._interface = interface

    def __layer(self, layer=None, **kwargs):
        if layer is None:
            self._layers.append(Layer(**kwargs))
            self._built = None
        elif callable(layer):
            newlayer = layer(**kwargs)
            if not isinstance(newlayer, Layer):
                raise TypeError("layer must return value of type Layer")
            self._layers.append(newlayer)
            self._built = None
        elif isinstance(layer, Layer):
            if kwargs:
                raise ValueError("layer is not callable, kwargs were ignored")
            self._layers.append(layer)
            self._built = None
        else:
            raise TypeError("Layer to be added must be of type Layer")
        return self

    def __theme(self, theme=None, **kwargs):
        if theme is None:
            self._theme = self._theme + Theme(**kwargs)
            self._built = None
        elif callable(theme):
            newtheme = self._theme + theme(**kwargs)
            if not isinstance(newtheme, Theme):
                raise TypeError("theme must return value of type Theme")
            self._theme = newtheme
            self._built = None
        elif isinstance(theme, Theme):
            if kwargs:
                raise ValueError("theme is not callable, kwargs were ignored")
            self._theme = self._theme + theme
            self._built = None
        else:
            raise TypeError("Theme to be added must be of type Theme")
        return self

    def __coord(self, coord=None, **kwargs):
        if coord is None:
            self._coordinates = CoordCartesian(**kwargs)
            self._built = None
        elif callable(coord):
            newcoord = coord(**kwargs)
            if not isinstance(coord, Coord):
                raise TypeError("coord must return value of type Coord")
            self._coordinates = newcoord
            self._built = None
        elif isinstance(coord, Coord):
            if kwargs:
                raise ValueError("coord is not callable, kwargs were ignored")
            self._coordinates = coord
            self._built = None
        else:
            raise TypeError("Coordinates object must be of type Coord")
        return self

    def __facet(self, facet, **kwargs):
        if facet == "null":
            self._facet = FacetNull(**kwargs)
            self._built = None
        elif facet is None:
            self._facet = FacetNull(**kwargs)
            self._built = None
        elif callable(facet):
            newfacet = facet(**kwargs)
            if not isinstance(facet, Facet):
                raise TypeError("facet must return value of type Facet")
            self._facet = newfacet
            self._built = None
        elif isinstance(facet, Facet):
            if kwargs:
                raise ValueError("facet is not callable, kwargs were ignored")
            self._facet = facet
            self._built = None
        else:
            raise TypeError("facet must be of type Facet or one of 'null', 'wrap', or 'grid'")
        return self

    def __scale(self, scale, **kwargs):
        if callable(scale):
            newscale = scale(**kwargs)
            if not isinstance(newscale, Scale):
                raise TypeError("Scale function must return object of type Scale")
            self._scales.add(newscale)
            self._built = None
        elif isinstance(scale, Scale):
            if kwargs:
                raise ValueError("scale is not callable, kwargs were ignored")
            self._scales.add(scale)
            self._built = None
        else:
            raise TypeError("scale must be of type Scale")
        return self

    def __labs(self, **kwargs):
        self._labels = self._labels + labs(**kwargs)
        return self

    def clone(self):
        newobj = type(self)(data=self._data, local_vars=self._local_vars, global_vars=self._global_vars)
        newobj._mapping = self._mapping.copy() if self._mapping is not None else None
        newobj._layers = [layer.clone() for layer in self._layers]
        newobj._scales = self._scales.clone()
        newobj._theme = self._theme.copy() if self._theme is not None else None
        newobj._coordinates = newobj._coordinates.clone()
        newobj._facet = self._facet.clone()
        newobj._labels = self._labels.copy()
        return newobj

    def modify(self, other):
        if isinstance(other, list):
            for obj in other:
                self.__iadd__(obj)
        elif isinstance(other, Scale):
            self.__scale(other)
        elif isinstance(other, Layer):
            self.__layer(other)
        elif isinstance(other, Coord):
            self.__coord(other)
        elif isinstance(other, Labels):
            self.__labs(**other)
        elif isinstance(other, Theme):
            self.__theme(other)
        elif isinstance(other, Facet):
            self.__facet(other)
        else:
            raise TypeError("Don't know how to add type %s to ggplot" % type(other).__name__)
        return self

    def add(self, other):
        newobj = self.clone()
        return newobj.modify(other)

    def __iadd__(self, other):
        return self.add(other)

    def __add__(self, other):
        newobj = self.clone()
        if isinstance(other, list):
            for obj in other:
                newobj.modify(obj)
        else:
            newobj.modify(other)
        return newobj

    # this allows stringing together functions imported to the _interface module with
    # the dot selector
    def __getattr__(self, item):
        if item in object.__dir__(self):
            return object.__getattribute__(self, item)
        elif self._interface is not None and item in _interface_dir(self._interface):
            intmeth = getattr(self._interface, item)
            return lambda *args, **kwargs: self.add(intmeth(*args, **kwargs))
        raise AttributeError("'%s' has no attribute '%s'" % (type(self).__name__, item))

    def __dir__(self):
        return list(object.__dir__(self)) + list(_interface_dir(self._interface))

    # this allows Jupyter Notebook to display the plot (as created/rendered by self._build_method)
    # regular repr should remain unbuilt (since it is not displayed)
    def build(self):
        if self._built is None:
            self._built = self._build_method(self)
        return self._built

    def rebuild(self):
        self._built = None
        return self.build()

    def _repr_html_(self):
        self.build()
        if '_repr_html_' in dir(self._built):
            return self._built._repr_html_()
        return None

    def _repr_svg_(self):
        self.build()
        if '_repr_svg_' in dir(self._built):
            return self._built._repr_svg_()
        return None

    def _repr_png_(self):
        self.build()
        if '_repr_png_' in dir(self._built):
            return self._built._repr_png_()
        return None

    def _repr_jpeg_(self):
        self.build()
        if '_repr_jpeg_' in dir(self._built):
            return self._built._repr_jpeg_()
        return None

    def _repr_javascript_(self):
        self.build()
        if '_repr_javascript_' in dir(self._built):
            return self._built._repr_javascript_()
        return None
