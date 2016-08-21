
import svgwrite as svg
import io
from .renderer import Renderer
from .._na import is_nan
from .._grob.grob import gpar
from .._grob.unit import Unit

_gp_aliases = {'lwd': 'stroke-width',
               'lineend': 'stroke-linecap',
               'fontsize': 'font-size',
               'col': 'stroke',
               'fill': 'fill',
               'family': 'font-family'}


def _transform_key(key):
    return _gp_aliases[key] if key in _gp_aliases else key


def _transform_value(key, value):
    if isinstance(value, Unit):
        return '%s%s' % (value.val, value.unit)
    elif key in ('stroke',):
        return 'none' if is_nan(value) else value
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

    def render_svg(self, grob):
        self.dwg = svg.Drawing(filename=None)
        self.dwg['viewBox'] = '0 0 %s %s' % (grob.width(), grob.height())
        self.dwg['width'] = grob.width()
        self.dwg['height'] = grob.height()

        # seems to always be added by ggplot in R for some reason
        self.dwg.add(self.dwg.style("line, polyline, path, rect, circle {fill: none; stroke: #000000; " +
                                    "stroke-linecap: round; stroke-linejoin: round; stroke-miterlimit: 10.00; }"))

        # render the grob (should be recursive)
        self.render_grob(grob)

        # return the string svg
        return self.dwg.tostring()

    def render_title(self, grob):
        t = self.dwg.text(grob.label)
        gp = _rename_gp(grob.gp)
        if grob.angle != 0:
            t['transform'] = 'rotate(%f)' % grob.angle
        if grob.hjust != 0:  # currently only valid for middle and end and start
            gp['text-anchor'] = 'start' if grob.hjust == 0 else 'end' if grob.hjust == 1 else 'middle'
        if grob.vjust != 0: # TODO this is probably not going to work
            gp['dominant-baseline'] = 'baseline' if grob.hjust == 0 else 'hanging' if grob.hjust == 1 else 'middle'
        t['x'] = grob.x
        t['y'] = grob.y
        t['style'] = _gp_to_style(gp)
        self.dwg.add(t)

    def render_polyline(self, grob):
        p = self.dwg.polyline()
        gp = _rename_gp(grob.gp)
        p['points'] = ' '.join([','.join(pair) for pair in zip(grob.x, grob.y)])
        p['style'] = _gp_to_style(gp)
        self.dwg.add(p)

    def render_rect(self, grob):
        r = self.dwg.rect()
        gp = _rename_gp(grob.gp)
        r['x'] = grob['x']
        r['y'] = grob['y']
        r['width'] = _transform_value('width', grob['width'])
        r['height'] = _transform_value('height', grob['height'])
        r['style'] = _gp_to_style(gp)
        self.dwg.add(r)

    def render_points(self, grob):
        raise NotImplementedError() # not here yet
