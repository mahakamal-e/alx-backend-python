#!/usr/bin/env python3
"""Test for GithubOrgClient"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""

        expected_response = {
            "repos_url": "https://api.github.com/orgs/{org}/repos"
        }
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)

        result = client.org

        expected_url = client.ORG_URL.format(org=org_name)
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, expected_response)

if __name__ == '__main__':
    unittest.main()
