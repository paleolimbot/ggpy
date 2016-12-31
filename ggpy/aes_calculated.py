
import re

match_calculated_aes = re.compile("^\\.\\.([a-zA-Z._]+)\\.\\.$")


def is_calculated_aes(aesthetic):
    # this uses a single aesthetic value instead of the mapping object that the R version uses
    return any(match_calculated_aes.match(v) for v in find_vars(aesthetic))


def find_vars(expr):
    # todo: not quite sure what this does
    return [expr, ]
