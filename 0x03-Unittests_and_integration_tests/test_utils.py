#!/usr/bin/env python3
"""Define test utils Module """
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """Class to test method access_nested_map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map method"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map method with KeyError exception"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Define the TestGetJson(unittest.TestCase) class """
    @parameterized.expand([
        ("http://example.com", {"payload", True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, get_mock):
        """Test get_json with two different urls"""
        get_mock.json.return_value = test_payload
        get_mock.return_value = get_mock

        self.assertEqual(get_json(test_url), test_payload)
        get_mock.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Class to test memoize decorator"""
    def test_memoize(self):
        """Test memoize decorator"""
        class TestClass:
            """Implement test class"""
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as a_mock:
            a_mock.return_value = lambda: 42

            my_test = TestClass()
            self.assertEqual(my_test.a_property(), 42)
            self.assertEqual(my_test.a_property(), 42)

            a_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
