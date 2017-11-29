""" Contient toute sorte de décorateurs utiles pour le projet. """
from time import time

from grille.grille_utils import verifie_grille


def timeit(function):
    """ Affiche le temps d'execution d'une fonction. """
    def wrapper(*args, **kwargs):
        time_begin = time()
        result = function(*args, **kwargs)
        time_end = time()
        time_total = time_end - time_begin

        second_or_seconds = "seconde" if (time_total < 1) else "secondes"
        print("Temps d'execution pour \"{}\": {} {}".format(
            function.__name__, time_total, second_or_seconds))
        return result
    return wrapper


def check_solution(resoudre):
    """ Vérifie qu'une grille est bien résolue. """
    def wrapper(contraintes_lignes, contraintes_colonnes):
        grille = resoudre(contraintes_lignes, contraintes_colonnes)
        print(verifie_grille(grille, contraintes_lignes, contraintes_colonnes))
        return grille
    return wrapper


if __name__ == '__main__':
    pass
