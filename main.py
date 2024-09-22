#!/usr/bin/env python3

import sys

def main() -> None:
    argv = sys.argv
    program_name = argv[0]

    argv = argv[1:]
    if len(argv) < 1:
        print(f"Usage: {program_name} <input.piled>")
        sys.exit(1)


if __name__ == "__main__":
    main()
