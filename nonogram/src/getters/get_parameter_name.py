import json
import os


_PATH_PARAMS_NAMES = "../../res/parameters_names.json"


def _get_name_from_file(value):
    path = os.path.join(os.path.dirname(__file__),
                        _PATH_PARAMS_NAMES)
    with open(path) as file:
        return json.load(file)[value]


def help_message() -> str:
    return _get_name_from_file("help")


def version() -> str:
    return _get_name_from_file("version")


def solving_method() -> str:
    return _get_name_from_file("solving_method")


if __name__ == '__main__':
    pass