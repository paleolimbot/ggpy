
# all imported functions must be protected by _ to avoid importing to the interface
from ._na import NA
from .layer import Layer as _Layer
from .labels import labs as _labs

# todo: this should store the shortcut functions that R uses (i.e. geom_point(), stat_bin())
# will all be imported to ggpy namespace and will be available by ggplot().XXX


def geom_point(mapping=None, data=None, stat="identity", position="identity",
               na_rm=False, show_legend=NA, inherit_aes=True):
    return _Layer(mapping=mapping, data=data, stat=stat, position=position, geom="point", show_legend=show_legend,
                  inherit_aes=inherit_aes, stat_params={"na_rm": na_rm}, geom_params={"na_rm": na_rm})


def labs(**kwargs):
    return _labs(**kwargs)
