# -*- coding: utf-8 -*-
""" This module contains all the tools usable by every solver.
"""

CASE_BLANCHE = -1
CASE_VIDE = 0
CASE_NOIRE = 1


class SolvingMethod():
    DYNAMIC = 0
    LINEAR = 1
    DYNAMIC_LINEAR = 2
    DYNAMIC_OPTIMIZED = 3


class SolvingMethodNotSupported(Exception):
    def __init__(self, solving_method):
        Exception.__init__(self, "The solving method \"{solving_method}\" is "
                           "currently not supported.".format(
                               solving_method=solving_method))


def str_to_solving_method(solving_method):
    solving_method = solving_method.lower()
    if solving_method == "dynamic":
        return SolvingMethod.DYNAMIC
    elif solving_method == "linear":
        return SolvingMethod.LINEAR
    elif solving_method == "dynamic_linear":
        return SolvingMethod.DYNAMIC_LINEAR
    elif solving_method == "dynamic_optimized":
        return SolvingMethod.DYNAMIC_OPTIMIZED
    else:
        raise SolvingMethodNotSupported(solving_method)


class GrilleImpossible(Exception):
    """ This exception is raised when a grid appear to be impossible to solve.
    """

    def __init__(self):
        Exception.__init__(self, "The grid appear to be impossible to solver.")


if __name__ == '__main__':
    pass
