#!/usr/bin/env python3

import sys

from piled import parse_word_as_token, lex_file

def main() -> None:
    argv = sys.argv
    program_name = argv[0]

    argv = argv[1:]
    if len(argv) < 1:
        print(f"Usage: {program_name} <input.piled>")
        sys.exit(1)

    print(list(map(lambda x: (x.type, x.value), [parse_word_as_token(word) for word in lex_file("tests/test.piled")])))


if __name__ == "__main__":
    main()
