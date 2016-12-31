
def coord_munch(coord, data, range, segment_length=0.01):
    if coord.is_linear():
        return coord.transform(data, range)
    else:
        raise NotImplementedError("coord_munch for non-linear coordinates is not implemented")
