import typing as tt

from piled.common import Location
from piled.common import Word


def find_col(line: str, start: int, stop: tt.Callable[[str], bool]) -> int:
    col = start
    while col < len(line) and not stop(line[col]):
        col += 1
    return col


def lex_line(line: str) -> tt.Generator[tuple[int, str], None, None]:
    col = find_col(line, 0, lambda x: not x.isspace())
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace())
        yield col, line[col:col_end]
        col = find_col(line, col_end, lambda x: not x.isspace())


# TODO lex_file does not support any style of comment.
def lex_file(file_path: str) -> list[Word]:
    with open(file_path) as f:
        return [
            Word(file_path, Location(row, col), word)
            for (row, line) in enumerate(f.readlines())
            for (col, word) in lex_line(line)
        ]
