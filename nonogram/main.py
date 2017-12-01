from nonogram.src.initialization.args_parser import \
    parse_args_main_entry_point
import nonogram.src.getters.environment as env
from nonogram.src.core.nongram import nonogram


def main_entry_point():
    print("Yoooo")
    parse_args_main_entry_point()
    nonogram(file=env.file,
             solving_method=env.solving_method)


if __name__ == '__main__':
    pass
