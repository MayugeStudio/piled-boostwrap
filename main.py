#!/usr/bin/env python3

import os
import subprocess
import sys

from piled import cross_references
from piled import generate_assembly
from piled import lex_file
from piled import parse_word_as_token


# TODO: call_cmd doesn't handle any type of error
def call_cmd(args: list[str], echo=True, capture=True) -> None:
    if echo:
        print("[CMD] " + " ".join(args))
    subprocess.run(args, capture_output=capture)


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

    in_filename = None
    out_filename = None
    with_run = False

    while len(argv) > 0:
        arg, *argv = argv
        if arg == "--help":
            usage(program_name)
            sys.exit(0)
        elif arg == "-o":
            if len(argv) <= 0:
                error("not enough argument for `-o`")
            out_filename, *argv = argv
        elif arg == "-r":
            with_run = True
        else:
            in_filename = arg

    if in_filename is None:
        error("input-filename is not specified")

    piled_ext = ".piled"
    base_name = os.path.basename(in_filename)
    if base_name.endswith(piled_ext):
        base_name = base_name[:-len(piled_ext)]

    if out_filename is None:
        out_filename = base_name + ".out"
    else:
        base_name = out_filename

    print("[INFO] Generating %s" % (base_name + ".asm"))
    generate_assembly(
        base_name + ".asm",
        cross_references([parse_word_as_token(word) for word in lex_file(in_filename)])
    )
    call_cmd(["fasm", base_name + ".asm"])
    call_cmd(["mv", base_name, out_filename], echo=False)

    if with_run:
        call_cmd(["./" + out_filename], capture=False)


if __name__ == "__main__":
    main()
