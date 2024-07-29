#!/usr/bin/env python3
"""Parameterize a unit test Module"""
import unittest
from parameterized import parameterized
from utils import *


class TestAccessNestedMap(unittest.TestCase):
    """ Calss to test methond access_nested_map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])

    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, expected):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

if __name__ == '__main__':
    unittest.main()
