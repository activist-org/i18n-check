# SPDX-License-Identifier: GPL-3.0-or-later
"""
Test script for nested_keys.py functionality.
"""

import unittest

import pytest

from i18n_check.check.nested_keys import is_nested_json, validate_nested_keys
from i18n_check.utils import read_json_file

from ..test_utils import checks_fail_json_dir, checks_pass_json_dir


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
                read_json_file(file_path=checks_pass_json_dir / "test_i18n_src.json"),
                False,
            ),
            (
                "nested JSON",
                read_json_file(file_path=checks_fail_json_dir / "test_i18n_src.json"),
                True,
            ),
            ("deeply nested JSON", {"key": {"nested": {"deep": "value"}}}, True),
            ("empty JSON", {}, False),
            ("non-dict input", ["list", "of", "values"], False),
        ]

        for desc, data, expected in test_cases:
            with self.subTest(desc):
                self.assertEqual(is_nested_json(data), expected)


class TestCheckI18nFiles:
    """
    Test cases for the validate_nested_keys function.
    """

    def test_validate_nested_keys_with_warnings(self, capsys) -> None:
        """
        Test that validate_nested_keys prints a warning for nested files.
        """
        # Test the failing case.
        validate_nested_keys(checks_fail_json_dir)
        captured_fail = capsys.readouterr()

        # The output from `rich` might have extra newlines or formatting.
        assert (
            "nested_keys error: Nested JSON structure detected in"
            in captured_fail.out.replace("\n", "")
        )
        assert "test_i18n_src.json" in captured_fail.out.replace("\n", "")
        assert (
            "i18n-check recommends using flat JSON files"
            in captured_fail.out.replace("\n", "")
        )

        # Test the passing case.
        validate_nested_keys(checks_pass_json_dir)
        captured_pass = capsys.readouterr()
        assert captured_pass.out == ""

    def test_validate_nested_keys_with_nonexistent_directory(self) -> None:
        """
        Test validate_nested_keys with a nonexistent directory.
        """
        with pytest.raises(FileNotFoundError):
            validate_nested_keys("/nonexistent/directory")


if __name__ == "__main__":
    pytest.main()
