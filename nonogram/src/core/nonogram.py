from nonogram.src.core.solveurs.solveur_utils import SolvingMethod
from nonogram.src.core.grille.parser import parse_instance
import nonogram.src.core.solveurs.dynamic_programming as dp
import nonogram.src.core.solveurs.linear_programming as lp
from nonogram.src.core.grille.affichage import affiche_grille


def nonogram(file, solving_method):
    constraints_lines, constraints_columns = parse_instance(file)
    grid = _solve(constraints_lines, constraints_columns, solving_method)
    affiche_grille(grid, file)


def _solve(constraints_lines, constraints_columns, solving_method):
    if solving_method == SolvingMethod.DYNAMIC:
        return dp.resoudre_dynamique(constraints_lines, constraints_columns)[0]

    elif solving_method == SolvingMethod.LINEAR:
        return lp.resoudre_linear(constraints_lines, constraints_columns, propagation=False)[0]

    elif solving_method == SolvingMethod.BOTH:
        return lp.resoudre_linear(constraints_lines, constraints_columns, propagation=True)[0]


if __name__ == '__main__':
    pass
