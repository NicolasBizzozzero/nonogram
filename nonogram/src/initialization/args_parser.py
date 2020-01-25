""" This module contains all functions related to parsing command-line
arguments for all entry points of the software. It uses the `docopt` package
(listed as a dependency) to easily combine the tedious task of writing
documentation and parsing arguments. Each parsing function contains a very
long documentation string which will be the string displayed with the --help
parameter. This string contains a lot of format-style parameters and has for
purpose to organize them into the best way possible for reading the
documentation. Each of these format-style parameters are defined inside the
`_FORMAT_DICTIONARY` variable at the beginning of the module. This dictionary
link theses variables with their respective value in the files located in the
`res` directory at the root of the software. This complex parsing method
allows to have the arguments, their documentation and default values to be
defined in only one location (the `res` folder) for a quicker and easier
maintenance.
"""

import docopt

import nonogram.src.getters.get_default_value as gdv
import nonogram.src.getters.get_global_variable as ggv
import nonogram.src.getters.get_parameter_documentation as gpd
import nonogram.src.getters.get_parameter_name as gpn
import nonogram.src.getters.get_entry_point_documentation as gepd
from nonogram.src.initialization.args_cleaner import clean_arguments


_FORMAT_DICTIONARY = dict(
    # Documentation
    doc_usage=gpd.usage(),
    doc_help_message=gpd.help_message(),
    doc_version=gpd.version(),
    doc_solving_method=gpd.solving_method(),
    doc_encoding=gpd.encoding(),

    # Parameters
    param_file=gpn.file(),
    param_help_message=gpn.help_message(),
    param_version=gpn.version(),
    param_solving_method=gpn.solving_method(),
    param_encoding=gpn.encoding(),

    # Default values
    default_solving_method=gdv.solving_method(),
    default_encoding=gdv.encoding(),

    # Miscellaneous
    global_name=ggv.name()
)


def parse_args_main_entry_point():
    """ This method used the `docopt` package (listed as a dependency) to
    easily combine the tedious task of writing documentation and parsing
    arguments.
    It contains a very long documentation string which will be the string
    displayed with the --help parameter. This string contains a lot of
    format-style parameters and has for purpose to organize them into the
    best way possible for reading the documentation. Each of these
    format-style parameters are defined inside the `_FORMAT_DICTIONARY`
    variable at the beginning of the module. This dictionary link theses
    variables with their respective value in the files located in the `res`
    directory at the root of the software. This complex parsing method allows
    to have the arguments, their documentation and default values to be
    defined in only one location (the `res` folder) for a quicker and easier
    maintenance.
    """
    documentation = gepd.main_entry_point()
    _parse_args(documentation)


def _parse_args(documentation):
    global _FORMAT_DICTIONARY

    # Format the string twice because all the "doc_" variables contains default variables which need to be formatted too
    documentation = documentation.format(**_FORMAT_DICTIONARY).format(**_FORMAT_DICTIONARY)

    arguments = docopt.docopt(documentation, version=ggv.version(), help=True)
    clean_arguments(arguments)


if __name__ == "__main__":
    pass
