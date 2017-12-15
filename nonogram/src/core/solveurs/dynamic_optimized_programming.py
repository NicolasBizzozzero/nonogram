# -*- coding: utf-8 -*-
""" Resout un nonograme en utilisant des méthodes de programmation dynamique
optimisée.
"""

import numpy as np
from time import time

from nonogram.src.core.solveurs.solveur_utils import CASE_BLANCHE,\
    CASE_NOIRE, CASE_VIDE, GrilleImpossible
from nonogram.src.core.solveurs.dynamic_programming import is_solvable
from nonogram.src.core.solveurs.linear_programming import PL


def index_score(i, j, line_constraints, column_constraints, colored_lines,
                colored_columns, weight_len, weight_colored):
    """ Compute the score of an index.
    The higher the score, the less recursive call of the solving function will
    be made.
    """
    return weight_len * (len(line_constraints[i]) + len(column_constraints[j])) +\
        weight_colored * (colored_lines[i] + colored_columns[j])


def find_best_index(line_constraints, column_constraints, grid, l, N, M,
                    weight_len, weight_colored):
    """ Seek the best index minimsing the number of recursive call to the
    solving function.
    """
    colored_lines = np.array(
        [len(list(np.where(grid[i] != CASE_VIDE)[0])) for i in range(N)])
    colored_columns = np.array(
        [len(list(np.where(grid.T[i] != CASE_VIDE)[0])) for i in range(M)])
    i, j = l[0]
    i_max, j_max = l[0]
    val_max = index_score(i, j, line_constraints, column_constraints,
                          colored_lines, colored_columns, weight_len,
                          weight_colored)
    for i, j in l[1:]:
        val = index_score(i, j, line_constraints, column_constraints,
                          colored_lines, colored_columns, weight_len,
                          weight_colored)
        if val > val_max:
            val_max, i_max, j_max = val, i, j
    return i_max, j_max


def dynamic_optimized(line_constraints, column_constraints, grid, nb_calls, borne, N, M, weight_len, weight_colored):
    if borne > 0 and nb_calls > borne:
        return grid, False, nb_calls

    l = [(i, j) for i in range(N) for j in range(M) if grid[i][j] == CASE_VIDE]
    if len(l) == 0:
        # The grid has been completed none of the element is empty
        return grid, True, nb_calls

    grid_copy = deepcopy(grid)
    i, j = find_best_index(
        line_constraints, column_constraints, grid, l, N, M, weight_len, weight_colored)
    grid_copy[i, j] = NOIRE
    possible, _ = resoudre_dynamique(
        line_constraints, column_constraints, grid_copy)
    if possible:
        grid_finished, complete, nb_calls = dynamic_optimized(
            line_constraints, column_constraints, grid_copy, nb_calls + 1, borne, N, M, weight_len, weight_colored)
        if complete:
            return grid_finished, complete, nb_calls
    grid_copy = deepcopy(grid)
    grid_copy[i, j] = CASE_BLANCHE
    possible, td_etap = resoudre_dynamique(
        line_constraints, column_constraints, grid_copy)
    if possible:
        grid_finished, complete, nb_calls = dynamic_optimized(
            line_constraints, column_constraints, grid_copy, nb_calls + 1, borne, N, M, weight_len, weight_colored)
        if complete:
            return grid_finished, complete, nb_calls
    return grid, False, nb_calls


def solve(line_constraints, column_constraints, grid, borne, weight_len=0, weight_colored=1):
    N, M = len(line_constraints), len(column_constraints)

    is_solvable, td = is_solvable(
        line_constraints, column_constraints, grid)
    if not is_solvable:
        raise GrilleImpossible()

    t0 = time()
    grid, complete, nb_calls = dynamic_optimized(
        line_constraints, column_constraints, grid, 0, borne, N, M, weight_len, weight_colored)
    t1 = time()
    if complete:
        return grid, td + (t1 - t0), nb_calls
    else:
        # We fallback to linear programming to complete the grid
        grid, temps_lineaire = PL(line_constraints, column_constraints,
                                  grid, propagation=True)
        return grid, td + (t1 - t0) + temps_lineaire, nb_calls


if __name__ == '__main__':
    pass
