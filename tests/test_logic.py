import json
from gendiff.logic import decoded, is_dict, compared, format_stylish

import pytest
import yaml


@pytest.fixture
def json1():
    return '/home/siderai/gendiff/tests/fixtures/file1.json'

@pytest.fixture
def json2():
    return '/home/siderai/gendiff/tests/fixtures/file2.json'

@pytest.fixture
def jsoncomplex1():
    return '/home/siderai/gendiff/tests/fixtures/complex1.json'

@pytest.fixture
def jsoncomplex2():
    return '/home/siderai/gendiff/tests/fixtures/complex2.json'

@pytest.fixture
def yaml1():
    return '/home/siderai/gendiff/tests/fixtures/file1.yaml'

@pytest.fixture
def yaml2():
    return '/home/siderai/gendiff/tests/fixtures/file2.yaml'

@pytest.fixture
def yamlcomplex1():
    return '/home/siderai/gendiff/tests/fixtures/complex1.yaml'
@pytest.fixture
def yamlcomplex2():
    return '/home/siderai/gendiff/tests/fixtures/complex2.yaml'

paths = (json1, json2, jsoncomplex1, jsoncomplex2, yaml1, yaml2, yamlcomplex1, yamlcomplex2)

def test_decoded(json1, json2, jsoncomplex1, jsoncomplex2, yaml1, yaml2, yamlcomplex1, yamlcomplex2):
    # jsons
    assert decoded(json1) == json.load(open(json1))
    assert decoded(json2) == json.load(open(json2))
    assert decoded(jsoncomplex1) == json.load(open(jsoncomplex1))
    assert decoded(jsoncomplex2) == json.load(open(jsoncomplex2))
    # yamls
    assert decoded(yaml1) == yaml.load(open(yaml1), Loader=yaml.Loader)
    assert decoded(yaml2) == yaml.load(open(yaml2), Loader=yaml.Loader)
    assert decoded(yamlcomplex1) == yaml.load(open(yamlcomplex1), Loader=yaml.Loader)
    assert decoded(yamlcomplex2) == yaml.load(open(yamlcomplex2), Loader=yaml.Loader)

def test_is_dict():
    assert is_dict(dict()) == True
    assert is_dict(list()) == False
    assert is_dict(set()) == False



simple_view = {
        ('+', 'timeout'): 20,
        ('+', 'verbose'): True,
        ('-', 'follow'): False,
        ('-', 'proxy'): '123.234.53.22',
        ('-', 'timeout'): 50,
        ('=', 'host'): 'hexlet.io'
        }

def test_compared_with_simple(json1, json2, yaml1, yaml2):
    jsoncomplex1 = json.load(open(json1))
    jsoncomplex2 = json.load(open(json2))
    assert compared(jsoncomplex1, jsoncomplex2) == simple_view
    
    yaml1 = yaml.load(open(yaml1), Loader=yaml.Loader)
    yaml2 = yaml.load(open(yaml2), Loader=yaml.Loader)
    assert compared(yaml1, yaml2) == simple_view


def test_compared_with_complex(jsoncomplex1, jsoncomplex2, yamlcomplex1, yamlcomplex2):
    pass




    formatted_str = '{\n  - follow: false\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}'