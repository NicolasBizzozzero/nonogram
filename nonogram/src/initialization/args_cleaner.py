""" This module contains all functions related to cleaning command-line
arguments parsed by the `docopt` package (listed as a dependency). It mainly
convert string values to their numeric and enum counterpart. It also checks
if some of the parameters are invalids and raises exceptions accordingly.
"""

import nonogram.src.getters.get_parameter_name as gpn
import nonogram.src.getters.environment as env
from nonogram.src.core.solveurs.solveur_utils import \
    str_to_solving_method


_KEY_FILE = "<" + gpn.file().split()[-1] + ">"
_KEY_SOLVING_METHOD = gpn.solving_method().split()[-1]
_KEY_ENCODING = gpn.encoding().split()[-1]


def clean_arguments(args):
    """ Clean the command-line arguments parsed by the `docopt` package.
    It mainly convert string values to their numeric and enum counterpart.
    It also checks if some of the parameters are invalids and raises
    exceptions accordingly.
    """
    env.file = args[_KEY_FILE]
    env.solving_method = str_to_solving_method(args[_KEY_SOLVING_METHOD])
    env.encoding = args[_KEY_ENCODING]
