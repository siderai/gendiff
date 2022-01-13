#!/usr/bin/env python3
from gendiff.logic.logic import decoded, compared, str_formatter
from gendiff.tests.fixtures

import argparse


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()


if __name__ == '__main__':
    main()


def generate_diff(filepath1, filepath2):
    # identify the format of input files and parse them into dict
    file1, file2 = decoded(filepath1), decoded(filepath2)
    diff = compared(file1, file2)
    result = str_formatter(diff)
    return result


