# -*- coding: utf-8 -*-
""" Resout un nonograme en utilisant des méthodes de programmation linéaire.
Ce module contient toutes les fonctions utiles pour répondre aux questions de
la seconde partie du projet.
"""
from __future__ import print_function
import numpy as np
from time import time
from gurobipy import *

from nonogram.src.core.solveurs.solveur_utils import CASE_BLANCHE, CASE_NOIRE, CASE_VIDE
from nonogram.src.core.solveurs.dynamic_programming import resoudre_dynamique


MODEL_NAME = "nonogram_solver"


def PL(contraintes_lignes, contraintes_colonnes, grille, propagation):
    """ Applique l'algorithme du PL sur une grille de nonogram.
    Correspond à l'algorithme demandé dans la question 14.
    """
    global MODEL_NAME

    # Declaration
    N, M, = len(contraintes_lignes), len(contraintes_colonnes)
    model = Model(MODEL_NAME)
    model.setParam('OutputFlag', False)

    # Calcul des cases possibles (cases qui peuvent être noircies)
    autorisees_Y = cases_possibles(contraintes_lignes, N, M)
    autorisees_Z = cases_possibles(contraintes_colonnes, M, N)

    # Variables type 1 X i,j
    lx = np.array([[model.addVar(vtype=GRB.BINARY) for j in range(M)] for i in range(N)])

    # Variables type 2 Y i,j,t
    ly = np.array([[[model.addVar(vtype=GRB.BINARY) if j in autorisees_Y[i][t] else None for t in range(len(contraintes_lignes[i]))] for j in range(M)] for i in range(N)])

    # Variables type 2 Z i,j,t
    lz = np.array([[[model.addVar(vtype=GRB.BINARY) if i in autorisees_Z[j][t] else None for t in range(len(contraintes_colonnes[j]))] for i in range(N)] for j in range(M)])

    # Ajout des contraintes dans le cas d'une propagation préliminaire
    if propagation:
        cases_resolues = ajoute_contraintes(model, grille, contraintes_lignes,
                                            contraintes_colonnes, lx, ly, lz)

        # Cas où la programmation dynamique a déjà résolu la grille
        if cases_resolues == N * M:
            return (grille, 0)

    # lignes:
    # Yijt =1 0<=j < M un bloc commence a une seul case
    for i in range(N):
        for t in range(len(contraintes_lignes[i])):
            l1 = [ly[i, k][t] for k in range(M) if ly[i, k][t]]
            if len(l1) > 0:
                model.addConstr(quicksum(key1 for key1 in l1), GRB.EQUAL, 1)

    # l'ordre , Decalage et Q10
    for i in range(N):
        for j in range(M):
            for t in range(len(contraintes_lignes[i])):
                if ly[i, j][t]:
                    l1 = []
                    for t1 in range(t + 1, len(contraintes_lignes[i])):
                        l1 += [ly[i, k][t1] for k in range(j + contraintes_lignes[i][t] + 1) if k < M and ly[i, k][t1]]
                    if len(l1) > 0:
                        model.addConstr(len(l1) * ly[i, j][t] + quicksum(keyy for keyy in l1)<= len(l1))
                    l1 = [lx[i,k] for k in range(j, j + contraintes_lignes[i][t]) if k < M]
                    if len(l1) > 0:
                        model.addConstr(contraintes_lignes[i][t] * ly[i,j][t] <= quicksum(keyx for keyx in l1))
            for t in range(len(contraintes_colonnes[j])):
                if lz[j, i][t]:
                    l1 = []
                    for t1 in range(t + 1, len(contraintes_colonnes[j])):
                        l1 += [lz[j, k][t1] for k in range(i + contraintes_colonnes[j][t] + 1) if k < N and lz[j, k][t1]]
                    if len(l1) > 0:
                        model.addConstr(len(l1) * lz[j, i][t] + quicksum(keyz for keyz in l1) <= len(l1))
                    l1 = [lx[k, j] for k in range(i, i + contraintes_colonnes[j][t]) if k < N]
                    if len(l1) > 0:
                        model.addConstr(contraintes_colonnes[j][t] * lz[j,i][t] <= quicksum(keyx for keyx in l1))

    # Les colonnes
    # Zijt =1 0<=j < M un bloc commence a une seule case
    for j in range(M):
        for t in range(len(contraintes_colonnes[j])):
            l1 = [lz[j, i][t] for i in range(N) if lz[j, i][t]]
            if len(l1) > 0:
                model.addConstr(quicksum(key1 for key1 in l1), GRB.EQUAL, 1)

    # Résolution
    model.setObjective(sum(sum(lx)), GRB.MINIMIZE)
    model.update()
    t1 = time()
    model.optimize()
    t2 = time()

    # Construction de la grille. En effet, Gurobipy sauvegarde la solution de
    # la grille dans son vecteur de solution. Il faut récupèrer les valeurs et
    # les assigner à notre grille manuellement.
    for i in range(N):
        for j in range(M):
            if grille[i, j] == CASE_VIDE:
                valeurs = lx[i, j].x
                # Passage d'un flottant en entier
                if valeurs < 0 or (valeurs >= 0 and valeurs < .5):
                    grille[i, j] = CASE_BLANCHE
                else:
                    grille[i, j] = CASE_NOIRE

    return grille, t2 - t1


def ajoute_contraintes(model, grille, contraintes_lignes, contraintes_colonnes,
                       lx, ly, lz):
    """ Ajoute des contraintes au model en considèrant les valeurs déjà
    définies dans la grille. Cette fonction est utilisée pour une grille déjà
    pré-remplie. Elle evite à l'algorithme de programmation linéaire de
    calculer des contraintes déjà réalisées auparavant.
    """
    cases_resolues = 0
    for i in range(len(contraintes_lignes)):
        for j in range(len(contraintes_colonnes)):
            if grille[i, j] == CASE_NOIRE:
                model.addConstr(lx[i, j], GRB.EQUAL, 1)
                cases_resolues += 1
            elif grille[i, j] == CASE_BLANCHE:
                model.addConstr(lx[i, j], GRB.EQUAL, 0)
                cases_resolues += 1
                for t in range(len(contraintes_lignes[i])):
                    if ly[i, j][t]:
                        model.addConstr(ly[i, j][t], GRB.EQUAL, 0)
                for t in range(len(contraintes_colonnes[j])):
                    if lz[j, i][t]:
                        model.addConstr(lz[j, i][t], GRB.EQUAL, 0)
    return cases_resolues


def cases_possibles(sequence, N, M):
    """ Retourne la liste des cases possibles pour chaque bloc des N lignes
    de taille M.
    Si on veut appeller cette fonction sur les colonnes, il suffit d'inverser
    le N et le M.
    """
    cases_possibles = []
    for i in range(N):
        L = []
        l = sequence[i]
        for t in range(len(l)):
            cases_interdites = []
            o = 0
            # Les blocs avant
            for t1 in range(0, t):
                for h in range(l[t1]):
                    cases_interdites += [o]
                    o += 1
                # Cases blanches
                cases_interdites += [o]
                o += 1
            # Depasse la ligne
            for o in range(M - 1, 0, -1):
                if o + l[t] > M:
                    cases_interdites += [o]
            o = M - 1
            # Les blocs apres
            for t1 in range(len(l) - 1, t, -1):
                for h in range(l[t1]):
                    cases_interdites += [o]
                    o -= 1
                # Cases blanches
                cases_interdites += [o]
                o -= 1
            # Ne pas confondre entre le bloc actuel et les blocs d'apres
            for t1 in range(l[t], 1, -1):
                cases_interdites += [o]
                o -= 1
            L.append([case for case in range(M) if case not in cases_interdites])
        cases_possibles.append(L)
    return cases_possibles


def resoudre_linear(contraintes_lignes, contraintes_colonnes, propagation):
    """ Résout une grille de nonogram avec une méthode de programmation
    linéaire.
    """
    temps_dynamique = 0
    if propagation:
        grille, temps_dynamique = resoudre_dynamique(contraintes_lignes,
                                                     contraintes_colonnes)
    else:
        grille = np.full((len(contraintes_lignes), len(contraintes_colonnes)),
                         CASE_VIDE)

    grille, temps_lineaire = PL(contraintes_lignes, contraintes_colonnes,
                                grille, propagation)
    return grille, temps_lineaire, temps_dynamique


if __name__ == '__main__':
    pass
