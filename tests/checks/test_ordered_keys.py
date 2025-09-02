# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the ordered_keys.py.
"""

import json
import tempfile
from pathlib import Path

import pytest

from i18n_check.check.ordered_keys import (
    check_file_ordered_keys,
    check_keys_are_ordered,
    check_ordered_keys,
    fix_ordered_keys,
)
from i18n_check.utils import read_json_file

fail_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_fail"
)
fail_checks_json_path = fail_dir / "test_i18n" / "test_i18n_src.json"

pass_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_pass"
)
pass_checks_json_path = pass_dir / "test_i18n" / "test_i18n_src.json"


class TestCheckKeysAreOrdered:
    """
    Tests for the check_keys_are_ordered function.
    """

    def test_ordered_keys(self):
        """
        Test that properly ordered keys are detected as ordered.
        """
        ordered_data = {
            "a_key": "value1",
            "b_key": "value2",
            "c_key": "value3",
        }

        is_ordered, sorted_keys = check_keys_are_ordered(ordered_data)

        assert is_ordered is True
        assert sorted_keys == ["a_key", "b_key", "c_key"]

    def test_unordered_keys(self):
        """
        Test that unordered keys are detected as unordered.
        """
        unordered_data = {
            "c_key": "value3",
            "a_key": "value1",
            "b_key": "value2",
        }

        is_ordered, sorted_keys = check_keys_are_ordered(unordered_data)

        assert is_ordered is False
        assert sorted_keys == ["a_key", "b_key", "c_key"]

    def test_single_key(self):
        """
        Test that a single key is always considered ordered.
        """
        single_key_data = {"only_key": "value"}

        is_ordered, sorted_keys = check_keys_are_ordered(single_key_data)

        assert is_ordered is True
        assert sorted_keys == ["only_key"]

    def test_empty_dict(self):
        """
        Test that an empty dictionary is considered ordered.
        """
        empty_data = {}

        is_ordered, sorted_keys = check_keys_are_ordered(empty_data)

        assert is_ordered is True
        assert sorted_keys == []


class TestCheckFileOrderedKeys:
    """
    Tests for the check_file_ordered_keys function.
    """

    def test_pass_frontend_file(self):
        """
        Test that the pass frontend file has ordered keys.
        """
        is_ordered, sorted_keys = check_file_ordered_keys(pass_checks_json_path)

        assert is_ordered is True
        assert len(sorted_keys) > 0

    def test_fail_frontend_file(self):
        """
        Test that the fail frontend file has unordered keys.
        """
        is_ordered, sorted_keys = check_file_ordered_keys(fail_checks_json_path)

        assert is_ordered is False
        assert len(sorted_keys) > 0


class TestFixOrderedKeys:
    """
    Tests for the fix_ordered_keys function.
    """

    def test_fix_unordered_file(self):
        """
        Test that fixing an unordered file works correctly.
        """
        # Create a temporary file with unordered keys
        unordered_data = {
            "z_key": "value_z",
            "a_key": "value_a",
            "m_key": "value_m",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(unordered_data, temp_file, indent=2)
            temp_file_path = temp_file.name

        try:
            # Verify it's initially unordered
            is_ordered_before, _ = check_file_ordered_keys(temp_file_path)
            assert is_ordered_before is False

            # Fix the file
            fix_result = fix_ordered_keys(temp_file_path)
            assert fix_result is True

            # Verify it's now ordered
            is_ordered_after, sorted_keys = check_file_ordered_keys(temp_file_path)
            assert is_ordered_after is True
            assert sorted_keys == ["a_key", "m_key", "z_key"]

            # Verify the content is preserved
            fixed_data = read_json_file(temp_file_path)
            assert fixed_data["a_key"] == "value_a"
            assert fixed_data["m_key"] == "value_m"
            assert fixed_data["z_key"] == "value_z"

        finally:
            # Clean up
            Path(temp_file_path).unlink()

    def test_fix_already_ordered_file(self):
        """
        Test that fixing an already ordered file doesn't change it.
        """
        # Create a temporary file with ordered keys
        ordered_data = {
            "a_key": "value_a",
            "m_key": "value_m",
            "z_key": "value_z",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(ordered_data, temp_file, indent=2)
            temp_file_path = temp_file.name

        try:
            # Verify it's initially ordered
            is_ordered_before, _ = check_file_ordered_keys(temp_file_path)
            assert is_ordered_before is True

            # Fix the file
            fix_result = fix_ordered_keys(temp_file_path)
            assert fix_result is True

            # Verify it's still ordered
            is_ordered_after, sorted_keys = check_file_ordered_keys(temp_file_path)
            assert is_ordered_after is True
            assert sorted_keys == ["a_key", "m_key", "z_key"]

        finally:
            # Clean up
            Path(temp_file_path).unlink()


class TestCheckOrderedKeysIntegration:
    """
    Integration tests for the check_ordered_keys function.
    """

    def test_check_with_mock_config(self, monkeypatch):
        """
        Test the main check function with mocked configuration.
        """
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create an ordered file
            ordered_file = temp_path / "ordered.json"
            ordered_data = {"a": "1", "b": "2", "c": "3"}
            with open(ordered_file, "w") as f:
                json.dump(ordered_data, f, indent=2)

            # Create an unordered file
            unordered_file = temp_path / "unordered.json"
            unordered_data = {"c": "3", "a": "1", "b": "2"}
            with open(unordered_file, "w") as f:
                json.dump(unordered_data, f, indent=2)

            # Mock the configuration
            monkeypatch.setattr(
                "i18n_check.check.ordered_keys.config_i18n_directory", temp_path
            )
            monkeypatch.setattr("i18n_check.check.ordered_keys.path_separator", "/")

            # Test that check fails when there are unordered files
            with pytest.raises(SystemExit) as exc_info:
                check_ordered_keys(fix=False)
            assert exc_info.value.code == 1

            # Test that fix mode works
            check_ordered_keys(fix=True)

            # Verify both files are now ordered
            ordered_after = read_json_file(ordered_file)
            unordered_after = read_json_file(unordered_file)

            assert list(ordered_after.keys()) == ["a", "b", "c"]
            assert list(unordered_after.keys()) == ["a", "b", "c"]
