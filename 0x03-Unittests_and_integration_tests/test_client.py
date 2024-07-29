#!/usr/bin/env python3
"""Test for GithubOrgClient"""
import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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

    @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property"""

        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/{org}/repos"
        }

        client = GithubOrgClient("google")
        result = client._public_repos_url

        expected_url = "https://api.github.com/orgs/google/repos"
        self.assertEqual(result, expected_url)
        mock_org.assert_called_once()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=property)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test the public_repos method"""

        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache2"}},
            {"name": "repo2", "license": {"key": "mit"}}
        ]
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )

        client = GithubOrgClient("google")
        result = client.public_repos()

        self.assertEqual(result, ["repo1"])
        mock_get_json.assert_called_once()
        mock_public_repos_url.assert_called_once()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=property)
    def test_public_repos_with_license(
            self, mock_public_repos_url, mock_get_json):
        """Test the public_repos method with a specific license"""

        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache2"}},
            {"name": "repo2", "license": {"key": "mit"}}
        ]
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )

        client = GithubOrgClient("google")
        result = client.public_repos("apache2")

        self.assertEqual(result, ["repo1"])
        mock_get_json.assert_called_once()
        mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license method"""

        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload,
     "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Setup class with mock data"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: cls.org_payload),
            unittest.mock.Mock(json=lambda: cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """Tear down class"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method with real data"""
        client = GithubOrgClient("google")
        result = client.public_repos("apache2")
        self.assertEqual(result, self.expected_repos)
        self.mock_get.assert_called()


if __name__ == '__main__':
    unittest.main()
