#!/usr/bin/env python3
"""Unit and integration tests for the GithubOrgClient class."""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for the GithubOrgClient class."""

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = {"org_name": org_name}

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), {"org_name": org_name})
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test the _public_repos_url property of GithubOrgClient."""
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}

            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method of GithubOrgClient."""
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "Apache"}}
        ]

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "mocked_repos_url"

            client = GithubOrgClient("mocked_repos_url")
            self.assertEqual(
                client.public_repos(license="MIT"),
                ["repo1"]
            )
            mock_get_json.assert_called_once()
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test the has_license method of GithubOrgClient."""
        client = GithubOrgClient("org_name")
        self.assertEqual(
            client.has_license(repo, license_key),
            expected_result
        )

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up the patcher for integration tests."""
        cls.get_patcher = patch('client.get_json')
        cls.mock_get_json = cls.get_patcher.start()

        from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
        cls.org_payload = org_payload
        cls.repos_payload = repos_payload
        cls.expected_repos = expected_repos
        cls.apache2_repos = apache2_repos

        cls.mock_get_json.side_effect = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }.get

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after integration tests."""
        cls.get_patcher.stop()

    @parameterized.expand([
        ('public_repos', 'https://api.github.com/orgs/google/repos', 'MIT', ['repo1']),
        ('public_repos_with_license', 'https://api.github.com/orgs/google/repos', 'apache-2.0', ['apache2_repo'])
    ])
    def test_public_repos(self, test_name, repos_url, license_key, expected_repos):
        """Test the public_repos method of GithubOrgClient using fixtures."""
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = repos_url

            client = GithubOrgClient("google")
            self.assertEqual(
                client.public_repos(license=license_key),
                expected_repos
            )
            self.mock_get_json.assert_called_once_with(repos_url)
            mock_public_repos_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()
