# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for utility functions in i18n-check.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import pytest

from i18n_check.utils import (
    collect_files_to_check,
    filter_valid_key_parts,
    get_all_json_files,
    is_valid_key,
    lower_and_remove_punctuation,
    path_to_valid_key,
    read_files_to_dict,
    read_json_file,
)


class TestUtils(unittest.TestCase):
    def test_read_json_file(self) -> None:
        # Sample JSON data.
        sample_data = {"name": "Test", "value": 123}

        # Create a temp JSON.
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, encoding="utf-8", suffix=".json"
        ) as temp_file:
            json.dump(sample_data, temp_file)
            temp_file_path = temp_file.name

        # Read the JSON file using the function.
        result = read_json_file(file_path=temp_file_path)

        assert isinstance(result, dict)
        assert result == sample_data

    def test_collect_files_to_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skip_dir = os.path.join(temp_dir, "skip_dir")
            os.makedirs(skip_dir)

            valid_file = os.path.join(temp_dir, "valid.txt")
            skipped_file = os.path.join(temp_dir, "skip.txt")
            file_in_skip_dir = os.path.join(skip_dir, "file_in_skip_dir.txt")

            with open(valid_file, "w") as f:
                f.write("test")
            with open(skipped_file, "w") as f:
                f.write("test")
            with open(file_in_skip_dir, "w") as f:
                f.write("test")

            result = collect_files_to_check(
                directory=temp_dir,
                file_types=[".txt"],
                directories_to_skip=["skip_dir"],
                files_to_skip=["skip.txt"],
            )

            assert valid_file in result
            assert skipped_file not in result
            assert file_in_skip_dir not in result

    def test_get_all_json_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file_1 = os.path.join(temp_dir, "file1.json")
            json_file_2 = os.path.join(temp_dir, "file2.json")
            non_json_file = os.path.join(temp_dir, "file.txt")

            with open(json_file_1, "w") as f:
                f.write("{}")
            with open(json_file_2, "w") as f:
                f.write("{}")
            with open(non_json_file, "w") as f:
                f.write("test")

            result = get_all_json_files(temp_dir, os.sep)

            assert json_file_1 in result
            assert json_file_2 in result
            assert non_json_file not in result

    def test_read_files_to_dict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = os.path.join(temp_dir, "file1.txt")
            file2 = os.path.join(temp_dir, "file2.txt")

            content1 = "Hello, world!"
            content2 = "Python testing."

            with open(file1, "w") as f:
                f.write(content1)
            with open(file2, "w") as f:
                f.write(content2)

            result = read_files_to_dict([file1, file2])

            assert isinstance(result, dict)
            assert result[file1] == content1
            assert result[file2] == content2

    def test_is_valid_key(self) -> None:
        assert is_valid_key("valid.key")
        assert is_valid_key("valid_key")
        assert is_valid_key("validkey123")
        assert not is_valid_key("Invalid-Key")
        assert not is_valid_key("invalid key")
        assert not is_valid_key("invalid/key")


@pytest.mark.parametrize(
    "input_path, expected_key",
    [
        (os.path.join("user", "ProfilePage"), "user.profile_page"),
        (os.path.join("admin", "Config", "Settings"), "admin.config.settings"),
        (os.path.join("API", "v1", "RequestData"), "api.v1.request_data"),
        (
            os.path.join("folder", "SubFolder", "FileName"),
            "folder.sub_folder.file_name",
        ),
        (os.path.join("nested.[id]", "path", "File"), "nested.path.file"),
    ],
)
def test_path_to_valid_key(input_path, expected_key) -> None:
    assert path_to_valid_key(input_path) == expected_key


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        (["word", "word_suffix"], ["word_suffix"]),
        (["abc", "def", "ghi"], ["abc", "def", "ghi"]),
        (["prefix", "suffix", "prefix_suffix"], ["prefix_suffix"]),
        (["AnItem"], ["AnItem"]),
        ([], []),
    ],
)
def test_filter_valid_key_parts(input_list, expected_output) -> None:
    assert filter_valid_key_parts(input_list) == expected_output


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        (
            r"Remove all Python's punctuation except the: !#$%\"&'()*+,-./:;<=>?@[\]^_`{|}~ Mark",
            "remove all pythons punctuation except the ! mark",
        )
    ],
)
def test_lower_and_remove_punctuation(input_list, expected_output) -> None:
    assert lower_and_remove_punctuation(input_list) == expected_output


class TestRunCheck(unittest.TestCase):
    @patch("i18n_check.utils.subprocess.run")
    def test_run_check_success(self, mock_subprocess_run):
        """Test run_check returns True on successful subprocess run."""
        mock_subprocess_run.return_value = None
        from i18n_check.utils import run_check

        result = run_check("test_script")
        self.assertTrue(result)
        mock_subprocess_run.assert_called_once_with(
            ["python", "-m", "i18n_check.check.test_script"],
            check=True,
        )

    @patch("i18n_check.utils.subprocess.run")
    @patch("builtins.print")
    def test_run_check_failure_with_error_output(self, mock_print, mock_subprocess_run):
        """Test run_check shows error message by default when subprocess fails."""
        from subprocess import CalledProcessError

        from i18n_check.utils import run_check

        mock_subprocess_run.side_effect = CalledProcessError(
            1, ["python", "-m", "test"]
        )

        result = run_check("test_script")
        self.assertFalse(result)
        mock_print.assert_called_once()
        self.assertIn("Error running test_script:", mock_print.call_args[0][0])

    @patch("i18n_check.utils.subprocess.run")
    @patch("builtins.print")
    def test_run_check_failure_suppress_errors(self, mock_print, mock_subprocess_run):
        """Test run_check suppresses error message when suppress_errors=True."""
        from subprocess import CalledProcessError

        from i18n_check.utils import run_check

        mock_subprocess_run.side_effect = CalledProcessError(
            1, ["python", "-m", "test"]
        )

        result = run_check("test_script", suppress_errors=True)
        self.assertFalse(result)
        mock_print.assert_not_called()


if __name__ == "__main__":
    unittest.main()
