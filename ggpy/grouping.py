
from ._na import NA
from .scale_discrete import is_discrete


NO_GROUP = -1


# this approximates plyr::id() for a data frame (generates a unique id for all unique groups)
def _df_id(df):
    groups = []

    # for some reason this function gets called twice on the first group
    # and therefore will return indicies starting at 1
    # this is ok, since the group variable is just used in another
    # groupby operation
    def f(grp):
        grp_id = len(groups)
        grp["group"] = grp_id
        grp["__ids__"] = list(grp.index)
        groups.append(grp_id)
        return grp
    return df.groupby(list(df.columns)).apply(f).sort_values(by="__ids__")["group"]


def add_group(data):
    if len(data) == 0:
        return data
    if "group" not in data.columns:
        disc = [col not in ("label", "PANEL") and is_discrete(data[col]) for col in data.columns]
        if any(disc):
            data["group"] = _df_id(data.iloc[:, disc])
        else:
            data["group"] = NO_GROUP
    else:
        unique = list(set(data["group"]))
        data["group"] = [unique.index(v) for v in data["group"]]

    return data


def has_groups(data):
    if len(data) == 0:
        return NA
    return data["group"][0] == NO_GROUP
