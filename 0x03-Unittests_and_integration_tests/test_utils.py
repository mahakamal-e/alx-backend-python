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
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        data = get_json(test_url)
        self.assertEqual(data, test_payload)
        mock_get.assert_called_once_with(test_url)

        mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    """Test the memoize decorator."""

    def test_memoize(self):
        """Test that the memoize decorator caches results correctly."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Patch the `a_method` of `TestClass`
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()

            # Access `a_property` twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Check that the result is as expected
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure `a_method` was called only once
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
