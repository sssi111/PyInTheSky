#!/usr/bin/env python3
import sys


def main():
    infile = sys.stdin

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            infile = open(filename, "r", encoding="utf-8", errors="replace")
        except FileNotFoundError:
            print(f"pynl: {filename}: No such file or directory", file=sys.stderr)
            return
        
    line_number = 1
    for line in infile:
        line = line.rstrip("\n")
        print(f"{line_number}\t{line}")
        line_number += 1

    if infile is not sys.stdin:
        infile.close()


if __name__ == "__main__":
    main()
