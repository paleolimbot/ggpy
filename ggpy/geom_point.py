

from .geom import Geom
from ._na import NA
from .aes import aes
from .legend_draw import draw_key_point
from ._grob.grob import PointsGrob, gpar
from ._grob.colours import alpha


class GeomPoint(Geom):

    def __init__(self):
        Geom.__init__(self, required_aes=('x', 'y'), non_missing_aes=('size', 'shape'),
                      default_aes=aes(shape=19, colour='black', size=1.5, fill=NA, alpha=NA, stroke=0.5),
                      draw_key=draw_key_point)

    def draw_panel(self, data, panel_scales, coord, params):
        coords = coord.transform(data, panel_scales)
        return PointsGrob(coords['x'], coords['y'], pch=coords['shape'],
                          gp=gpar(col=alpha(coords['col'], coords['alpha']),
                                  fill=alpha(coords['fill'], coords['alpha']),
                                  fontsize=coords['size'] + coords['stroke'],  # sizes here are up for grabs
                                  lwd = coords['stroke']))
