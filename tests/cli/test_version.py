# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI version functionality.
"""

import importlib.metadata
import unittest
from unittest.mock import patch

from i18n_check.cli.version import (
    UNKNOWN_VERSION_NOT_FETCHED,
    UNKNOWN_VERSION_NOT_PIP,
    get_latest_version,
    get_local_version,
    get_version_message,
)


class TestVersionFunctions(unittest.TestCase):
    @patch("i18n_check.cli.version.importlib.metadata.version")
    def test_get_local_version_installed(self, mock_version):
        mock_version.return_value = "1.0.0"
        self.assertEqual(get_local_version(), "1.0.0")

    @patch(
        "i18n_check.cli.version.importlib.metadata.version",
        side_effect=importlib.metadata.PackageNotFoundError,
    )
    def test_get_local_version_not_installed(self, mock_version):
        self.assertEqual(get_local_version(), UNKNOWN_VERSION_NOT_PIP)

    @patch("requests.get")
    def test_get_latest_version(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "v1.0.1"}
        self.assertEqual(get_latest_version(), "v1.0.1")

    @patch("requests.get", side_effect=Exception("Unable to fetch version"))
    def test_get_latest_version_failure(self, mock_get):
        self.assertEqual(get_latest_version(), UNKNOWN_VERSION_NOT_FETCHED)

    @patch("i18n_check.cli.version.get_local_version", return_value="X.Y.Z")
    @patch("i18n_check.cli.version.get_latest_version", return_value="i18n-check X.Y.Z")
    def test_get_version_message_up_to_date(
        self, mock_latest_version, mock_local_version
    ):
        """
        Tests the scenario where the local version is up to date with the latest version.
        """
        expected_message = "i18n-check vX.Y.Z"
        self.assertEqual(get_version_message(), expected_message)

    @patch("i18n_check.cli.version.get_local_version", return_value="X.Y.Y")
    @patch("i18n_check.cli.version.get_latest_version", return_value="i18n-check X.Y.Z")
    def test_upgrade_available(self, mock_latest_version, mock_local_version):
        """
        Test case where a newer version is available.
        """
        expected_message = "i18n-check vX.Y.Y (Upgrade available: i18n-check vX.Y.Z). To upgrade: i18n-check -u"
        self.assertEqual(get_version_message(), expected_message)

    @patch(
        "i18n_check.cli.version.get_local_version",
        return_value=UNKNOWN_VERSION_NOT_PIP,
    )
    @patch("i18n_check.cli.version.get_latest_version", return_value="i18n-check X.Y.Z")
    def test_local_version_unknown(self, mock_latest_version, mock_local_version):
        """
        Test case where the local version is unknown.
        """
        self.assertEqual(get_version_message(), UNKNOWN_VERSION_NOT_PIP)

    @patch("i18n_check.cli.version.get_local_version", return_value="X.Y.Z")
    @patch(
        "i18n_check.cli.version.get_latest_version",
        return_value=UNKNOWN_VERSION_NOT_FETCHED,
    )
    def test_latest_version_unknown(self, mock_latest_version, mock_local_version):
        """
        Test case where the latest version cannot be fetched.
        """
        self.assertEqual(get_version_message(), UNKNOWN_VERSION_NOT_FETCHED)


if __name__ == "__main__":
    unittest.main()
