import numpy as np

from solveurs.solveur_utils import SolvingMethod, CASE_VIDE
from grille.parser import parse_instance
from grille.affichage import affiche_grille
import solveurs.dynamic_programming as dp
import solveurs.linear_programming as lp
import solveurs.dynamic_optimized_programming as dop


def nonogram(file, solving_method, encoding):
    constraints_lines, constraints_columns = parse_instance(file, encoding)
    grid = np.full((len(constraints_lines), len(constraints_columns)),
                   CASE_VIDE)
    grid = _solve(constraints_lines, constraints_columns, solving_method, grid)
    affiche_grille(grid, file)


def _solve(constraints_lines, constraints_columns, solving_method, grid):
    # TODO: Rename all methods 'solve'
    if solving_method == SolvingMethod.DYNAMIC:
        return dp.resoudre_dynamique(constraints_lines, constraints_columns, grid=grid)[0]

    elif solving_method == SolvingMethod.LINEAR:
        return lp.resoudre_linear(constraints_lines, constraints_columns,
                                  grid=grid, propagation=False)[0]

    elif solving_method == SolvingMethod.DYNAMIC_LINEAR:
        return lp.resoudre_linear(constraints_lines, constraints_columns,
                                  grid=grid, propagation=True)[0]

    elif solving_method == SolvingMethod.DYNAMIC_OPTIMIZED:
        # if instance_index == 15:
        #     poids_a, poids_b = 1, 0
        # else:
        #     poids_a, poids_b = 0, 1
        poids_a, poids_b = 0, 1
        grid, temps_resolution, nb_appels = dop.solve(constraints_lines,
                                                      constraints_columns,
                                                      grid=grid, max_call=100,
                                                      poids_a=poids_a,
                                                      poids_b=poids_b)
        return grid


if __name__ == '__main__':
    pass
