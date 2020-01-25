import numpy as np

from nonogram.src.core.solveurs.solveur_utils import SolvingMethod, CASE_VIDE
from nonogram.src.core.grille.parser import parse_instance
from nonogram.src.core.grille.affichage import affiche_grille
import nonogram.src.core.solveurs.dynamic_programming as dp
import nonogram.src.core.solveurs.linear_programming as lp
import nonogram.src.core.solveurs.dynamic_optimized_programming as dop


def nonogram(file, solving_method, encoding):
    constraints_lines, constraints_columns = parse_instance(file, encoding)
    grid = np.full((len(constraints_lines), len(constraints_columns)),
                   CASE_VIDE)
    grid = _solve(constraints_lines, constraints_columns, solving_method, grid)
    affiche_grille(grid, file)


def _solve(constraints_lines, constraints_columns, solving_method, grid):
    if solving_method == SolvingMethod.DYNAMIC:
        return dp.solve(constraints_lines, constraints_columns, grid=grid)[0]

    elif solving_method == SolvingMethod.LINEAR:
        return lp.solve(constraints_lines, constraints_columns,
                        grid=grid, propagation=False)[0]

    elif solving_method == SolvingMethod.DYNAMIC_LINEAR:
        return lp.solve(constraints_lines, constraints_columns,
                        grid=grid, propagation=True)[0]

    elif solving_method == SolvingMethod.DYNAMIC_OPTIMIZED:
        weight_len, weight_colored = 0, 1
        return dop.solve(constraints_lines, constraints_columns,
                         grid=grid, max_call=100,
                         weight_len=weight_len,
                         weight_colored=weight_colored)[0]


if __name__ == '__main__':
    pass
