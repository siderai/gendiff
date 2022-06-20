import json
from collections import namedtuple
from typing import Any, Mapping, NamedTuple, Union

import yaml


def decoded(filepath: str) -> Union[dict, None]:
    """Yaml/json parser."""
    try:
        if filepath.endswith(".json"):
            return json.load(open(filepath))
        elif filepath.endswith((".yaml", ".yml")):
            return yaml.load(open(filepath, mode="r"), Loader=yaml.Loader)
    except (json.JSONDecodeError, yaml.YAMLError):
        raise ValueError("Failed to deserialize json/yaml file!")


ComparedKey = namedtuple("ComparedKey", ["mark", "key"])  # compared data template


def compared(file1: dict, file2: dict) -> Union[Mapping[NamedTuple, Any], None]:
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

    diff = {}  # init an image of difference

    # compare common keys
    for key in common_keys:
        value_in_first = file1[key]
        value_in_second = file2[key]

        # equal items
        if value_in_first == value_in_second:
            diff[ComparedKey("=", key)] = value_in_first

        # nested values need recursive comparison
        elif is_dict(value_in_first) and is_dict(value_in_second):
            diff[ComparedKey(" ", key)] = compared(value_in_first, value_in_second)

        # value was updated
        else:
            diff[ComparedKey("-", key)] = value_in_first
            diff[ComparedKey("+", key)] = value_in_second

    # deleted items
    for key in first_only:
        diff[ComparedKey("-", key)] = file1[key]

    # added items
    for key in second_only:
        diff[ComparedKey("+", key)] = file2[key]

    return diff


def is_dict(obj: Any) -> bool:
    return isinstance(obj, dict)
