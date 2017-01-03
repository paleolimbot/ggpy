
from .layer import Layer
from .scale import aesthetics_x, aesthetics_y, Scale
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
        self.data = data
        self.mapping = mapping
        self.layers = []
        self.scales = ScalesList()
        self.theme = get_default_theme()
        self.coordinates = CoordCartesian()
        self.facet = FacetNull()
        self.labels = None
        # this is kind of like "plot_env". these are passed to 'eval' in Mapping.map()
        self.local_vars = local_vars if local_vars is not None else locals()
        self.global_vars = global_vars if global_vars is not None else globals()
        self.labels = make_labels(self.mapping)

    def layer(self, layer=None, **kwargs):
        if layer is None:
            self.layers.append(Layer(**kwargs))
        elif callable(layer):
            newlayer = layer(**kwargs)
            if not isinstance(newlayer, Layer):
                raise TypeError("layer must return value of type Layer")
            self.layers.append(layer)
        elif isinstance(layer, Layer):
            if kwargs:
                raise ValueError("layer is not callable, kwargs were ignored")
            self.layers.append(layer)
        else:
            raise TypeError("Layer to be added must be of type Layer")
        return self

    def theme(self, theme=None, **kwargs):
        if theme is None:
            self.theme = self.theme + Theme(**kwargs)
        elif callable(theme):
            newtheme = self.theme + theme(**kwargs)
            if not isinstance(newtheme, Theme):
                raise TypeError("theme must return value of type Theme")
            self.theme = theme
        elif isinstance(theme, Theme):
            if kwargs:
                raise ValueError("theme is not callable, kwargs were ignored")
            self.theme = self.theme + theme
        else:
            raise TypeError("Theme to be added must be of type Theme")
        return self

    def coord(self, coord=None, **kwargs):
        if coord is None:
            self.coordinates = CoordCartesian(**kwargs)
        elif callable(coord):
            newcoord = coord(**kwargs)
            if not isinstance(coord, Coord):
                raise TypeError("coord must return value of type Coord")
            self.coordinates = newcoord
        elif isinstance(coord, Coord):
            if kwargs:
                raise ValueError("coord is not callable, kwargs were ignored")
            self.coordinates = coord
        else:
            raise TypeError("Coordinates object must be of type Coord")
        return self

    def facet(self, facet, **kwargs):
        if facet == "null":
            self.facet = FacetNull(**kwargs)
        elif callable(facet):
            newfacet = facet(**kwargs)
            if not isinstance(facet, Facet):
                raise TypeError("facet must return value of type Facet")
            self.facet = newfacet
        elif isinstance(facet, Facet):
            if kwargs:
                raise ValueError("facet is not callable, kwargs were ignored")
            self.facet = facet
        else:
            raise TypeError("facet must be of type Facet or one of 'null', 'wrap', or 'grid'")
        return self

    def scale(self, scale, **kwargs):
        if callable(scale):
            newscale = scale(**kwargs)
            if not isinstance(newscale, Scale):
                raise TypeError("Scale function must return object of type Scale")
            self.scales.add(scale)
        elif isinstance(scale, Scale):
            if kwargs:
                raise ValueError("scale is not callable, kwargs were ignored")
            self.scales.add(scale)
        else:
            raise TypeError("scale must be of type Scale")
        return self

    def scales(self, *scales, **kwargs):
        for scale in scales:
            self.scale(scale, **kwargs)
        return self

    def labs(self, **kwargs):
        self.labels = self.labels + labs(**kwargs)
        return self




