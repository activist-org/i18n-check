# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the repeat_keys.py.
"""

import pytest

from i18n_check.check.repeat_keys import (
    check_file_keys_repeated,
    find_repeat_keys,
    repeat_keys_check,
)

from ..test_utils import (
    fail_checks_src_json_path,
    pass_checks_src_json_path,
)


@pytest.mark.parametrize(
    "json_str,expected",
    [
        (
            fail_checks_src_json_path,
            {
                "i18n._global.repeat_key": [
                    "This key is duplicated",
                    "This key is duplicated, but the value is not",
                ]
            },
        ),
        (pass_checks_src_json_path, {}),
        (
            '{"a": 1, "b": 2, "a": 3, "b": 4, "c": 5}',
            {"a": ["1", "3"], "b": ["2", "4"]},
        ),
        ("{}", {}),
        ('{"a": null, "a": 42}', {"a": ["42", "None"]}),
    ],
)
def test_find_repeat_keys(json_str, expected) -> None:
    assert find_repeat_keys(json_str) == expected


@pytest.mark.parametrize(
    "json_str",
    [
        '{"a": 1, "b": 2,}',  # trailing comma
        '{"a": 1 "b": 2}',  # missing comma
        '{"a": 1, "b": [1, 2,}',  # unclosed array
    ],
)
def test_invalid_json(json_str) -> None:
    with pytest.raises(ValueError, match="Invalid JSON:"):
        find_repeat_keys(json_str)


@pytest.mark.parametrize(
    "file_path,expected_duplicates",
    [
        (
            fail_checks_src_json_path,
            {
                "i18n._global.repeat_key": [
                    "This key is duplicated",
                    "This key is duplicated, but the value is not",
                ]
            },
        ),
        (pass_checks_src_json_path, {}),
    ],
)
def test_check_file_keys_repeated(file_path, expected_duplicates) -> None:
    filename, duplicates = check_file_keys_repeated(file_path)
    assert duplicates == expected_duplicates


def test_check_file_keys_repeated_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        check_file_keys_repeated("nonexistent_file.json")


def test_main_with_duplicates_raises(capsys) -> None:
    with pytest.raises(SystemExit):
        repeat_keys_check()

    output = capsys.readouterr().out
    assert "Repeat keys in" in output
    assert "appears 2 times" in output
    assert "repeat-keys error" in output


if __name__ == "__main__":
    pytest.main()
