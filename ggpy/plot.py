
class ggplot(object):

    def __init__(self, data, mapping=None):
        self._data = data
        self._mapping = mapping
        self._layers = []
        self._scales = None
        self._theme = []
        self._coordinates = None
        self._facet = None
        self._labels = None

