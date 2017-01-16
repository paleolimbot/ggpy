
from .layer import Layer
from .geom_blank import GeomBlank
from .layout import Layout


_default_render_method = None  # todo: set to actual render method


def set_render_method(method):
    global _default_render_method
    _default_render_method = method


class BuiltGGPlot(object):

    def __init__(self, ggplot):
        self.plot = ggplot.clone()
        self.data = None
        self.layout = None
        self._rendered = None
        self._render_method = _default_render_method
        self._built = False

    def build(self):
        if self._built:
            return
        plot = self.plot
        if len(plot._layers) == 0:
            plot = plot.modify(Layer(geom="blank"))
        layers = plot._layers
        layer_data = [l.layer_data(plot._data) for l in layers]
        scales = plot._scales

        def by_layer(layers, data, f):
            return [f(layers[i], data[i]) for i in range(len(layers))]

        # Initialise panels, add extra data for margins & missing facetting
        # variables, and add on a PANEL variable to data
        # todo: analyze data chain to minimize copying (ensure modification doesn't screw up multiple layers)
        layout = Layout(plot._facet)
        data = layout.setup(layer_data, plot._data, plot._global_vars, plot._local_vars, plot._coordinates)
        data = layout.map(data)

        # Compute aesthetics to produce data with generalised variable names
        data = by_layer(layers, data, lambda l, d: l.compute_aesthetics(d, plot))

        # Transform all scales
        data = [scales.transform_df(df) for df in data]

        # Map and train positions so that statistics have access to ranges
        # and all positions are numeric
        layout.train_position(data, scales.get_scales("x"), scales.get_scales("y"))
        data = layout.map_position(data)

        # Apply and map statistics
        data = by_layer(layers, data, lambda l, d: l.compute_statistic(d, layout))
        data = by_layer(layers, data, lambda l, d: l.map_statistic(d, plot))

        # make sure x and y scales exist
        scales.add_missing(("x", "y"))

        # Reparameterise geoms from (e.g.) y and width to ymin and ymax
        data = by_layer(layers, data, lambda l, d: l.compute_geom_1(d))

        # Apply position adjustments
        data = by_layer(layers, data, lambda l, d: l.compute_position(d, layout))

        # Reset position scales, then re-train and map.  This ensures that facets
        # have control over the range of a plot: is it generated from what's
        # displayed, or does it include the range of underlying data
        layout.reset_scales()
        layout.train_position(data, scales.get_scales("x"), scales.get_scales("y"))
        data = layout.map_position(data)

        # Train and map non-position scales
        npscales = scales.non_position_scales()
        if len(npscales) > 0:
            for df in data:
                npscales.train_df(df)
            data = [npscales.map_df(df) for df in data]

        # Train coordinate system
        layout.train_ranges(plot._coordinates)

        # Fill in defaults etc.
        data = by_layer(layers, data, lambda l, d: l.compute_geom_2(d))

        # Let layer stat have a final say before rendering
        data = by_layer(layers, data, lambda l, d: l.finish_statistics(d))

        # Let Layout modify data before rendering
        data = layout.finish_data(data)

        self.data = data
        self.layout = layout
        self._built = True
        return self

    def rebuild(self):
        self._built = False
        return self.build()

    # this allows Jupyter Notebook to display the plot (as rendered by self._render_method)
    # regular repr should remain unbuilt (since it is not displayed)
    def render(self):
        if not self._built:
            self.build()
        if self._rendered is None:
            self._rendered = self._render_method(self)
        return self._rendered

    def rerender(self):
        self._rendered = None
        return self.render()

    def _repr_html_(self):
        self.render()
        if '_repr_html_' in dir(self._rendered):
            return self._rendered._repr_html_()
        return None

    def _repr_svg_(self):
        self.render()
        if '_repr_svg_' in dir(self._rendered):
            return self._rendered._repr_svg_()
        return None

    def _repr_png_(self):
        self.render()
        if '_repr_png_' in dir(self._rendered):
            return self._rendered._repr_png_()
        return None

    def _repr_jpeg_(self):
        self.render()
        if '_repr_jpeg_' in dir(self._rendered):
            return self._rendered._repr_jpeg_()
        return None

    def _repr_javascript_(self):
        self.render()
        if '_repr_javascript_' in dir(self._rendered):
            return self._rendered._repr_javascript_()
        return None