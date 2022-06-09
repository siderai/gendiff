import json
from typing import Any

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
    In addition to original keys, there are markers that store
    difference of a certain key in two dicts.
        Markers info:
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

    else:
        raise Exception("Json/yaml parsing error!")

    diff = {}  # diff is an image of difference to store compared
    
    # compare common keys
    for key in common_keys:
        value_in_first = file1[key]
        value_in_second = file2[key]
        
        # equal items
        if value_in_first == value_in_second:
            diff[("=", key)] = value_in_first
        
        # nested values need recursive comparison
        elif is_dict(value_in_first) and is_dict(value_in_second):
            diff[(" ", key)] = compared(value_in_first, value_in_second)
        
        # value was updated
        else:
            diff[("-", key)] = value_in_first
            diff[("+", key)] = value_in_second
    
    # deleted items
    for key in first_only:
        diff[("-", key)] = file1[key]
    
    # added items
    for key in second_only:
        diff[("+", key)] = file2[key]
    
    return diff


def is_dict(obj: Any) -> bool:
    return isinstance(obj, dict)
