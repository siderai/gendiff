import json
import copy
from typing import List, Any

import yaml


def decoded(filepath: str) -> dict:
    """Yaml/json parser."""
    if filepath.endswith(".json"):
        return json.load(open(filepath))
    elif filepath.endswith((".yaml", ".yml")):
        return yaml.load(open(filepath, mode="r"), Loader=yaml.Loader)
    else:
        raise Exception("Json/yaml parsing error!")


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
    else:
        raise Exception("Json/yaml parsing error!")
    diff = {}
    # compare common keys
    for key in common_keys:
        value_in_first = file1[key]
        value_in_second = file2[key]
        # mark equal items
        if value_in_first == value_in_second:
            diff[("=", key)] = value_in_first
        # mark keys that need recursive comparison of values
        elif is_dict(value_in_first) and is_dict(value_in_second):
            diff[(" ", key)] = compared(value_in_first, value_in_second)
        else:
            # mark initial and updated value of a common key
            diff[("-", key)] = value_in_first
            diff[("+", key)] = value_in_second
    # mark deleted keys
    for key in first_only:
        diff[("-", key)] = file1[key]
    # mark added keys
    for key in second_only:
        diff[("+", key)] = file2[key]
    return diff


def format_json(diff: dict) -> str:
    """Return diff as json"""
    blank = dict()
    for sign, key in diff:
        keyword = f"{sign} {key}"
        equal_keyword = f"  {key}"
        value = diff[(sign, key)]
        if sign == "=":
            blank[equal_keyword] = value
        elif sign == " ":
            blank[keyword] = format_stylish(value)
        else:
            blank[keyword] = value
    result = json.dumps(blank)
    return result


def format_plain(diff: dict) -> str:
    """Human-friendly output formatter"""
    blank: List[str] = list()
    ancestry: List[str] = list()
    walk_plain(diff, ancestry, blank)
    return "\n".join(sorted(blank, key=lambda x: x[10:]))


def format_stylish(diff: dict, depth=1) -> str:
    """Convert diff to json-like string"""
    blank: List[str] = list()
    indenter: str = " " * 4 * (depth - 1)
    walk_stylish(diff, blank, indenter, depth)
    return _stylish_sorted_str(blank, depth, indenter)


def walk_stylish(diff: dict, blank: list, indenter: str, depth: int) -> None:
    '''Tree traversal to format nodes for stylish output'''
    for sign, key in diff:
        value_view = diff[(sign, key)]
        if sign == " ":
            next_lvl = depth + 1
            # sign ' ' means we need to run recursion to get value
            value = format_stylish(value_view, next_lvl)
            line = f"    {key}: {value}"
        else:
            value = _parse_value(value_view, depth)
        # generate whole line
        if sign == "=":
            # key didn't change
            line = f"    {key}: {value}"
            blank.append(indenter + line)
        elif sign == "-":
            line = f"  {sign} {key}: {value}"
            try:
                # key updated
                comparison_value = diff[("+", key)]
                comparison_value = _parse_value(comparison_value, depth)
                line2 = f"  + {key}: {comparison_value}"
                blank.append(indenter + line + "\n" + indenter + line2)
            except KeyError:
                # key removed
                blank.append(indenter + line)
        else:
            try:
                comparison_value = diff[("-", key)]
                continue
            except KeyError:
                # key added
                line = f"  {sign} {key}: {value}"
                blank.append(indenter + line)


def _stylish_sorted_str(blank: List[str], depth: int, indenter: str) -> str:
    """Data collector that finalizes stylish formatter.
    Contecatenates diff pieces from blank, then adds indents for readability
    """
    sorter = 4 * depth
    blank = sorted(blank, key=lambda x: x[sorter:])
    blank.insert(0, "{")
    blank.append(indenter + "}")
    result = "\n".join(blank)
    return result


def walk_plain(node, ancestry: list, blank: list) -> None:
    '''Tree traversal to format nodes for plaintext output'''
    for sign, key in node:
        if sign == "-":
            # check if key was updated or just removed
            try:
                # if key was updated there is new value for it
                updated_value_view = node[("+", key)]
            except KeyError:  # if no new value, key was removed
                # accumulate name
                name_removed = _get_node_name(key, ancestry)
                # Gen output
                blank.append(f"Property '{name_removed}' was removed")
            else:
                # accumulate name and new value
                name_updated = _get_node_name(key, ancestry)
                updated_value = _plain_value_formatter(updated_value_view)

                # get and translate initial value
                initial_value_view = node[("-", key)]
                initial_value = _plain_value_formatter(initial_value_view)
                # gen output line
                blank.append(
                    f"Property '{name_updated}' was updated. "
                    f"From {initial_value} to {updated_value}"
                )

        elif sign == "+":
            try:
                _ = node[("-", key)]
                continue  # avoid duplicates, diff is added at previous step
            except KeyError:  # means key was added
                # accumulate name
                name_added = _get_node_name(key, ancestry)
                added_value_view = node[("+", key)]
                added_value = _plain_value_formatter(added_value_view)
                blank.append(
                    f"Property '{name_added}' was added "
                    f"with value: {added_value}"
                )

        elif sign == " ":
            next_node = node[(" ", key)]
            new_ancestry = copy.copy(ancestry)
            new_ancestry.append(key)
            walk_plain(next_node, new_ancestry, blank)


def _get_value_from(value_view):
    """Type dependent parser for flat values.
    As json and yaml use different keywords for bool (false, true)
    and None (null), we should put them into final diff view"""
    if isinstance(value_view, bool) or value_view is None:
        value = json.dumps(value_view)
    else:
        value = value_view
    return value


def _stylish_formatted_equals(node, depth=1) -> str:
    """Parser for nodes that have no diff sign from after compared().
    Keys are equal, but keys need recursive comparison.
    Produces formatted string (to be used part of stylish formatter)"""
    children = list()
    indenter = " " * 4 * (depth - 1)
    for key in node:
        item = node[key]
        if is_dict(item):
            next_lvl = depth + 1
            value = _stylish_formatted_equals(item, next_lvl)
            line = f"    {key}: {value}"
        else:
            value = _get_value_from(item)
            line = f"    {key}: {value}"
        children.append(indenter + line)
    result = _stylish_sorted_str(children, depth, indenter)
    return result


def _parse_value(value_view, depth=1):
    """Generic value parser and formatter"""
    if is_dict(value_view):
        # parse nested value
        next_lvl = depth + 1
        value = _stylish_formatted_equals(value_view, next_lvl)
    else:
        # parse flat value
        value = _get_value_from(value_view)
    return value


def _get_node_name(key, ancestry):
    node_ancestry = copy.copy(ancestry)
    node_ancestry.append(key)
    name = ".".join(node_ancestry)
    return name


def _plain_value_formatter(value_view):
    if is_dict(value_view):
        value = "[complex value]"
    elif isinstance(value_view, str):
        value = "'" + value_view + "'"
    else:
        # translate plain updated value back to json
        value = _get_value_from(value_view)
    return value


def is_dict(obj: Any) -> bool:
    return isinstance(obj, dict)
