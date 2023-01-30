import os
import json
from dataclasses import dataclass

import pytest
from things_to_test_hw import search_in_file, add_from_json, Storage


@pytest.fixture(scope='module')
def data_for_search():
    return 'first_line\n', 'second_line\n', 'third_line\n'


@pytest.fixture(scope='module')
def text_filename():
    return 'patterns.tmp'


@pytest.fixture(scope='module')
def file_for_search(text_filename, data_for_search):
    with open(text_filename, 'w') as file:
        file.writelines(data_for_search)
    yield text_filename
    os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), text_filename))


@pytest.mark.parametrize(
    'pattern, expected',
    (
            ('first', ['first_line\n']),
            ('last', []),
    ),
)
def test_search_positive1(file_for_search, pattern, expected):
    assert search_in_file(file_for_search, pattern) == expected


def test_search_negative2():
    with pytest.raises(FileNotFoundError):
        assert search_in_file('', 'first') == []


@pytest.fixture(scope='module')
def data_for_add():
    return {'a': 3, 'b': 4, 'c': 5}


@pytest.fixture(scope='module')
def json_filename():
    return 'dict.tmp'


@pytest.fixture(scope='module')
def file_for_add(json_filename, data_for_add):
    with open(json_filename, 'w') as file:
        json.dump(data_for_add, file)
    yield json_filename
    os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), json_filename))


@pytest.mark.parametrize(
    'keys, expected',
    (
            ('a', 3),
            ([], 0),
            (['a', 'b'], 7),
    ),
)
def test_add_positive1(file_for_add, keys, expected):
    assert add_from_json(file_for_add, keys) == expected


def test_add_negative2(file_for_add):
    with pytest.raises(KeyError):
        assert add_from_json(file_for_add, ('a', 'b', 'z')) == []


def test_add_negative3():
    with pytest.raises(FileNotFoundError):
        assert add_from_json('', ('a', 'b')) == []


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Line:
    start: Point
    end: Point


@pytest.fixture(scope='function')
def storage():
    storage = Storage()
    storage.add_table('points', Point)
    storage.add_table('lines', Line)
    return storage


def test_storage_positive1(storage):
    assert storage.get_from_table('points') == []


@pytest.mark.parametrize(
    'table_name, items, expected',
    (
            ('points', (Point(0, 0), Point(1, 1)), [Point(0, 0), Point(1, 1)]),
            ('lines', (Line(Point(0, 0), Point(1, 1)), ), [Line(Point(0, 0), Point(1, 1))]),
    ),
)
def test_storage_positive2(storage, table_name, items, expected):
    storage.add_to_table(table_name, *items)
    assert storage.get_from_table(table_name) == expected


def test_storage_negative3(storage):
    with pytest.raises(ValueError):
        assert storage.get_from_table('polygons') == []


def test_storage_negative4(storage):
    with pytest.raises(ValueError):
        assert storage.add_table('lines', Line) == []


def test_storage_negative5(storage):
    with pytest.raises(ValueError):
        assert storage.add_to_table('positions', Point(0, 0), Point(1, 1)) == []


def test_storage_negative6(storage):
    with pytest.raises(ValueError):
        assert storage.add_to_table('points', 0, 0, 1, 1) == []
