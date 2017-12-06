# -*- coding: utf-8 -*-
from nonogram.src.core.solveurs.solveur_utils import CASE_NOIRE, CASE_BLANCHE, CASE_VIDE


CHAR_BLANC = "X"
CHAR_VIDE = "░"
CHAR_NOIR = "█"


def verifie_grille(grille, sequence_lignes, sequence_colonnes):
    """ Verifie la validité d'une grille en fonction de ses contraintes de
    lignes et de colonnes.
    """
    N, M = len(sequence_lignes), len(sequence_colonnes)
    return _verifie_sequence(grille, sequence_lignes, N, M) and \
           _verifie_sequence(grille.T, sequence_colonnes, M, N)


def _verifie_sequence(grille, sequence, N, M):
    """ Verifie la validité d'une grille en fonction d'une des ses séquences
    de contraintes.
    N est la taille de la séquence de contraintes passée en paramètre.
    M est la taille de la séquence de contraintes non-passée en paramètre.
    """
    for i in range(N):
        j, l = 0, sequence[i]
        for s in l:
            # TODO: if CASE_BLANCHE in grille[i][:M] ?
            while j < M and grille[i][j] == CASE_BLANCHE:
                j += 1
            if j == M:
                return False
            k = j
            while j < M and grille[i][j] == CASE_NOIRE:
                j += 1
            if s != j - k :
                return False
    return True    


def remplace_couleur(grille, couleur_originale, nouvelle_couleur):
    """ Remplace toutes les occurences de `couleur_originale` dans la grille
    par `nouvelle_couleur`.
    """
    grille[grille == couleur_originale] = nouvelle_couleur


if __name__ == '__main__':
    pass
