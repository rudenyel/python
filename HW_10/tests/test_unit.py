import os
import json
from dataclasses import dataclass

import unittest
from things_to_test_hw import search_in_file, add_from_json, Storage


class TestSearch(unittest.TestCase):
    __temp_file = 'patterns'

    @classmethod
    def setUpClass(cls):
        lines = ('first_line\n', 'second_line\n', 'third_line\n')
        with open(cls.__temp_file, 'w') as file:
            file.writelines(lines)

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), cls.__temp_file))

    def test1_positive(self):
        result = search_in_file(self.__temp_file, 'first')
        self.assertEqual(['first_line\n'], result)

    def test2_positive(self):
        result = search_in_file(self.__temp_file, 'last')
        self.assertEqual([], result)

    def test3_negative(self):
        with self.assertRaises(FileNotFoundError):
            result = search_in_file('', 'first')
            self.assertEqual([], result)


class TestAdd(unittest.TestCase):
    __temp_file = 'dict'

    @classmethod
    def setUpClass(cls):
        data = {'a': 3, 'b': 4, 'c': 5}
        with open(cls.__temp_file, 'w') as file:
            json.dump(data, file)

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), cls.__temp_file))

    def test1_positive(self):
        result = add_from_json(self.__temp_file, 'a')
        self.assertEqual(3, result)

    def test2_positive(self):
        result = add_from_json(self.__temp_file, ())
        self.assertEqual(0, result)

    def test3_positive(self):
        result = add_from_json(self.__temp_file, ('a', 'b'))
        self.assertEqual(7, result)

    def test4_negative(self):
        with self.assertRaises(KeyError):
            result = add_from_json(self.__temp_file, ('a', 'b', 'z'))
            self.assertEqual([], result)

    def test5_negative(self):
        with self.assertRaises(FileNotFoundError):
            result = add_from_json('', 'a')
            self.assertEqual([], result)


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Line:
    start: Point
    end: Point


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.__storage = Storage()
        self.__storage.add_table('points', Point)
        self.__storage.add_table('lines', Line)

    def test_positive1(self):
        result = self.__storage.get_from_table('points')
        self.assertEqual([], result)

    def test_positive2(self):
        self.__storage.add_to_table('points', Point(0, 0), Point(1, 1))
        result = self.__storage.get_from_table('points')
        self.assertEqual([Point(0, 0), Point(1, 1)], result)

    def test_positive3(self):
        self.__storage.add_to_table('lines', Line(Point(0, 0), Point(1, 1)))
        result = self.__storage.get_from_table('lines')
        self.assertEqual([Line(Point(0, 0), Point(1, 1))], result)

    def test_negative4(self):
        with self.assertRaises(ValueError):
            self.__storage.get_from_table('polygons')

    def test_negative5(self):
        with self.assertRaises(ValueError):
            self.__storage.add_table('lines', Line)

    def test_negative6(self):
        with self.assertRaises(ValueError):
            self.__storage.add_to_table('positions', Point(0, 0), Point(1, 1))

    def test_negative7(self):
        with self.assertRaises(ValueError):
            self.__storage.add_to_table('points', 0, 0, 1, 1)
