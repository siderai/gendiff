#!/usr/bin/env
import argparse
from .logic import decoded, compared, format_stylish, format_plain, format_json


def generate_diff(filepath1, filepath2, format_="stylish"):
    file1, file2 = decoded(filepath1), decoded(filepath2)
    diff = compared(file1, file2)
    if format_ == "json":
        return format_json(diff)
    elif format_ == "plain":
        return format_plain(diff)
    else:
        return format_stylish(diff)


def main():
    parser = argparse.ArgumentParser(description="Generate diff")
    parser.add_argument("first_file", type=str)
    parser.add_argument("second_file", type=str)
    parser.add_argument(
        "-f", "--format", default="stylish", help="set format of output"
    )
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file, format_=args.format))


if __name__ == "__main__":
    main()
