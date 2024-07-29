#!/usr/bin/env python3
"""Unit and integration tests for the GithubOrgClient class."""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock
from typing import Dict, List
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
        self, repo: Dict, license_key: str, expected_result: bool
    ) -> None:
        """Test the has_license method of GithubOrgClient."""
        client = GithubOrgClient("org_name")
        self.assertEqual(
            client.has_license(repo, license_key),
            expected_result
        )


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    [
        # Add the fixtures data here from fixtures.py
        (
            {"login": "google", "repos_url": "https://api.github.com/orgs/google/repos"},
            [
                {"name": "episodes.dart", "license": {"key": "bsd-3-clause"}},
                {"name": "cpp-netlib", "license": {"key": "apache-2.0"}}
            ],
            ["episodes.dart", "cpp-netlib"],
            ["cpp-netlib"]
        )
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test suite for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class method to start patching."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return MockResponse(cls.repos_payload)
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class method to stop patching."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test the public_repos method of GithubOrgClient."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test public_repos method with a license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


class MockResponse:
    """Mock response class for requests.get."""

    def __init__(self, json_data: dict) -> None:
        self.json_data = json_data

    def json(self) -> dict:
        """Return the JSON data."""
        return self.json_data


if __name__ == '__main__':
    unittest.main()
