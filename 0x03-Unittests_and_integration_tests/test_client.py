#!/usr/bin/env python3
"""Tests for the GithubOrgClient class."""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class"""

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch('client.get_json')
    def test_org_method(self, org_name, mock_get_json):
        """Test the org method to ensure it returns the correct value"""
        mock_get_json.return_value = {"org_name": org_name}

        github_client = GithubOrgClient(org_name)
        self.assertEqual(github_client.org(), {"org_name": org_name})
        mock_get_json.assert_called_once()

    def test_public_repos_url_property(self):
        """Test the _public_repos_url property"""
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "google_repos_url"}

            github_client = GithubOrgClient("google")
            self.assertEqual(
                github_client._public_repos_url,
                "google_repos_url"
            )

    @patch('client.get_json')
    def test_public_repos_method(self, mock_get_json):
        """Test the public_repos method"""
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

            github_client = GithubOrgClient("mocked_repos_url")
            self.assertEqual(
                github_client.public_repos(license="MIT"),
                ["repo1"]
            )
            mock_get_json.assert_called_once()
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license_method(self, repo, license_key, expected_result):
        """Test the has_license method"""
        github_client = GithubOrgClient("org_name")
        self.assertEqual(
            github_client.has_license(repo, license_key),
            expected_result
        )


if __name__ == '__main__':
    unittest.main()
