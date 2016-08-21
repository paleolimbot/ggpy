
import svgwrite as svg
from .renderer import Renderer
from .._na import is_nan
from .._grob.unit import Unit

_gp_aliases = {'lwd': 'stroke-width',
               'lty': 'linetype',
               'lineend': 'stroke-linecap',
               'fontsize': 'font-size',
               'col': 'stroke',
               'fill': 'fill',
               'fontfamily': 'font-family',
               'fontface': 'font-face'}


def _transform_key(key):
    return _gp_aliases[key] if key in _gp_aliases else key


def _transform_value(key, value):
    if isinstance(value, Unit):
        return '%s%s' % (value.val, value.unit)
    elif key in ('stroke',):
        return 'none' if is_nan(value) else value
    elif key == 'font-size':
        return '%spt' % value
    else:
        return value


def _rename_gp(gp):
    # make style text from gpars
    # eg stroke-width: 1.07; stroke: none; fill: #EBEBEB;
    # stroke-width: 0.53; stroke: #FFFFFF; stroke-linecap: butt;
    # font-size: 8.80pt; fill: #4D4D4D; font-family: Arial;
    gpout = {}
    for key, value in gp.items():
        key = _transform_key(key)
        gpout[key] = _transform_value(key, value)
    return gpout


def _gp_to_style(gp):
    return ''.join(['%s: %s; ' % (key, value) for key, value in gp.items()]).strip()


class SVGRenderer(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.dwg = None
        self._height = None
        self._width = None

    def convertx(self, x, unitfrom=None):
        return x

    def converty(self, y, unitfrom=None):
        return self._height - y

    def render_svg(self, grob):
        self.dwg = svg.Drawing(filename=None, debug=False)
        # assumes zero based coordinates
        self._height = grob.range_y()[1]
        self._width = grob.range_x()[1]
        self.dwg['viewBox'] = '0 0 %s %s' % (self._width, self._height)
        self.dwg['width'] = self._width
        self.dwg['height'] = self._height

        # seems to always be added by ggplot in R for some reason
        self.dwg.add(self.dwg.style("line, polyline, path, rect, circle {fill: none; stroke: #000000; " +
                                    "stroke-linecap: round; stroke-linejoin: round; stroke-miterlimit: 10.00; }"))

        # need a background rect often
        self.dwg.add(self.dwg.rect((0, 0), ('100%', '100%'), fill="#FFFFFF", stroke='#FFFFFF'))

        # render the grob (should be recursive)
        self.render_grob(grob)

        # return the string svg
        return self.dwg.tostring()

    def render_text(self, grob):
        gp = _rename_gp(grob.gp)
        transform = []
        if grob.hjust != 0 or grob.vjust != 0:
            transform.append('translate(%s, %s)' % (-grob.hjust * grob.width(), grob.vjust * grob.height()))
        if grob.angle != 0:
            transform.append('rotate(%f)' % grob.angle)

        t = self.dwg.text(grob.label, insert=(grob.x, self.converty(grob.y)))
        if transform:
            t['transform'] = ' '.join(transform)
        gp['color'] = gp['stroke']
        gp['stroke'] = 'none'
        t['style'] = _gp_to_style(gp)
        self.dwg.add(t)

    def render_polyline(self, grob):
        p = self.dwg.polyline(points=list(zip(grob.x, [self.converty(y) for y in grob.y])))
        gp = _rename_gp(grob.gp)
        p['style'] = _gp_to_style(gp)
        self.dwg.add(p)

    def render_rect(self, grob):
        r = self.dwg.rect(insert=(grob.x, self.converty(grob.y)-grob.height()), size=(grob.width(), grob.height()))
        gp = _rename_gp(grob.gp)
        r['style'] = _gp_to_style(gp)
        self.dwg.add(r)

    def render_points(self, grob):
        raise NotImplementedError() # not here yet
