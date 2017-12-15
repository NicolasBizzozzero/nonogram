# -*- coding: utf-8 -*-
""" Resout un nonograme en utilisant des méthodes de programmation dynamique.
Ce module contient toutes les fonctions utiles pour répondre aux questions de
la première partie du projet.
"""
import numpy as np
from time import time

from nonogram.src.core.solveurs.solveur_utils import CASE_BLANCHE, CASE_NOIRE, CASE_VIDE,\
    GrilleImpossible


def T_sans_ligne(j, l, s):
    """ Retourne `True` si on peut colorier de la case `0` à `j` la
    sous-séquence de `s` des `l` premiers blocs.
    Cette fonction ne tient pas compte de l'état des cases en cours de calcul.
    Correspond à l'algorithme demandé dans la question 4.
    """
    # Pas de case à colorier
    if l == 0:
        return True
    else:
        # Trop de cases à colorier
        if j < s[l - 1] - 1:
            return False
        # Pareil sauf s'il y'a qu'un seul element dans la séquence
        elif j == s[l - 1] - 1:
            return l == 1
        else:
            # On peut colorier le début, vérifions la suite
            return T(j - (s[l - 1] + 1), l - 1, s)


def T_recursif(s, li, cache):
    """ Retourne `True` si on peut colorier la ligne `li` en fonction de la
    séquence `s`. Le paramètre `cache` permet de stocker des valeurs déjà
    calculées pour les réutiliser en cas de besoin.
    Correspond à l'algorithme demandé dans la question 6.
    """
    K, M = len(s), len(li)
    if (K, M) in cache:
        return cache[K, M]
    if K == 0:
        cache[K, M] = not (CASE_NOIRE in li)
        return cache[K, M]

    elif M < s[-1]:
        cache[K, M] = False
        return cache[K, M]

    elif M == s[-1]:
        if K > 1:
            cache[K, M] = False
        else:
            cache[K, M] = not (CASE_BLANCHE in li)
        return cache[K, M]
    elif M > s[-1]:
        if li[M - 1] == CASE_BLANCHE:
            cache[K, M] = T_recursif(s, li[:M - 1], cache)
            return cache[K, M]

        b = np.all(li[M - s[-1]:] >= CASE_VIDE) and \
                  ((K == 1 and np.all(li[:M - s[-1]] <= CASE_VIDE)) or
                   (li[M - s[-1] - 1] != CASE_NOIRE and
                    M - s[-1] - 2 >= 0 and
                    T_recursif(s[:-1], li[:M - s[-1] - 1], cache)))

        if li[M - 1] == CASE_NOIRE:
            cache[K, M] = b
            return cache[K, M]

        elif li[M - 1] == CASE_VIDE:
            cache[K, M] = b or T_recursif(s, li[:M - 1], cache)
            return cache[K, M]


def T(s, li):
    """ Appelle la fonction `T_recursif` avec un nouveau cache.
    Le fait de tester la grille avec des valeurs possiblement fausses dans la
    fonction `propagation` nous oblige a ne pas utiliser le même cache à
    chaque appel de `T`.
    """
    cache = dict()
    return T_recursif(s, li, cache)


def propag_once(grille, contraintes_lignes, contraintes_colonnes,
                indexes_a_voir, index_a_ajouter):
    """ Applique une demi-itération de l'algorithme de propagation décrit dans
    l'annexe.
    """
    for i in indexes_a_voir:
        # On itère sur toutes les cases vides pour éviter des itérations
        # superflues.
        for j in np.where(grille[i] == CASE_VIDE)[0]:
            cligne = contraintes_lignes[i]
            ccolonne = contraintes_colonnes[j]

            # On regarde si le cas où la case est noire est possible
            grille[i][j] = CASE_NOIRE
            t1 = T(cligne, grille[i]) and T(ccolonne, grille.T[j])

            # On regarde si le cas où la case est blanche est possible
            grille[i][j] = CASE_BLANCHE
            t2 = T(cligne, grille[i]) and T(ccolonne, grille.T[j])

            # On modifie la couleur de la case en conséquence
            if t1 and t2:
                # On ne peut rien déduire
                grille[i][j] = CASE_VIDE
            elif not t1 and not t2:
                # La grille n'admet pas de solution
                raise GrilleImpossible()
            else:
                if t1 and not t2:
                    grille[i][j] = CASE_NOIRE
                else:
                    grille[i][j] = CASE_BLANCHE
                index_a_ajouter |= {j}


def propagation(contraintes_lignes, contraintes_colonnes, grid):
    """ Résout une grille de nonogram avec une méthode de programmation
    dynamique. Correspond à l'algorithme demandé dans la question 7.
    """
    lignes_a_voir = set(range(len(contraintes_lignes)))
    colonnes_a_voir = set()
    while lignes_a_voir or colonnes_a_voir:
        # Application de l'algorithme de propagation sur les lignes à voir
        propag_once(grid, contraintes_lignes, contraintes_colonnes,
                    lignes_a_voir, colonnes_a_voir)
        lignes_a_voir = set()

        # Application de l'algorithme de propagation sur les colonnes à voir
        propag_once(grid.T, contraintes_colonnes, contraintes_lignes,
                    colonnes_a_voir, lignes_a_voir)
        colonnes_a_voir = set()


def solve(contraintes_lignes, contraintes_colonnes, grid):
    t1 = time()
    propagation(contraintes_lignes, contraintes_colonnes, grid)
    t2 = time()
    return grid, t2 - t1


def is_solvable(contraintes_lignes, contraintes_colonnes, grid):
    t1 = time()
    try:
        propagation(contraintes_lignes, contraintes_colonnes, grid)
        return True, time() - t1
    except GrilleImpossible:
        return False, time() - t1


if __name__ == '__main__':
    pass
