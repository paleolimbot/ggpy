
# all imported functions must be protected by _ to avoid importing to the interface
from ._na import NA
from .layer import Layer as _Layer
from .labels import labs as _labs
from .facet import Facet as _Facet
from .facet_null import FacetNull as _FacetNull
from .utilities import Waiver as _Waiver

# todo: this should store the shortcut functions that R uses (i.e. geom_point(), stat_bin())
# will all be imported to ggpy namespace and will be available by ggplot().XXX


# layers
def geom_point(mapping=None, data=None, stat="identity", position="identity",
               na_rm=False, show_legend=NA, inherit_aes=True, **kwargs):
    data = data if data is not None else _Waiver()
    return _Layer(mapping=mapping, data=data, stat=stat, position=position, geom="point", show_legend=show_legend,
                  inherit_aes=inherit_aes, stat_params={"na_rm": na_rm}, geom_params={"na_rm": na_rm}, **kwargs)


# labels
def labs(**kwargs):
    return _labs(**kwargs)


# facets
def facet_null(shrink=True):
    return _FacetNull(shrink=shrink)


# generic facet sanitizing function
def facet(type=None, **kwargs):
    if type is None:
        return _FacetNull(**kwargs)
    elif callable(type):
        newfac = type(**kwargs)
        if not isinstance(newfac, _Facet):
            raise TypeError("Facet function returns non-facet value")
        return newfac
    elif type == "null":
        return _FacetNull(**kwargs)
    else:
        raise ValueError("Could not convert input '%s' to type Facet" % type)
