import json
import os


_PATH_PARAMS_DOC = "../../res/parameters_documentation.json"


def _get_doc_from_file(value):
    path = os.path.join(os.path.dirname(__file__),
                        _PATH_PARAMS_DOC)
    with open(path) as file:
        return json.load(file)[value]


def usage():
    return _get_doc_from_file("usage")


def help_message():
    return _get_doc_from_file("help")


def version():
    return _get_doc_from_file("version")


def solving_method():
    return _get_doc_from_file("solving_method")


def encoding():
    return _get_doc_from_file("encoding")


if __name__ == '__main__':
    pass
