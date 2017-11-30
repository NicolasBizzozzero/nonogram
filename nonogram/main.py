from nonogram.src.core.initialization.args_parser import \
    parse_args_main_entry_point
import nonogram.src.getters.environment as env


def main_entry_point():
    parse_args_main_entry_point()
    nonogram(file=env.file,
             solving_method=env.solving_method)


if __name__ == '__main__':
    pass
