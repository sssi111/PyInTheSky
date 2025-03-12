#!/usr/bin/env python3

import sys


def main():
    if len(sys.argv) == 1:
        content = sys.stdin.buffer.read()
        lines = content.count(b"\n")
        words = len(content.split())
        bytes_count = len(content)
        print(f"{lines} {words} {bytes_count}")
    else:
        total_lines = 0
        total_words = 0
        total_bytes = 0
        processed_files = 0

        for filename in sys.argv[1:]:
            try:
                with open(filename, "rb") as f:
                    content = f.read()
            except FileNotFoundError:
                print(f"pywc: {filename}: No such file or directory", file=sys.stderr)
                continue
            except Exception as e:
                print(f"pywc: {filename}: {e}", file=sys.stderr)
                continue

            lines = content.count(b"\n")
            words = len(content.split())
            bytes_count = len(content)

            print(f"{lines} {words} {bytes_count} {filename}")

            total_lines += lines
            total_words += words
            total_bytes += bytes_count
            processed_files += 1

        if processed_files > 1:
            print(f"{total_lines} {total_words} {total_bytes} total")


if __name__ == "__main__":
    main()
