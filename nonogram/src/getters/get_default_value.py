import json
import os


_PATH_DEFAULT_VALUES = "../../res/default_values.json"


def _get_value_from_file(value):
    path = os.path.join(os.path.dirname(__file__),
                        _PATH_DEFAULT_VALUES)
    with open(path) as file:
        return json.load(file)[value]


def solving_method():
    return _get_value_from_file("solving_method")


def encoding():
    return _get_value_from_file("encoding")


if __name__ == '__main__':
    pass
