import warnings

from nonogram.src.initialization.args_parser import \
    parse_args_main_entry_point
import nonogram.src.getters.environment as env
from nonogram.src.core.nonogram import nonogram


def main_entry_point():
    warnings.filterwarnings("ignore", module="matplotlib")

    parse_args_main_entry_point()
    nonogram(file=env.file,
             solving_method=env.solving_method,
             encoding=env.encoding)


if __name__ == '__main__':
    pass
