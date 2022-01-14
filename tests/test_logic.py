import json
from logic import decoded, compared, format_stylish

import pytest

@pytest.fixture
def filepath1():
    return '/home/siderai/gendiff/tests/fixtures/file1.json'

@pytest.fixture
def filepath2():
    return '/home/siderai/gendiff/tests/fixtures/file2.json'

@pytest.fixture
def path1():
    return '/home/siderai/gendiff/tests/fixtures/complex1.json'

@pytest.fixture
def path2():
    return '/home/siderai/gendiff/tests/fixtures/complex2.json'


def test_decoded(filepath1, filepath2, path1):
    assert decoded(filepath1) == json.load(open(filepath1))
    assert decoded(filepath2) == json.load(open(filepath2))
    assert decoded(path1) == json.load(open(path1))
    assert decoded(path2) == json.load(open(path2))