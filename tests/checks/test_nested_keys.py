# SPDX-License-Identifier: GPL-3.0-or-later
"""
Test script for nested_keys.py functionality.
"""

import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

from i18n_check.check.nested_keys import is_nested_json, validate_nested_keys
from i18n_check.utils import read_json_file

fail_json_dir = (
    Path(__file__).parent.parent / "test_frontends" / "all_checks_fail" / "test_i18n"
)
pass_json_dir = (
    Path(__file__).parent.parent / "test_frontends" / "all_checks_pass" / "test_i18n"
)


class TestIsNestedJson(unittest.TestCase):
    """
    Test cases for the is_nested_json function.
    """

    def test_json_structure_detection(self) -> None:
        """
        Test various JSON structures.
        """
        test_cases = [
            # (description, input_data, expected_result)
            (
                "flat JSON",
                read_json_file(file_path=pass_json_dir / "test_i18n_src.json"),
                False,
            ),
            (
                "nested JSON",
                read_json_file(file_path=fail_json_dir / "test_i18n_src.json"),
                True,
            ),
            ("deeply nested JSON", {"key": {"nested": {"deep": "value"}}}, True),
            ("empty JSON", {}, False),
            ("non-dict input", ["list", "of", "values"], False),
        ]

        for desc, data, expected in test_cases:
            with self.subTest(desc):
                self.assertEqual(is_nested_json(data), expected)


class TestCheckI18nFiles(unittest.TestCase):
    """
    Test cases for the check_i18n_files function.
    """

    def setUp(self) -> None:
        """
        Set up test JSON files.
        """
        self.fail_files = fail_json_dir
        self.pass_files = list(pass_json_dir.glob("*.json"))
        self.json_files = self.pass_files + [self.fail_files]

    def _assert_warning_printed(self, mock_print, path, should_be_present) -> None:
        """
        Helper to check if warning was printed for a specific file.
        """
        found = any(
            f"Warning: Nested JSON structure detected in {path}" in str(call)
            for call in mock_print.call_args_list
        )
        self.assertEqual(found, should_be_present)

    @patch("i18n_check.check.nested_keys.warn_on_nested_keys", True)
    @patch("builtins.print")
    def test_validate_nested_keys_with_warnings(self, mock_print) -> None:
        """
        Test validate_nested_keys with warning enabled.
        """

        for file in self.json_files:
            validate_nested_keys(file)

        self._assert_warning_printed(mock_print, self.fail_files, True)
        self._assert_warning_printed(mock_print, self.pass_files, False)

    @patch("i18n_check.check.nested_keys.warn_on_nested_keys", False)
    @patch("builtins.print")
    def test_validate_nested_keys_without_warnings(self, mock_print) -> None:
        """
        Test validate_nested_keys with warning disabled.
        """
        for file in self.json_files:
            validate_nested_keys(file)

        # Check no warnings at all were printed.
        self.assertFalse(
            any(
                "Warning: Nested JSON structure detected" in str(call)
                for call in mock_print.call_args_list
            )
        )

    def test_validate_nested_keys_with_nonexistent_directory(self) -> None:
        """
        Test validate_nested_keys with nonexistent directory.
        """
        with self.assertRaises(FileNotFoundError):
            validate_nested_keys("/nonexistent/directory")


if __name__ == "__main__":
    pytest.main()
