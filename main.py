#!/usr/bin/env python3

import subprocess
import sys

from piled import build_IR_from_token
from piled import generate_assembly
from piled import lex_file
from piled import parse_word_as_token


def call_cmd(args: list[str], echo=True) -> None:
    if echo:
        print("[CMD] " + " ".join(args))
    subprocess.run(args, capture_output=True)


def usage(program_name: str) -> None:
    print(f"Usage: {program_name} <input.piled>")
    sys.exit(1)


def main() -> None:
    argv = sys.argv
    program_name = argv[0]

    argv = argv[1:]
    if len(argv) < 1:
        usage(program_name)

    generate_assembly(
        "output.asm",
        list([build_IR_from_token(parse_word_as_token(word)) for word in lex_file("tests/test.piled")])
    )
    call_cmd(["fasm", "output.asm"])
    call_cmd(["mv", "output", "output.out"], echo=False)


if __name__ == "__main__":
    main()
