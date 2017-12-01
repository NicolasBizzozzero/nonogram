# -*- coding: utf-8 -*-
import numpy as np

from solveurs.solveur_utils import CASE_BLANCHE, CASE_NOIRE, CASE_VIDE,\
    GrilleImpossible
from vrac.decorateurs import timeit, check_solution


def T_sans_ligne(j, l, s):
    """ Retourne `True` si on peut colorier de la case `0` à `j` la
    sous-séquence de `s` des `l` premiers blocs.
    Version 'Dynamic Programming', ne tient pas compte de l'état des cases en
    cours de calcul.
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


def T_recursif(s, li):
    K, M = len(s), len(li)
    if K == 0:
        return not (CASE_NOIRE in li)

    elif M < s[-1]:
        return False

    elif M == s[-1]:
        if K > 1:
            return False
        return not (CASE_BLANCHE in li)

    elif M > s[-1]:
        if li[M - 1] == CASE_BLANCHE:
            return T_recursif(s, li[:M - 1])

        b = np.all(li[M - s[-1]:] >= CASE_VIDE) and \
                  ((K == 1 and np.all(li[:M - s[-1]] <= CASE_VIDE)) or \
                    (li[M - s[-1] - 1] != CASE_NOIRE and \
                        M - s[-1] - 2 >= 0 and \
                        T_recursif(s[:-1], li[:M - s[-1] - 1])))

        if li[M - 1] == CASE_NOIRE:
            return b
       
        elif li[M - 1] == CASE_VIDE:
            return b or T_recursif(s, li[:M - 1])
    return True


def T(sequence, li):
    M, k = len(li), len(sequence) + 1
    tab = np.array([[False  for _ in range(k)] for _ in range(M)])
    for j in range(M):
        for l in range(k):
            if l == 0:
                tab[j, l] = np.all(li[:j + 1] != CASE_NOIRE)

            elif (l == 1) and (j == sequence[l - 1] - 1):
                tab[j, l] = np.all(li[:j + 1] != CASE_BLANCHE)

            elif j > sequence[l - 1] - 1:
                if li[j] == CASE_BLANCHE:
                    tab[j, l] = tab[j - 1, l]
                else:
                    b = np.all(li[j - sequence[l - 1] + 1:j] != CASE_BLANCHE) and\
                    ((l == 1 and np.all(li[:j - sequence[l - 1] + 1] != CASE_NOIRE)) or \
                    (li[j - sequence[l - 1]] != CASE_NOIRE and j - sequence[l -1 ] - 1 != CASE_BLANCHE and tab[j - sequence[l - 1] - 1, l - 1]))

                    if li[j] == CASE_NOIRE:
                            tab[j, l] = b
                    else:
                        tab[j, l] = b or tab[j - 1, l]

        if tab[j, -1] and np.all(li[j + 1:] != CASE_NOIRE):
            return True
    return tab[M - 1, k - 1]


def propagation(grille, contraintes_lignes, contraintes_colonnes,
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
            t2 =  T(cligne, grille[i]) and T(ccolonne, grille.T[j])

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


@check_solution
@timeit
def resoudre(contraintes_lignes, contraintes_colonnes):
    # Initialisation des variables
    N, M = len(contraintes_lignes), len(contraintes_colonnes)
    grille = np.full((N, M), CASE_VIDE)
    lignes_a_voir = set(range(N))
    colonnes_a_voir = set()

    while lignes_a_voir or colonnes_a_voir:
        # Application de l'algorithme de propagation sur les lignes à voir
        propagation(grille, contraintes_lignes, contraintes_colonnes,
                    lignes_a_voir, colonnes_a_voir)
        lignes_a_voir = set()

        # Application de l'algorithme de propagation sur les colonnes à voir
        propagation(grille.T, contraintes_colonnes, contraintes_lignes,
                    colonnes_a_voir, lignes_a_voir)
        colonnes_a_voir = set()
    return grille


if __name__ == '__main__':
    pass
