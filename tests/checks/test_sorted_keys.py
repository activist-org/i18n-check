# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the sorted_keys.py.
"""

import json
import tempfile
from pathlib import Path

import pytest

from i18n_check.check.sorted_keys import (
    check_file_keys_sorted,
    check_file_sorted,
    fix_sorted_keys,
    sorted_keys_check_and_fix,
)
from i18n_check.utils import read_json_file

from ..test_utils import fail_checks_src_json_path, pass_checks_src_json_path


class TestCheckKeysAreSorted:
    """
    Tests for the check_file_keys_sorted function.
    """

    def test_sorted_keys(self):
        """
        Test that properly sorted keys are detected as sorted.
        """
        sorted_data = {
            "a_key": "value1",
            "b_key": "value2",
            "c_key": "value3",
        }

        is_sorted, sorted_keys = check_file_keys_sorted(sorted_data)

        assert is_sorted is True
        assert sorted_keys == ["a_key", "b_key", "c_key"]

    def test_unsorted_keys(self):
        """
        Test that unsorted keys are detected as unsorted.
        """
        unsorted_data = {
            "c_key": "value3",
            "a_key": "value1",
            "b_key": "value2",
        }

        is_sorted, sorted_keys = check_file_keys_sorted(unsorted_data)

        assert is_sorted is False
        assert sorted_keys == ["a_key", "b_key", "c_key"]

    def test_single_key(self):
        """
        Test that a single key is always considered sorted.
        """
        single_key_data = {"only_key": "value"}

        is_sorted, sorted_keys = check_file_keys_sorted(single_key_data)

        assert is_sorted is True
        assert sorted_keys == ["only_key"]

    def test_empty_dict(self):
        """
        Test that an empty dictionary is considered sorted.
        """
        empty_data = {}

        is_sorted, sorted_keys = check_file_keys_sorted(empty_data)

        assert is_sorted is True
        assert sorted_keys == []


class TestCheckFileSortedKeys:
    """
    Tests for the check_file_sorted function.
    """

    def test_pass_frontend_file(self):
        """
        Test that the pass frontend file has sorted keys.
        """
        is_sorted, sorted_keys = check_file_sorted(pass_checks_src_json_path)

        assert is_sorted is True
        assert len(sorted_keys) > 0

    def test_fail_frontend_file(self):
        """
        Test that the fail frontend file has unsorted keys.
        """
        is_sorted, sorted_keys = check_file_sorted(fail_checks_src_json_path)

        assert is_sorted is False
        assert len(sorted_keys) > 0


class TestFixSortedKeys:
    """
    Tests for the fix_sorted_keys function.
    """

    def test_fix_unsorted_file(self):
        """
        Test that fixing an unsorted file works correctly.
        """
        # Create a temporary file with unsorted keys.
        unsorted_data = {
            "z_key": "value_z",
            "a_key": "value_a",
            "m_key": "value_m",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(unsorted_data, temp_file, indent=2)
            temp_file_path = temp_file.name

        try:
            # Verify it's initially unsorted.
            is_sorted_before, _ = check_file_sorted(temp_file_path)
            assert is_sorted_before is False

            # Fix the file.
            fix_result = fix_sorted_keys(temp_file_path)
            assert fix_result is True

            # Verify it's now sorted.
            is_sorted_after, sorted_keys = check_file_sorted(temp_file_path)
            assert is_sorted_after is True
            assert sorted_keys == ["a_key", "m_key", "z_key"]

            # Verify the content is preserved.
            fixed_data = read_json_file(temp_file_path)
            assert fixed_data["a_key"] == "value_a"
            assert fixed_data["m_key"] == "value_m"
            assert fixed_data["z_key"] == "value_z"

        finally:
            Path(temp_file_path).unlink()

    def test_fix_already_sorted_file(self):
        """
        Test that fixing an already sorted file doesn't change it.
        """
        # Create a temporary file with sorted keys.
        sorted_data = {
            "a_key": "value_a",
            "m_key": "value_m",
            "z_key": "value_z",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(sorted_data, temp_file, indent=2)
            temp_file_path = temp_file.name

        try:
            # Verify it's initially sorted.
            is_sorted_before, _ = check_file_sorted(temp_file_path)
            assert is_sorted_before is True

            # Fix the file.
            fix_result = fix_sorted_keys(temp_file_path)
            assert fix_result is True

            # Verify it's still sorted.
            is_sorted_after, sorted_keys = check_file_sorted(temp_file_path)
            assert is_sorted_after is True
            assert sorted_keys == ["a_key", "m_key", "z_key"]

        finally:
            Path(temp_file_path).unlink()


class TestCheckSortedKeysIntegration:
    """
    Integration tests for the sorted_keys_check_and_fix function.
    """

    def test_check_with_mock_config(self, monkeypatch):
        """
        Test the main check function with mocked configuration.
        """
        # Create a temporary directory with test files.
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create an sorted file.
            sorted_file = temp_path / "sorted.json"
            sorted_data = {"a": "1", "b": "2", "c": "3"}
            with open(sorted_file, "w", encoding="utf-8") as f:
                json.dump(sorted_data, f, indent=2)

            # Create an unsorted file.
            unsorted_file = temp_path / "unsorted.json"
            unsorted_data = {"c": "3", "a": "1", "b": "2"}
            with open(unsorted_file, "w", encoding="utf-8") as f:
                json.dump(unsorted_data, f, indent=2)

            # Mock the configuration.
            monkeypatch.setattr(
                "i18n_check.check.sorted_keys.config_i18n_directory", temp_path
            )

            # Test that check fails when there are unsorted files.
            with pytest.raises(SystemExit) as exc_info:
                sorted_keys_check_and_fix(fix=False)

            assert exc_info.value.code == 1

            # Test that fix mode works.
            sorted_keys_check_and_fix(fix=True)

            # Verify both files are now sorted.
            sorted_after = read_json_file(sorted_file)
            unsorted_after = read_json_file(unsorted_file)

            assert list(sorted_after.keys()) == ["a", "b", "c"]
            assert list(unsorted_after.keys()) == ["a", "b", "c"]
