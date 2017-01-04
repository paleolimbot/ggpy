
from .geom_blank import GeomBlank
from .layout import Layout


class BuiltGGPlot(object):

    def __init__(self, ggplot):
        self.plot = ggplot.clone()
        self.data = None
        self.layout = None
        self.build()

    def build(self):
        plot = self.plot
        if len(plot._layers) == 0:
            plot.layer(geom=GeomBlank())
        layers = plot._layers
        layer_data = [l.layer_data(plot._data) for l in layers]
        scales = plot._scales
        layout = Layout(plot._facet)

        def by_layer(layers, data, f):
            return [f(layers[i], data[i]) for i in range(len(layers))]

        # todo: analyze data chain to minimize copying
        data = layout.setup(layer_data, plot._data, plot._global_vars, plot._local_vars, plot._coordinates)
        data = layout.map(data)
        data = by_layer(layers, data, lambda l, d: l.compute_statistic(d, layout))
        data = by_layer(layers, data, lambda l, d: l.map_statistic(d, plot))

        # make sure x and y scales exist
        scales.add_missing(("x", "y"))
        data = by_layer(layers, data, lambda l, d: l.compute_geom_1(d))

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

    def render(self, renderer):
        # todo: method stub
        pass
