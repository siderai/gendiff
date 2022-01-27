import json  # noqa E902
from gendiff import decoded, is_dict, compared, format_stylish
from gendiff import format_plain, format_json

import pytest
import yaml


@pytest.fixture
def json1():
    return 'tests/fixtures/file1.json'


@pytest.fixture
def json2():
    return 'tests/fixtures/file2.json'


@pytest.fixture
def jsoncomplex1():
    return 'tests/fixtures/complex1.json'


@pytest.fixture
def jsoncomplex2():
    return 'tests/fixtures/complex2.json'


@pytest.fixture
def yaml1():
    return 'tests/fixtures/file1.yaml'


@pytest.fixture
def yaml2():
    return 'tests/fixtures/file2.yaml'


@pytest.fixture
def yamlcomplex1():
    return 'tests/fixtures/complex1.yaml'


@pytest.fixture
def yamlcomplex2():
    return 'tests/fixtures/complex2.yaml'


@pytest.fixture
def json_paths(json1, json2, jsoncomplex1, jsoncomplex2):
    return [json1, json2, jsoncomplex1, jsoncomplex2]


@pytest.fixture
def yaml_paths(yaml1, yaml2, yamlcomplex1, yamlcomplex2):
    return [yaml1, yaml2, yamlcomplex1, yamlcomplex2]


def test_decoded_decodes(json_paths, yaml_paths):
    for path in json_paths:
        assert decoded(path) == json.load(open(path))
    for path in yaml_paths:
        assert decoded(path) == yaml.load(open(path), Loader=yaml.Loader)


def test_decoded_uses_correct_parser(json1, yaml1):
    assert decoded(json1) == decoded(yaml1)


def test_is_dict():
    assert is_dict(dict()) is True
    assert is_dict(list()) is False
    assert is_dict(set()) is False


# compared
def test_compared_with_simple(json1, json2, yaml1, yaml2):
    json_simple_view = {
        ('=', 'host'): "hexlet.io",
        ('-', 'timeout'): 50,
        ('+', 'timeout'): 20,
        ('-', 'proxy'): "123.234.53.22",
        ('-', 'follow'): False,
        ('+', 'verbose'): True
    }
    yaml_simple_view = {
        ('=', 'host'): 'hexlet.io',
        ('-', 'timeout'): 50,
        ('+', 'timeout'): 20,
        ('-', 'proxy'): '123.234.53.22',
        ('-', 'follow'): False,
        ('+', 'verbose'): True
    }
    assert compared(decoded(json1), decoded(json2)) == json_simple_view
    assert compared(decoded(yaml1), decoded(yaml2)) == yaml_simple_view


def test_compared_with_complex(jsoncomplex1, jsoncomplex2):
    #  diff_complex_view = {}
    pass


#  stylish formatter
def test_format_stylish_simple(json1, json2, yaml1, yaml2):
    simple_stylish_view = '{\n  - follow: false\n    host: hexlet.io\n'\
                          '  - proxy: 123.234.53.22\n  - timeout: 50\n'\
                          '  + timeout: 20\n  + verbose: true\n}'
    assert format_stylish(compared(
        decoded(json1),
        decoded(json2))) == simple_stylish_view


def test_format_stylish_complex(jsoncomplex1, jsoncomplex2):
    with open('tests/fixtures/stylish.txt') as f:
        result = f.read()
        assert format_stylish(compared(decoded(jsoncomplex1),
               decoded(jsoncomplex2))) == result


#  plain formatter
def test_format_plain_simple(json1, json2):
    assert format_plain(compared(
        decoded(json1), decoded(json2))) == 'Property \'follow\''\
        ' was removed\nProperty \'proxy\' was removed\nProperty \'timeout\''\
        ' was updated. From'\
        ' 50 to 20\nProperty \'verbose\' was added with value: true'


def test_format_plain_complex(jsoncomplex1, jsoncomplex2):
    with open('tests/fixtures/plain.txt', 'r') as f:
        result = f.read()
        assert format_plain(compared(
            decoded(jsoncomplex1),
            decoded(jsoncomplex2))) == result


#  json formatter
def test_format_json__with_simple(json1, json2):
    res = format_json(compared(decoded(json1), decoded(json2)))
    assert isinstance(res, str) is True
