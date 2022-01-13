from gendiff.scripts.logic import decoded, compared, str_formatter

import pytest


@pytest.fixture
def simple_json1():
    return {
    "host": "hexlet.io",
    "timeout": 50,
    "proxy": "123.234.53.22",
    "follow": false
    }


@pytest.fixture
def simple_json2():
    return {
    "timeout": 20,
    "verbose": true,
    "host": "hexlet.io"
    }


def test_decoded:
    assert decoded(simple_json1) == json.load(simple_json1)

