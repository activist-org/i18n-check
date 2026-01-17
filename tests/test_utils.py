# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for utility functions in i18n-check.
"""

import json
import os
import tempfile
import unittest
import unittest.mock
from pathlib import Path

import pytest

from i18n_check.check.key_naming import map_keys_to_files
from i18n_check.utils import (
    collect_files_to_check,
    filter_valid_key_parts,
    get_all_json_files,
    get_config_file_path,
    is_valid_key,
    lower_and_remove_punctuation,
    path_to_valid_key,
    read_files_to_dict,
    read_json_file,
    replace_text_in_file,
)

# MARK: Test Variables

checks_fail_dir = (
    Path(__file__).parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_fail"
)
checks_fail_json_dir = checks_fail_dir / "test_i18n"

fail_checks_src_json_path = checks_fail_json_dir / "test_i18n_src.json"
fail_checks_src_locale_path = checks_fail_json_dir / "test_i18n_locale.json"
fail_checks_test_file_path = checks_fail_dir / "test_file.ts"
fail_checks_sub_dir_first_file_path = (
    checks_fail_dir / "sub_dir" / "sub_dir_first_file.ts"
)
fail_checks_sub_dir_second_file_path = (
    checks_fail_dir / "sub_dir" / "sub_dir_second_file.ts"
)

fail_checks_src_json = read_json_file(file_path=fail_checks_src_json_path)
fail_checks_locale_json = read_json_file(file_path=fail_checks_src_locale_path)
i18n_map_fail = map_keys_to_files(
    i18n_src_dict=fail_checks_src_json, src_directory=checks_fail_dir
)

checks_pass_dir = (
    Path(__file__).parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_pass"
)
checks_pass_json_dir = checks_pass_dir / "test_i18n"

pass_checks_src_json_path = checks_pass_json_dir / "test_i18n_src.json"

pass_checks_src_json = read_json_file(file_path=pass_checks_src_json_path)
i18n_map_pass = map_keys_to_files(
    i18n_src_dict=pass_checks_src_json, src_directory=checks_pass_dir
)

# MARK: Utils Tests


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

            with open(valid_file, "w", encoding="utf-8") as f:
                f.write("test")
            with open(skipped_file, "w", encoding="utf-8") as f:
                f.write("test")
            with open(file_in_skip_dir, "w", encoding="utf-8") as f:
                f.write("test")

            result = collect_files_to_check(
                directory=temp_dir,
                file_types_to_check=[".txt"],
                directories_to_skip=[Path(temp_dir) / "skip_dir"],
                files_to_skip=[Path(temp_dir) / "skip.txt"],
            )

            assert any("valid.txt" in r for r in result)
            assert skipped_file not in result
            assert file_in_skip_dir not in result

    def test_get_all_json_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file_1 = os.path.join(temp_dir, "file1.json")
            json_file_2 = os.path.join(temp_dir, "file2.json")
            non_json_file = os.path.join(temp_dir, "file.txt")

            with open(json_file_1, "w", encoding="utf-8") as f:
                f.write("{}")
            with open(json_file_2, "w", encoding="utf-8") as f:
                f.write("{}")
            with open(non_json_file, "w", encoding="utf-8") as f:
                f.write("test")

            result = get_all_json_files(directory=temp_dir)

            assert os.path.realpath(json_file_1) in result
            assert os.path.realpath(json_file_2) in result
            assert non_json_file not in result

    def test_read_files_to_dict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = os.path.join(temp_dir, "file1.txt")
            file2 = os.path.join(temp_dir, "file2.txt")

            content1 = "Hello, world!"
            content2 = "Python testing."

            with open(file1, "w", encoding="utf-8") as f:
                f.write(content1)
            with open(file2, "w", encoding="utf-8") as f:
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


def test_successful_replacement(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello World!", encoding="utf-8")

    replace_text_in_file(file_path, old="World", new="Universe")

    assert file_path.read_text(encoding="utf-8") == "Hello Universe!"


def test_no_replacement_when_old_not_found(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello World!", encoding="utf-8")

    replace_text_in_file(file_path, old="Galaxy", new="Universe")

    # Content should remain unchanged.
    assert file_path.read_text(encoding="utf-8") == "Hello World!"


def test_replacement_with_multiple_occurrences(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("abc abc abc", encoding="utf-8")

    replace_text_in_file(file_path, old="abc", new="xyz")

    assert file_path.read_text(encoding="utf-8") == "xyz xyz xyz"


def test_print_output_on_successful_replacement(tmp_path, capsys):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Replace this text", encoding="utf-8")

    replace_text_in_file(file_path, old="Replace this text", new="New text")

    output = capsys.readouterr().out
    assert "✨ Replaced 'Replace this text' with 'New text'" in output
    assert "sample.txt" in output


def test_print_output_on_no_replacement(tmp_path, capsys):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("nothing to change here", encoding="utf-8")

    replace_text_in_file(file_path, old="old", new="new")

    output = capsys.readouterr().out
    assert output == ""


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


def test_get_config_file_path_yaml_exists(tmp_path) -> None:
    """
    Test that .yaml file is preferred when both .yaml and .yml exist.
    """
    yaml_file = tmp_path / ".i18n-check.yaml"
    yml_file = tmp_path / ".i18n-check.yml"

    yaml_file.write_text("yaml: true", encoding="utf-8")
    yml_file.write_text("yml: true", encoding="utf-8")

    # Mock CWD_PATH to use tmp_path.
    with unittest.mock.patch("i18n_check.utils.CWD_PATH", tmp_path):
        result = get_config_file_path()
        assert result.name == ".i18n-check.yaml"
        assert result.is_file()


def test_get_config_file_path_only_yml_exists(tmp_path) -> None:
    """
    Test that .yml file is found when only .yml exists.
    """
    yml_file = tmp_path / ".i18n-check.yml"
    yml_file.write_text("yml: true", encoding="utf-8")

    # Mock CWD_PATH to use tmp_path.
    with unittest.mock.patch("i18n_check.utils.CWD_PATH", tmp_path):
        result = get_config_file_path()
        assert result.name == ".i18n-check.yml"
        assert result.is_file()


def test_get_config_file_path_neither_exists(tmp_path) -> None:
    """
    Test that .yaml is returned as default when neither file exists.
    """
    # Mock CWD_PATH to use tmp_path.
    with unittest.mock.patch("i18n_check.utils.CWD_PATH", tmp_path):
        result = get_config_file_path()
        assert result.name == ".i18n-check.yaml"
        assert not result.is_file()


if __name__ == "__main__":
    unittest.main()
