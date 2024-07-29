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
        """Tesr access_nested_map method """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """" Test access_nested_map method with key error exception"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Define the TestGetJson(unittest.TestCase) class """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, mock_get, test_url, test_payload):
        """Test get_json function to ensure it returns the expected result."""
        # Configure the mock to return the test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function with the test_url
        data = get_json(test_url)

        # Assert that the mocked get method was called exactly once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert that the output of get_json is equal to test_payload
        self.assertEqual(data, test_payload)

        # Reset the mock for the next iteration
        mock_get.reset_mock()


if __name__ == '__main__':
    unittest.main()
