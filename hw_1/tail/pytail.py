#!/usr/bin/env python3

import sys


def print_tail(filename, n, print_header):
    try:
        with open(filename, "r") as f:
            if print_header:
                print(f"==> {filename} <==")
            lines = f.readlines()
            tail = lines[-n:]
            print("".join(tail), end="")
    except FileNotFoundError:
        print(
            f"pytail: cannot open '{filename}' for reading: No such file or directory",
            file=sys.stderr,
        )


def process_stdin():
    lines = sys.stdin.readlines()
    tail = lines[-17:]
    print("".join(tail), end="")


if __name__ == "__main__":
    files = sys.argv[1:]
    if not files:
        process_stdin()
    else:
        multiple_files = len(files) > 1
        for filename in files:
            print_tail(filename, 10, multiple_files)
