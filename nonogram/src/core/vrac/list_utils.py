""" Contient des methodes appliquées sur des listes utiles pour le logiciel.
Ces methodes doivent être, de plus, indépendante du logiciel et aussi générale
que possible, afin de permettre un maximum de réutilisation.
"""


def intersection(iter1, iter2):
    """ Réalise l'intersection de deux listes binaires.

        Exemples :
            >>> intersection([1, 1, 0], [0, 1, 1])
            [0, 1, 0]
            >>> intersection([1, 1, 1, 0], [0, 1, 1, 1])
            [0, 1, 1, 0]
            >>> intersection([1, 1, 1, 0, 0], [0, 0, 1, 1, 1])
            [0, 0, 1, 0, 0]
            >>> intersection([1, 1, 1, 1, 0], [0, 1, 1, 1, 1])
            [0, 1, 1, 1, 0]
    """
    return [1 if (i == j == 1) else 0 for i, j in zip(iter1, iter2)]


def indexes_XOR(l1, l2):
    """ Retourne la liste des index où le XOR de l1 et l2 est vrai.

        Exemples :
        >>> indexes_XOR([0, 1, 0], [1, 0, 0])
        [0, 1]
    """
    return [i for i in range(min(len(l1), len(l2))) if l1[i] != l2[i]]


if __name__ == '__main__':
    pass
