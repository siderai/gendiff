import json

import yaml


def decoded(filepath: str) -> dict:
    """ Yaml/json parser. """

    if filepath.endswith('.json'):
        return json.load(open(filepath))
    else:
        if filepath.endswith('.yaml') or filepath.endswith('.yml'):
            return yaml.load(open(filepath, mode='r'), Loader=yaml.Loader)


def is_dict(obj) -> bool:
    if isinstance(obj, dict):
        return True
    return False


def compared(file1: dict, file2: dict) -> dict:
    """
    Compare two dicts and create image of their difference.
    In addition to original keys, there are signs that store diff of dicts:
        1. '-': the item is only in 1st file (and its value is not a dict);
        2. '+': the item is only in 2nd file (and its value is not a dict);
        3. '=': items are equal;
        4. ' ': keys are equal, but values are dicts
                                and should be compared recursively.
    """
    if is_dict(file1) and is_dict(file2):
        # compare keys of the dicts
        common_keys = file1.keys() & file2.keys()
        first_only = file1.keys() - file2.keys()
        second_only = file2.keys() - file1.keys()
    # create image of difference
    diff = {}
    # compare common keys
    for key in common_keys:
        value_in_first = file1[key]
        value_in_second = file2[key]
        if value_in_first == value_in_second:
            diff[('=', key)] = value_in_first
        elif is_dict(value_in_first) and is_dict(value_in_second):
            diff[(' ', key)] = compared(value_in_first, value_in_second)
        else:
            diff[('-', key)] = value_in_first
            diff[('+', key)] = value_in_second
    # mark deleted keys
    for key in first_only:
        diff[('-', key)] = file1[key]
    # mark added keys
    for key in second_only:
        diff[('+', key)] = file2[key]
    return diff


def format_stylish(diff: dict) -> str:
    """ Prepare diff for output as json-like string. """
    blank = list()
    for sign, key in diff:
        if sign == '=':
            blank.append(f'    {key}: {diff[(sign, key)]}')
        elif sign == ' ':
            blank.append(f'    {key}: {format_stylish(diff[(sign, key)])}')
        else:
            blank.append(f'  {sign} {key}: {diff[(sign, key)]}')

    blank = sorted(blank, key=lambda x: x[4])  # index of key's first non-empty char
    blank.insert(0, '{')
    blank.append('}')
    result = '\n'.join(blank)
    print(result)


def format_plain(diff: dict) -> str:
    ''' Second output formatter: human-friendly text'''
    blank = list()
    name = list()
    complex_value = '[complex value]'
    for sign, key in diff:

        if sign == '-':
            # check if key was updated or just removed
            try:
                updated_value = diff[('+', key)]  # this line raises exception if key was removed
                if is_dict(updated_value):
                    output_update = complex_value
                else:
                    output_update = json.dumps(updated_value)  # translate data from Python back to json

                initial_value = diff[('-', key)]
                output_initial_value = json.dumps(initial_value)

                # accumulate name
                name.append(key)
                output_name = '.'.join(name)
                # Gen diff output
                blank.append(f'Property \'{output_name}\' was updated. ' 
                            f'From {output_initial_value} to {output_update}')
            except KeyError:  # key removed scenario
                # accumulate name
                name.append(key)
                output_name = '.'.join(name)
                # Gen output
                blank.append(f'Property \'{output_name}\' was removed') 
            name = list()

        if sign == '+':
            try: 
                _ = diff[('-', key)] # added in previous step
                pass
            except KeyError: # means key was added
                value = diff[('+', key)]
                if is_dict(value):
                    output_value = complex_value
                else:
                    output_value = json.dumps(value)
                name.append(key)
                output_name = '.'.join(name)
                blank.append(f'Property \'{output_name}\' was added with value: {output_value}')
            name = list()

    result = '\n'.join(sorted(blank, key=lambda x: x[10]))
    return result




def format_json(diff: dict) -> str:
    pass


