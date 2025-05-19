# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the repeat_keys.py.
"""

from pathlib import Path

import pytest

from i18n_check.check.repeat_keys import (
    check_file,
    find_repeat_keys,
    validate_repeat_keys,
)

fail_checks_json = (
    Path(__file__).parent.parent
    / "test_frontends"
    / "all_checks_fail"
    / "test_i18n"
    / "test_i18n_src.json"
)
pass_checks_json = (
    Path(__file__).parent.parent
    / "test_frontends"
    / "all_checks_pass"
    / "test_i18n"
    / "test_i18n_src.json"
)


@pytest.mark.parametrize(
    "json_str,expected",
    [
        (
            fail_checks_json,
            {
                "i18n._global.hello_global_repeat": [
                    "This key is duplicated",
                    "hello, global!",
                ]
            },
        ),
        (pass_checks_json, {}),
        (
            '{"a": 1, "b": 2, "a": 3, "b": 4, "c": 5}',
            {"a": ["1", "3"], "b": ["2", "4"]},
        ),
        ("{}", {}),
        ('{"a": null, "a": 42}', {"a": ["None", "42"]}),
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
            fail_checks_json,
            {
                "i18n._global.hello_global_repeat": [
                    "This key is duplicated",
                    "hello, global!",
                ]
            },
        ),
        (pass_checks_json, {}),
    ],
)
def test_check_file(file_path, expected_duplicates) -> None:
    filename, duplicates = check_file(file_path)
    assert duplicates == expected_duplicates


def test_check_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        check_file("nonexistent_file.json")


# Note: capsys is a fixture for capturing system outputs.
def test_main_with_duplicates_raises(capsys) -> None:
    with pytest.raises(ValueError) as exc_info:
        validate_repeat_keys()

    output = capsys.readouterr().out
    assert "Duplicate keys in" in output
    assert "appears 2 times" in output
    assert "repeat_keys failure" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
