from gendiff import generate_diff


filepath1 = 'tests/fixtures/complex1.json'
filepath2 = 'tests/fixtures/complex2.json'

simple1 = 'tests/fixtures/file1.json'
simple2 = 'tests/fixtures/file2.json'


def test_json():
    output = generate_diff(filepath1, filepath2, format_='json')
    assert isinstance(output, str) is True


def test_stylish():
    with open('tests/fixtures/stylish.txt') as stylish:
        result = stylish.read()
        assert generate_diff(filepath1, filepath2, format_='stylish') == result


def test_plain():
    with open('tests/fixtures/plain.txt') as plain:
        result = plain.read()
        assert generate_diff(filepath1, filepath2, format_='plain') == result
