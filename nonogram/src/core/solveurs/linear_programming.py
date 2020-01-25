# -*- coding: utf-8 -*-
""" Resout un nonograme en utilisant des méthodes de programmation linéaire.
Ce module contient toutes les fonctions utiles pour répondre aux questions de
la seconde partie du projet.
"""
from __future__ import print_function
import numpy as np
from time import time

from nonogram.src.core.solveurs.solveur_utils import CASE_BLANCHE, CASE_NOIRE, CASE_VIDE
from nonogram.src.core.solveurs.dynamic_programming import solve as solve_dynamic


MODEL_NAME = "nonogram_solver"


def PL(line_constraints, column_constraints, grid, propagation):
    """ Applique l'algorithme du PL sur une grid de nonogram.
    Correspond à l'algorithme demandé dans la question 14.
    """
    global MODEL_NAME

    from gurobipy import Model, GRB, quicksum

    # Declaration
    N, M, = len(line_constraints), len(column_constraints)
    model = Model(MODEL_NAME)
    model.setParam('OutputFlag', False)

    # Calcul des cases possibles (cases qui peuvent être noircies)
    autorisees_Y = cases_possibles(line_constraints, N, M)
    autorisees_Z = cases_possibles(column_constraints, M, N)

    # Variables type 1 X i,j
    lx = np.array([[model.addVar(vtype=GRB.BINARY) for j in range(M)] for i in range(N)])

    # Variables type 2 Y i,j,t
    ly = np.array([[[model.addVar(vtype=GRB.BINARY) if j in autorisees_Y[i][t] else None
                        for t in range(len(line_constraints[i]))] for j in range(M)] for i in range(N)])

    # Variables type 2 Z i,j,t
    lz = np.array([[[model.addVar(vtype=GRB.BINARY) if i in autorisees_Z[j][t] else None
                        for t in range(len(column_constraints[j]))] for i in range(N)] for j in range(M)])

    # Ajout des contraintes dans le cas d'une propagation préliminaire
    if propagation:
        cases_resolues = ajoute_contraintes(model, grid, line_constraints,
                                            column_constraints, lx, ly, lz)

        # Cas où la programmation dynamique a déjà résolu la grid
        if cases_resolues == N * M:
            return (grid, 0)

    # lignes:
    # Yijt =1 0<=j < M un bloc commence a une seul case
    for i in range(N):
        for t in range(len(line_constraints[i])):
            l1 = [ly[i, k][t] for k in range(M) if ly[i, k][t]]
            if len(l1) > 0:
                model.addConstr(quicksum(key1 for key1 in l1), GRB.EQUAL, 1)

    # l'ordre , Decalage et Q10
    for i in range(N):
        for j in range(M):
            for t in range(len(line_constraints[i])):
                if ly[i, j][t]:
                    l1 = []
                    for t1 in range(t + 1, len(line_constraints[i])):
                        l1 += [ly[i, k][t1] for k in range(j + line_constraints[i][t] + 1) if k < M and ly[i, k][t1]]
                    if len(l1) > 0:
                        model.addConstr(len(l1) * ly[i, j][t] + quicksum(keyy for keyy in l1) <= len(l1))
                    l1 = [lx[i, k] for k in range(j, j + line_constraints[i][t]) if k < M]
                    if len(l1) > 0:
                        model.addConstr(line_constraints[i][t] * ly[i, j][t] <= quicksum(keyx for keyx in l1))
            for t in range(len(column_constraints[j])):
                if lz[j, i][t]:
                    l1 = []
                    for t1 in range(t + 1, len(column_constraints[j])):
                        l1 += [lz[j, k][t1] for k in range(i + column_constraints[j][t] + 1) if k < N and lz[j, k][t1]]
                    if len(l1) > 0:
                        model.addConstr(len(l1) * lz[j, i][t] + quicksum(keyz for keyz in l1) <= len(l1))
                    l1 = [lx[k, j] for k in range(i, i + column_constraints[j][t]) if k < N]
                    if len(l1) > 0:
                        model.addConstr(column_constraints[j][t] * lz[j, i][t] <= quicksum(keyx for keyx in l1))

    # Les colonnes
    # Zijt =1 0<=j < M un bloc commence a une seule case
    for j in range(M):
        for t in range(len(column_constraints[j])):
            l1 = [lz[j, i][t] for i in range(N) if lz[j, i][t]]
            if len(l1) > 0:
                model.addConstr(quicksum(key1 for key1 in l1), GRB.EQUAL, 1)

    # Résolution
    model.setObjective(sum(sum(lx)), GRB.MINIMIZE)
    model.update()
    t1 = time()
    model.optimize()
    t2 = time()

    # Construction de la grid. En effet, Gurobipy sauvegarde la solution de
    # la grid dans son vecteur de solution. Il faut récupèrer les valeurs et
    # les assigner à notre grid manuellement.
    for i in range(N):
        for j in range(M):
            if grid[i, j] == CASE_VIDE:
                valeurs = lx[i, j].x
                # Passage d'un flottant en entier
                if valeurs < 0 or (valeurs >= 0 and valeurs < .5):
                    grid[i, j] = CASE_BLANCHE
                else:
                    grid[i, j] = CASE_NOIRE

    return grid, t2 - t1


def ajoute_contraintes(model, grid, line_constraints, column_constraints,
                       lx, ly, lz):
    """ Ajoute des contraintes au model en considèrant les valeurs déjà
    définies dans la grid. Cette fonction est utilisée pour une grid déjà
    pré-remplie. Elle evite à l'algorithme de programmation linéaire de
    calculer des contraintes déjà réalisées auparavant.
    """
    from gurobipy import GRB

    cases_resolues = 0
    for i in range(len(line_constraints)):
        for j in range(len(column_constraints)):
            if grid[i, j] == CASE_NOIRE:
                model.addConstr(lx[i, j], GRB.EQUAL, 1)
                cases_resolues += 1
            elif grid[i, j] == CASE_BLANCHE:
                model.addConstr(lx[i, j], GRB.EQUAL, 0)
                cases_resolues += 1
                for t in range(len(line_constraints[i])):
                    if ly[i, j][t]:
                        model.addConstr(ly[i, j][t], GRB.EQUAL, 0)
                for t in range(len(column_constraints[j])):
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


def solve(line_constraints, column_constraints, grid, propagation):
    """ Résout une grid de nonogram avec une méthode de programmation
    linéaire.
    """
    temps_dynamique = 0
    if propagation:
        grid, temps_dynamique = solve_dynamic(line_constraints, column_constraints, grid)

    grid, temps_lineaire = PL(line_constraints, column_constraints, grid, propagation)
    return grid, temps_lineaire, temps_dynamique


if __name__ == '__main__':
    pass
