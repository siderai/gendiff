#!/usr/bin/env
from logic import decoded, compared, str_formatter

import argparse


def generate_diff(filepath1, filepath2):
    file1, file2 = decoded(filepath1), decoded(filepath2)
    diff = compared(file1, file2)
    result = str_formatter(diff)
    return result


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))

    if __name__ == '__main__':
        main()
