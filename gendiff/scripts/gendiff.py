#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file)


if __name__ == '__main__':
    main()

def generate_diff(file1, file2):
    json1 = json.load(open('~/python-project-lvl2/gendiff/tests/file1.json'))
    json2 = json.load(open('~/python-project-lvl2/gendiff/tests/file2.json'))
    common_keys = json1.keys() & json2.keys()
    first_only = json1.keys() - json2.keys()
    second_only = json2.keys() - json1.keys()
    result = ["{",]
    for key in common_keys:
        if json1[key] == json2[key]:
            result.append(f"  {key}: {json1[key]}")
        else:
            result.append(f"- {key}: {json1[key]}")
            result.append(f"+ {key}: {json2[key]}")
    for key in first_only:
        result.append(f"- {key}: {json1[key]}")
    for key in second_only:
        result.append(f"+ {key}: {json2[key]}")
    result.append("}")
    for item in result:
        item += "\n"
    return result


