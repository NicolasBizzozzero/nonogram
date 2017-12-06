# -*- coding: utf-8 -*-
""" Lit proprement des inputs donnés comme décrits dans la question 7. """

import io


DELIMITEUR = "#\n"
MOTIF_NOM_INSTANCES = "../instances/{index}.txt"


def parse_instance(file_path, encoding="utf8"):
    global DELIMITEUR

    lignes, colonnes = [], []
    with io.open(file_path, encoding=encoding) as file:
        for line in file:
            if line != DELIMITEUR:
                lignes.append(_parse_ligne(line))
            else:
                break
        for line in file:
            colonnes.append(_parse_ligne(line))
    return lignes, colonnes


def _parse_ligne(ligne):
    """ Parse une ligne contenant des entiers séparés par un espace, ou une
    ligne vide, puis retourne une liste d'entiers, ou une liste vide.
    Exemples :
    >>> _parse_ligne("1 2 3\n")
    [1, 2, 3]
    >>> _parse_ligne("\n")
    []
    """
    return list(map(int, ligne.split()))


if __name__ == '__main__':
    pass
