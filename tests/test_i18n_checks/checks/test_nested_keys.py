# SPDX-License-Identifier: GPL-3.0-or-later
"""
Test script for nested_keys.py functionality.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from i18n_check.check.nested_keys import check_i18n_files, is_nested_json


class TestIsNestedJson(unittest.TestCase):
    """Test cases for the is_nested_json function."""

    def test_json_structure_detection(self):
        """Test various JSON structures."""
        test_cases = [
            # (description, input_data, expected_result)
            ("flat JSON", {"key1": "value1", "key2": "value2"}, False),
            ("nested JSON", {"key1": {"nested": "value"}, "key2": "value2"}, True),
            ("deeply nested JSON", {"key": {"nested": {"deep": "value"}}}, True),
            ("empty JSON", {}, False),
            ("non-dict input", ["list", "of", "values"], False),
            ("mixed content", {"key1": "value", "key2": {"nested": "value"}}, True),
        ]

        for desc, data, expected in test_cases:
            with self.subTest(desc):
                self.assertEqual(is_nested_json(data), expected)


class TestCheckI18nFiles(unittest.TestCase):
    """Test cases for the check_i18n_files function."""

    def setUp(self):
        """Set up temporary directory with test JSON files."""
        self.temp_dir = tempfile.mkdtemp()

        # Test files data: (filename, content, is_valid)
        test_files = [
            ("flat.json", {"key1": "value1", "key2": "value2"}, True),
            ("nested.json", {"key1": {"nested": "value"}, "key2": "value2"}, True),
            ("invalid.json", "{invalid json}", False),
        ]

        for filename, content, is_valid in test_files:
            path = os.path.join(self.temp_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                if is_valid:
                    json.dump(content, f)
                else:
                    f.write(content)
            setattr(self, f"{filename.split('.')[0]}_json_path", path)

    def _assert_warning_printed(self, mock_print, path, should_be_present):
        """Helper to check if warning was printed for a specific file."""
        found = any(
            f"Warning: Nested JSON structure detected in {path}" in str(call)
            for call in mock_print.call_args_list
        )
        self.assertEqual(found, should_be_present)

    def _assert_error_printed(self, mock_print, path):
        """Helper to check if error was printed for a specific file."""
        self.assertTrue(
            any(
                f"Error processing {path}" in str(call)
                for call in mock_print.call_args_list
            )
        )

    @patch("i18n_check.check.nested_keys.warn_on_nested_keys", True)
    @patch("builtins.print")
    def test_check_i18n_files_with_warnings(self, mock_print):
        """Test check_i18n_files with warning enabled."""
        check_i18n_files(self.temp_dir)

        self._assert_warning_printed(mock_print, self.nested_json_path, True)
        self._assert_warning_printed(mock_print, self.flat_json_path, False)
        self._assert_error_printed(mock_print, self.invalid_json_path)

    @patch("i18n_check.check.nested_keys.warn_on_nested_keys", False)
    @patch("builtins.print")
    def test_check_i18n_files_without_warnings(self, mock_print):
        """Test check_i18n_files with warning disabled."""
        check_i18n_files(self.temp_dir)

        # Just check no warnings at all were printed
        self.assertFalse(
            any(
                "Warning: Nested JSON structure detected" in str(call)
                for call in mock_print.call_args_list
            )
        )

    def test_check_i18n_files_with_nonexistent_directory(self):
        """Test check_i18n_files with nonexistent directory."""
        with self.assertRaises(FileNotFoundError):
            check_i18n_files("/nonexistent/directory")
