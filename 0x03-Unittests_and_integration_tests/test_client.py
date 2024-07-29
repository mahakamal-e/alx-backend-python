#!/usr/bin/env python3
"""Defines TestGithubOrgClient class"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Implement TestGithubOrgClient class"""
    @parameterized.expand(['google', 'abc'])
    @patch('client.get_json')
    def test_org(self, org_name, get_mock):
        """Test org method"""
        get_mock.return_value = lambda: {"org_name": org_name}

        github_client = GithubOrgClient(org_name)
        self.assertEqual(github_client.org(), {"org_name": org_name})
        get_mock.assert_called_once()

    def test_public_repos_url(self):
        """Test public_repos_url property"""
        with patch.object(GithubOrgClient,
                          'org', new_callable=PropertyMock) as org_mock:
            org_mock.return_value = {"repos_url": "google"}

            github_client = GithubOrgClient("google")
            self.assertEqual(github_client._public_repos_url, "google")

    @patch('client.get_json')
    def test_public_repos(self, get_mock):
        """Test public_repos method"""
        get_mock.return_value = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "Apache"}}
        ]

        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as repos_mock:
            repos_mock.return_value = "mocked_repos_url"

            github_client = GithubOrgClient("mocked_repos_url")
            self.assertEqual(github_client.public_repos(license="MIT"),
                             ["repo1"])
            get_mock.assert_called_once()
            repos_mock.assert_called_once()

    @parameterized.expand([
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False)
        ])
    def test_has_license(self, repo, license, result):
        """Test has_license method"""
        github_client = GithubOrgClient("org_name")
        self.assertEqual(github_client.has_license(repo, license), result)


if __name__ == '__main__':
    unittest.main()
