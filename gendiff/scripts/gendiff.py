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


if __name__ == '__main__':
    main()


def generate_diff(filepath1, filepath2, format_name):
    # identify the format of input files and parse them into dict
    def decode(filepath: str) -> file_: dict:
        '''
        Yaml/json parser
        :param filepath: path of json/yaml
        :return: dict
        '''
        if filepath.endswith('.json'):
            file_ = json.load(open(filepath, mode='r'))
        else:
            if filepath.endswith('.yaml', '.yml'):
                file_ = yaml.load(open(filepath, mode='r'), Loader=yaml.Loader)
        return file_
        
    file1, file2 = decode(filepath1), decode(filepath2)

