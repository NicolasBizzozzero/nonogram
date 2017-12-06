# -*- coding: utf-8 -*-
from __future__ import print_function
import pylab as plt
from  matplotlib.patches import  Rectangle
from matplotlib.collections import PatchCollection

from nonogram.src.core.grille.grille_utils import CHAR_NOIR, CHAR_BLANC, CHAR_VIDE


def dessiner(grille):
    for ligne in grille:
        for case in ligne:
            if case == 1:
                char_to_print = CHAR_NOIR
            elif case == -1:
                char_to_print = CHAR_BLANC
            elif case == 0:
                char_to_print = CHAR_VIDE
            print(char_to_print, end="")
        print("\n", end="")


def affiche_grille(grille, titre):
    # Divers préparatifs
    n = len(grille)
    m = len(grille[0])
    plt.rcParams['figure.figsize'] = int((m * 5) / n), 5
    plt.subplots_adjust(bottom=0.02, top=0.92, left=0.02, right=0.98)
    graphe = plt.subplot(1, 1, 1)
    graphe.get_xaxis().set_visible(False)
    graphe.get_yaxis().set_visible(False)
    plt.axis([0, len(grille[0]), n, 0])
    plt.suptitle(titre, fontsize=24)

    # Carrés noirs dans les cases interdites
    CN = []
    CB = []
    CG = []
    for i in range(n):
        for j in range(len(grille[i])):
            if grille[i][j] == 1:
                CN.append(Rectangle((j, i), 1, 1, color="black"))
            elif grille[i][j] == -1:
                CB.append(Rectangle((j, i), 1, 1, color="white"))
            elif grille[i][j] == 0:
                CG.append(Rectangle((j, i), 1, 1, color="grey"))
    if CN != []:
        graphe.add_collection(PatchCollection(CN, match_original=True))
    if CB != []:
        graphe.add_collection(PatchCollection(CB, match_original=True))
    if CG != []:
        graphe.add_collection(PatchCollection(CG, match_original=True))
    plt.show()


if __name__ == '__main__':
    pass
