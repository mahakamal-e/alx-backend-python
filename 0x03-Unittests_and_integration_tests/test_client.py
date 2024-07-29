#!/usr/bin/env python3
"""Unit and integration tests for the GithubOrgClient class."""

import unittest
from parameterized import parameterized
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
    def test_org(self, org_name: str, mock_get_json: unittest.mock.Mock) -> None:
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = {"org_name": org_name}

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), {"org_name": org_name})
        mock_get_json.assert_called_once()

    def test_public_repos_url(self) -> None:
        """Test the _public_repos_url property of GithubOrgClient."""
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }

            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: unittest.mock.Mock) -> None:
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
    def test_has_license(
        self, repo: dict, license_key: str, expected_result: bool
    ) -> None:
        """Test the has_license method of GithubOrgClient."""
        client = GithubOrgClient("org_name")
        self.assertEqual(
            client.has_license(repo, license_key),
            expected_result
        )


if __name__ == '__main__':
    unittest.main()
