# SPDX-License-Identifier: GPL-3.0-or-later
"""
Test script for nested_files.py functionality.
"""

import json
import unittest

import pytest

from i18n_check.check.nested_files import (
    flatten_json,
    is_nested_json,
    nested_files_check,
    nested_files_check_and_fix,
)
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
            # Note: (description, input_data, expected_result).
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
    Test cases for the nested_files_check function.
    """

    def test_nested_files_check_with_warnings(self, capsys) -> None:
        """
        Test that nested_files_check prints a warning for nested files.
        """
        # Test the failing case.
        nested_files_check(directory=checks_fail_json_dir)
        captured_fail = capsys.readouterr()

        # The output from `rich` might have extra newlines or formatting.
        assert (
            "nested-files error: Nested JSON structure detected in"
            in captured_fail.out.replace("\n", "")
        )
        assert "test_i18n_src.json" in captured_fail.out.replace("\n", "")
        assert (
            "i18n-check recommends using flat JSON files"
            in captured_fail.out.replace("\n", "")
        )

        # Test the passing case.
        nested_files_check(directory=checks_pass_json_dir)
        captured_pass = capsys.readouterr()
        assert captured_pass.out == ""

    def test_nested_files_check_with_nonexistent_directory(self) -> None:
        """
        Test nested_files_check with a nonexistent directory.
        """
        with pytest.raises(FileNotFoundError):
            nested_files_check(directory="/nonexistent/directory")

    def test_flatten_json_reports_key_collision(self) -> None:
        """
        Test that flatten_json reports collisions for duplicate flattened keys.
        """
        flattened, has_collision = flatten_json({"a": {"b": 1}, "a.b": 2})

        assert has_collision is True
        assert flattened["a.b"] == 2

    def test_nested_files_check_and_fix_flattens_nested_json(
        self, tmp_path, capsys
    ) -> None:
        """
        Test that nested_files_check_and_fix rewrites nested JSON.
        """
        nested_file = tmp_path / "nested.json"
        nested_file.write_text(
            json.dumps({"auth": {"login": "Login", "logout": "Logout"}}, indent=2),
            encoding="utf-8",
        )

        result = nested_files_check_and_fix(directory=tmp_path)
        captured = capsys.readouterr()

        assert result is True
        assert "Flattening nested JSON in 1 file" in captured.out
        assert "Flattened nested keys" in captured.out
        assert read_json_file(nested_file) == {
            "auth.login": "Login",
            "auth.logout": "Logout",
        }

    def test_nested_files_check_and_fix_reports_collision_without_rewriting(
        self, tmp_path, capsys
    ) -> None:
        """
        Test that fix mode reports collisions and leaves the file unchanged.
        """
        nested_file = tmp_path / "nested_collision.json"
        original = {"auth": {"login": "Login"}, "auth.login": "Existing"}
        nested_file.write_text(json.dumps(original, indent=2), encoding="utf-8")

        result = nested_files_check_and_fix(tmp_path)
        captured = capsys.readouterr()

        assert result is False
        assert "Key collision detected" in captured.out
        assert read_json_file(nested_file) == original


if __name__ == "__main__":
    pytest.main()
