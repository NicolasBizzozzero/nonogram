""" Ce module contient tous les outils utiles et communs aux solveurs d'une
grille.
"""

CASE_BLANCHE = -1
CASE_VIDE = 0
CASE_NOIRE = 1


class GrilleImpossible(Exception):
    """ Exception lancée lorsqu'une grille est impossible à résoudre. """

    def __init__(self):
        Exception.__init__(self, "La grille est impossible à résoudre.")


if __name__ == '__main__':
    pass
