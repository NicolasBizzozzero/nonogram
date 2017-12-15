import json
import os


_PATH_PARAMS_NAMES = "../../res/parameters_names.json"


def _get_name_from_file(value):
    path = os.path.join(os.path.dirname(__file__),
                        _PATH_PARAMS_NAMES)
    with open(path) as file:
        return json.load(file)[value]


def file():
    return _get_name_from_file("file")


def help_message():
    return _get_name_from_file("help")


def version():
    return _get_name_from_file("version")


def solving_method():
    return _get_name_from_file("solving_method")


def encoding():
    return _get_name_from_file("encoding")


if __name__ == '__main__':
    pass
