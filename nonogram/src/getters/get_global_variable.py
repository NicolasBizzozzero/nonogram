import json
import os


_PATH_GLOBAL_VARIABLES = "../../res/global_variables.json"


def _get_value_from_file(value):
    path = os.path.join(os.path.dirname(__file__),
                        _PATH_GLOBAL_VARIABLES)
    with open(path) as file:
        return json.load(file)[value]


def name():
    return _get_value_from_file("name")


def description():
    return _get_value_from_file("description")


def keywords():
    return _get_value_from_file("keywords")


def main_homepage():
    return _get_value_from_file("main_homepage")


def download_url():
    return _get_value_from_file("download_url")


def version():
    return _get_value_from_file("version")


def author():
    return _get_value_from_file("author")


def maintainer():
    return _get_value_from_file("maintainer")


def email():
    return _get_value_from_file("email")


def status():
    return _get_value_from_file("status")


def copyright_text():
    return _get_value_from_file("copyright")


def credits_authors():
    return _get_value_from_file("credits")


def license_used():
    return _get_value_from_file("license")


def classifiers():
    return _get_value_from_file("classifiers")


def dependencies():
    return _get_value_from_file("dependencies")


def main_entry_point():
    return _get_value_from_file("main_entry_point")


if __name__ == '__main__':
    pass
