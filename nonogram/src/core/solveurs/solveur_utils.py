# -*- coding: utf-8 -*-
""" Ce module contient tous les outils utiles et communs aux solveurs d'une
grille.
"""

from enum import IntEnum


CASE_BLANCHE = -1
CASE_VIDE = 0
CASE_NOIRE = 1


class SolvingMethod(IntEnum):
    DYNAMIC = 0
    LINEAR = 1
    BOTH = 2


class SolvingMethodNotSupported(Exception):
    def __init__(self, solving_method):
        Exception.__init__(self, "The solving method \"{solving_method}\" is "
                           "currently not supported.".format(
                               solving_method=solving_method))


def str_to_solving_method(solving_method):
    try:
        return SolvingMethod[solving_method.upper()]
    except KeyError:
        raise SolvingMethodNotSupported(solving_method)


class GrilleImpossible(Exception):
    """ Exception lancée lorsqu'une grille est impossible à résoudre. """

    def __init__(self):
        Exception.__init__(self, "La grille est impossible à résoudre.")


if __name__ == '__main__':
    pass
