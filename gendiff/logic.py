import json

import yaml


def decoded(filepath: str) -> dict:
    """ Yaml/json parser. """
    if filepath.endswith('.json'):
        return json.load(open(filepath))
    else:
        if filepath.endswith(('.yaml', '.yml')):
            return yaml.load(open(filepath, mode='r'), Loader=yaml.Loader)


def is_dict(obj) -> bool:
    if isinstance(obj, dict):
        return True
    return False


def compared(file1: dict, file2: dict) -> dict:
    """
    Compare two dicts and create image of their difference.
    In addition to original keys, there are signs that store diff of dicts:
        1. '-': the item is only in 1st file;
        2. '+': the item is only in 2nd file;
        3. '=': items are equal;
        4. ' ': only keys are equal, but values are dicts
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


def stylish_formatted_equals(node, depth=1) -> str:
    """Convert subdict to formatted string (for format_stylish())"""
    if not is_dict(node):
        return json.dumps(node)
    blank = list()
    indenter = ' ' * 4 * (depth - 1)
    for key in node:
        if is_dict(node[key]):
            next_lvl = depth + 1
            value = stylish_formatted_equals(node[key], next_lvl)
            line = f'    {key}: {value}'
        else:
            if isinstance(node[key]):
                value = json.dumps(node[key])
            else:
                value = node[key]
            line = f'    {key}: {value}'
        blank.append(indenter + line)
    blank.insert(0, '{')
    blank.append(indenter + '}')
    result = '\n'.join(blank)
    return result


def format_stylish(diff: dict, depth=1) -> str:
    """ Convert diff to json-like string. """
    blank = list()
    indenter = ' ' * 4 * (depth - 1)
    for sign, key in diff:
        value_view = diff[(sign, key)]
        if sign == ' ':
            next_lvl = depth + 1
            value = format_stylish(value_view, next_lvl)
            line = f'    {key}: {value}'
        # combine if and else later
        else:
            if is_dict(value_view):
                next_lvl = depth + 1
                value = stylish_formatted_equals(value_view, next_lvl)
            else:
                if isinstance(value_view, bool):
                    value = json.dumps(value_view)
                else:
                    value = value_view

            if sign == '=':
                line = f'    {key}: {value}'
            else:
                line = f'  {sign} {key}: {value}'

        blank.append(indenter + line)

    # names start from index 4, sort them in alphabet order:
    names_begin_with = (5 * depth) - 1
    blank = sorted(blank, key=lambda x: x[names_begin_with])
    blank.insert(0, '{')
    blank.append(indenter + '}')
    result = '\n'.join(blank)
    return result


def format_plain(diff: dict) -> str:
    '''Human-friendly output formatter'''
    blank = list()
    name = list()
    complex_value = '[complex value]'
    for sign, key in diff:
        if sign == '-':
            # check if key was updated or just removed
            try:
                # next line raises exception if key was removed
                updated_value = diff[('+', key)]
                if is_dict(updated_value):
                    output_update = complex_value
                else:
                    # translate data from Python back to json
                    output_update = json.dumps(updated_value)

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
            continue

        if sign == '+':
            try:
                _ = diff[('-', key)]
                continue  # avoid duplicates, info is added at previous step
            except KeyError:  # means key was added, not updated
                value = diff[('+', key)]
                if is_dict(value):
                    output_value = complex_value
                else:
                    output_value = json.dumps(value)
                name.append(key)
                output_name = '.'.join(name)
                blank.append(
                    f'Property \'{output_name}\' was added '
                    f'with value: {output_value}')
            name = list()
            continue

    result = '\n'.join(sorted(blank, key=lambda x: x[10]))
    return result


def format_json(diff: dict) -> str:
    """Return diff as json"""
    blank = dict()
    for sign, key in diff:
        keyword = f'{sign} {key}'
        equal_keyword = f'  {key}'
        value = diff[(sign, key)]
        if sign == '=':
            blank[equal_keyword] = value
        elif sign == ' ':
            blank[keyword] = format_stylish(value)
        else:
            blank[keyword] = value
    result = json.dumps(blank)
    return result
