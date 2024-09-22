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
    print(f"Usage: {program_name} [options] <input.piled>")
    print("    -o <filename>        Specify output <filename>")


def error(message: str) -> None:
    print("ERROR: %s" % (message,))
    sys.exit(1)


def main() -> None:
    argv = sys.argv
    program_name, *argv = argv

    if len(argv) < 1:
        usage(program_name)
        sys.exit(1)

    out_filename = "output.out"
    in_filename = None

    while len(argv) > 0:
        arg, *argv = argv
        if arg == "--help":
            usage(program_name)
            sys.exit(0)
        elif arg == "-o":
            if len(argv) <= 0:
                error("not enough argument for `-o`")
            out_filename, *argv = argv
        else:
            in_filename = arg

    if in_filename is None:
        error("input-filename is not specified")

    generate_assembly(
        "output.asm",
        list([build_IR_from_token(parse_word_as_token(word)) for word in lex_file("tests/test.piled")])
    )
    call_cmd(["fasm", "output.asm"])
    call_cmd(["mv", "output", out_filename], echo=False)


if __name__ == "__main__":
    main()
