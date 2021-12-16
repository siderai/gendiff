#!/usr/bin/env python3
import json

import argparse
import yaml


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()


def generate_diff(filepath1, filepath2, format_name):
    # identify the format of input files and parse them into Py object (dict)
    def decode(filepath):
        '''
        Yaml/json parser
        :param filepath: path of json/yaml
        :return: dict
        '''
        if filepath.endswith('.json'):
            file = json.load(open(filepath, mode='r'))
        else:
            yaml_format = ('.yaml', '.yml')
            if filepath.endswith(yaml_format):
                file = yaml.load(open(filepath, mode='r'), Loader=yaml.Loader)
        return file
    file1, file2 = decode(filepath1), decode(filepath2)


# generate list of output diff statements
result = ["{"]
for key in common_keys:
    if file1[key] == file2[key]:
        if not isinstance(file1[key], dict):
            result.append(f"  {key}: {file1[key]}")
    else:
        result.append(f"- {key}: {file1[key]}")
        result.append(f"+ {key}: {file2[key]}")
for key in first_only:
    result.append(f"- {key}: {file1[key]}")
for key in second_only:
    result.append(f"+ {key}: {file2[key]}")
result.append("}")
# convert list to string
result_str = "\n".join(x for x in result)
return result_str




