#!/usr/bin/env python3

import sys

from piled import lex_file

def main() -> None:
    argv = sys.argv
    program_name = argv[0]

    argv = argv[1:]
    if len(argv) < 1:
        print(f"Usage: {program_name} <input.piled>")
        sys.exit(1)

    print(lex_file("tests/test.piled"))


if __name__ == "__main__":
    main()
