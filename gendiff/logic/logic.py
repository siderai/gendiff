def compare(file1, file2):
    """
    Compare two dicts and create their difference form.
    The beginnings of original keys are changed to store difference:
        1. '- ': item is only in 1st file (and value is not a dict);
        2. '+ ': item is only in 2nd file (and value is not a dict);
        3. '= ': items are equal;
        4. '  ': keys are equal, but values are dicts
                                 and should be compared recursively.
    :param file1: dict
    :param file2: dict
    :return: result: dict
    """
    # check if input is correct
    if isinstance(file1, dict) and isinstance(file2, dict):
        # compare keys of the dicts
        common_keys = file1.keys() & file2.keys()
        first_only = file1.keys() - file2.keys()
        second_only = file2.keys() - file1.keys()
    else:
        return
    # create inner representation of difference
    result = {}
    for key in common_keys:
        if file1[key] == file2[key]:
            result[f"= {key}"] = file1[key]
        else:
            if isinstance(file1[key], dict) and isinstance(file2[key], dict):
                result[f"  {key}"] = compare(file1[key], file2[key])
            else:
                result[f"- {key}"] = file1[key]
                result[f"+ {key}"] = file2[key]
    for key in first_only:
        result[f"- {key}"] = file1[key]
    for key in second_only:
        result[f"+ {key}"] = file2[key]
    return result


fixt1 = {
  "common": {
    "setting1": "Value 1",
    "setting2": 200,
    "setting3": True,
    "setting6": {
      "key": "value",
      "doge": {
        "wow": ""
      }
    }
  },
  "group1": {
    "baz": "bas",
    "foo": "bar",
    "nest": {
      "key": "value"
    }
  },
  "group2": {
    "abc": 12345,
    "deep": {
      "id": 45
    }
  }
}

fixt2 = {
  "common": {
    "follow": False,
    "setting1": "Value 1",
    "setting3": None,
    "setting4": "blah blah",
    "setting5": {
      "key5": "value5"
    },
    "setting6": {
      "key": "value",
      "ops": "vops",
      "doge": {
        "wow": "so much"
      }
    }
  },
  "group1": {
    "foo": "bar",
    "baz": "bars",
    "nest": "str"
  },
  "group3": {
    "deep": {
      "id": {
        "number": 45
      }
    },
    "fee": 100500
  }
}
print(isinstance(s, dict))
print(isinstance(d, dict))
print(compare(s, d))
