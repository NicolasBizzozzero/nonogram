import src.solveurs.dynamic_programming as dp
import src.solveurs.linear_programming as lp
from src.grille.parser import parse_instance
from src.grille.affichage import affiche_grille


NOMBRE_INSTANCES = 17
INSTANCE_PATTERN = "../instances/{index}.txt"


def main():
    for instance_index in range(NOMBRE_INSTANCES):
        file_path = INSTANCE_PATTERN.format(index=instance_index)
        contraintes_lignes, contraintes_colonnes = parse_instance(file_path)

        #grille1 = dp.resoudre(contraintes_lignes, contraintes_colonnes)
        grille2 = lp.resoudre(contraintes_lignes, contraintes_colonnes)

        # affiche_grille(grille1, "Instance {index}, DP".format(
        #    index=instance_index))
        affiche_grille(grille2, "Instance {index}, LP".format(
            index=instance_index))
        exit(0)


if __name__ == '__main__':
    main()
