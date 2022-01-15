from logic import decoded, compared, format_stylish
import json


import pytest
import yaml


@pytest.fixture
def jsonpath1():
    return '/home/siderai/gendiff/tests/fixtures/file1.json'

@pytest.fixture
def jsonpath2():
    return '/home/siderai/gendiff/tests/fixtures/file2.json'

@pytest.fixture
def json1():
    return '/home/siderai/gendiff/tests/fixtures/complex1.json'

@pytest.fixture
def json2():
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


def test_decoded(jsonpath1, jsonpath2, json1, json2, yaml1, yaml2, yamlcomplex1, yamlcomplex2):
    # jsons
    assert decoded(jsonpath1) == json.load(open(jsonpath1))
    assert decoded(jsonpath2) == json.load(open(jsonpath2))
    assert decoded(json1) == json.load(open(json1))
    assert decoded(json2) == json.load(open(json2))
    # yamls
    assert decoded(yaml1) == yaml.load(open(yaml1), Loader=yaml.Loader)
    assert decoded(yaml2) == yaml.load(open(yaml2), Loader=yaml.Loader)
    assert decoded(yamlcomplex1) == yaml.load(open(yamlcomplex1), Loader=yaml.Loader)
    assert decoded(yamlcomplex2) == yaml.load(open(yamlcomplex2), Loader=yaml.Loader)

def test_compared(jsonpath1, jsonpath2, json1, json2, yaml1, yaml2, yamlcomplex1, yamlcomplex2):
    json1 = json.load(open(jsonpath1))
    json2 = json.load(open(jsonpath2))
    assert compared(json1, json2) == '{\
      - follow: false\
        host: hexlet.io\
      - proxy: 123.234.53.22\
      - timeout: 50\
      + timeout: 20\
      + verbose: true\
    }'