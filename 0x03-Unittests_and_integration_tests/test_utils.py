#!/usr/bin/env python3
"""Define a unit test Module"""
import unittest
from parameterized import parameterized
from utils import *
from unittest.mock import Mock, patch


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
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Define the TestGetJson(unittest.TestCase) class """
    @patch('requests.get')
    def test_get_json(self, mock_get):
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            data = get_json(test_url)

            mock_get.assert_called_once_with(test_url)

            self.assertEqual(data, test_payload)

            mock_get.reset_mock()


if __name__ == '__main__':
    unittest.main()
