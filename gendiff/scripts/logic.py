import json

import yaml


def decoded(filepath: str) -> dict:
    """ Yaml/json parser. """

    if filepath.endswith('.json'):
        return json.load(open(filepath))
    else:
        yaml_format = ('.yaml', '.yml')
        if filepath.endswith(yaml_format):
            return yaml.load(open(filepath, mode='r'), Loader=yaml.Loader)



def compared(file1: dict, file2: dict) -> dict:
    """
    Compare two dicts and create image of their difference.
    In addition to original keys, there are signs that store difference of dicts:
        1. '-': the item is only in 1st file (and its value is not a dict);
        2. '+': the item is only in 2nd file (and its value is not a dict);
        3. '=': items are equal;
        4. ' ': keys are equal, but values are dicts
                                and should be compared recursively.
    """
    # check if input is correct
    if isinstance(file1, dict) and isinstance(file2, dict):
        # compare keys of the dicts
        common_keys = file1.keys() & file2.keys()
        first_only = file1.keys() - file2.keys()
        second_only = file2.keys() - file1.keys()

    # create operational image of difference
    diff = {}
    for key in common_keys:
        if file1[key] == file2[key]:
            diff[('=', key)] = file1[key]
        else:
            if isinstance(file1[key], dict) and isinstance(file2[key], dict):
                diff[(' ', key)] = compared(file1[key], file2[key])
            else:
                diff[('-', key)] = file1[key]
                diff[('+', key)] = file2[key]
    for key in first_only:
        diff[('-', key)] = file1[key]
    for key in second_only:
        diff[('+', key)] = file2[key]

    return diff


def str_formatter(diff: dict) -> str:
    """ Prepare diff for output as json-like string. """
    blank = []
    for sign, key in diff:
        if sign == '=':
            blank.append(f'    {key}: {diff[(sign, key)]}')
        else:
            blank.append(f'  {sign} {key}: {diff[(sign, key)]}')

    blank = sorted(blank, key=lambda x: x[4]) # index of key's first char
    blank.insert(0, '{')
    blank.append('}')
    result = '\n'.join(blank)
    print(result)


def plain_formatter():
    pass
