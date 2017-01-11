
# all imported names must be protected by _ to avoid importing to the interface
from .layer import Layer as _Layer
from .geom_point import GeomPoint as _GeomPoint
from .labels import labs as _labs

# todo: this should store the shortcut functions that R uses (i.e. geom_point(), stat_bin())
# will all be imported to ggpy namespace and will be available by ggplot().XXX


def geom_point(mapping=None, inherit_aes=True):
    return _Layer(mapping=mapping, geom=_GeomPoint(), inherit_aes=inherit_aes)


def labs(**kwargs):
    return _labs(**kwargs)
