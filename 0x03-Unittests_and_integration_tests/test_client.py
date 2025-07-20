#!/usr/bin/env python3
"""A module for testing the `GithubOrgClient` class and its methods."""

import unittest
from typing import Dict
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the `GithubOrgClient` class."""

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, resp: Dict, mocked_fxn: MagicMock) -> None:
        """Tests the `org` method of `GithubOrgClient`.

        Args:
            org (str): The organization login.
            resp (Dict): The expected response from the `get_json` function.
            mocked_fxn (MagicMock): Mocked `get_json` function.

        Asserts:
            The `org` method returns the expected response,
            and the `get_json` function is called with the correct URL.
        """
        mocked_fxn.return_value = resp
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org, resp)  # <-- تم التصحيح هنا
        mocked_fxn.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    def test_public_repos_url(self) -> None:
        """Tests the `_public_repos_url` property of `GithubOrgClient`.

        Asserts:
            The `_public_repos_url` property returns the expected URL.
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method of `GithubOrgClient`.

        Args:
            mock_get_json (MagicMock): Mocked `get_json` function.

        Asserts:
            The `public_repos` method returns the correct list
            of repository names and `_public_repos_url` is called once.
        """
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                ["episodes.dart", "kratu"],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "my_license"}}, "my_license", True),
        ({'license': {'key': "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self, repo: Dict, license_key: str, expected: bool
    ) -> None:
        """Tests the `has_license` method of `GithubOrgClient`.

        Args:
            repo (Dict): The repository data containing license information.
            license_key (str): The license key to check for.
            expected (bool): The expected result of the `has_license` method.

        """
        gh_org_client = GithubOrgClient("google")
        self.assertEqual(
            gh_org_client.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the `GithubOrgClient` class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures for integration tests.

        Sets up a mock for `requests.get`,
        to return predefined responses based on the request URL.
        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url: str):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            raise HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method with integration data.

        Asserts:
            The `public_repos` method returns
            the expected list of repositories.
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a specific license
        using integration data.

        Asserts:
            The `public_repos` method returns
            the expected list of repositories filtered by license.
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleans up class fixtures after running all tests."""
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()
