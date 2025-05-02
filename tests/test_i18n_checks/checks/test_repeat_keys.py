# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for the repeat_keys.py.
"""

import pytest

from i18n_check.check.repeat_keys import check_file, find_duplicate_keys


@pytest.mark.parametrize(
    "json_str,expected",
    [
        ('{"a": 1, "a": 2, "b": 3}', {"a": ["1", "2"]}),
        ('{"a": 1, "b": 2, "c": 3}', {}),
        (
            '{"a": 1, "b": 2, "a": 3, "b": 4, "c": 5}',
            {"a": ["1", "3"], "b": ["2", "4"]},
        ),
        (
            '{"a": 1, "a": 2, "b": {"x": 10, "x": 20}}',
            {"a": ["1", "2"], "x": ["10", "20"]},
        ),
        ("{}", {}),
        ('{"a": null, "a": 42}', {"a": ["None", "42"]}),
    ],
)
def test_find_duplicate_keys(json_str, expected):
    assert find_duplicate_keys(json_str) == expected


@pytest.mark.parametrize(
    "json_str",
    [
        '{"a": 1, "b": 2,}',  # trailing comma.
        '{"a": 1 "b": 2}',  # missing comma.
        '{"a": 1, "b": [1, 2,}',  # unclosed array.
    ],
)
def test_invalid_json(json_str):
    with pytest.raises(ValueError, match="Invalid JSON:"):
        find_duplicate_keys(json_str)


@pytest.mark.parametrize(
    "file_content,expected_duplicates",
    [
        ('{"a": 1, "a": 2}', {"a": ["1", "2"]}),
        ('{"x": 1, "y": 2}', {}),
        ('{"a": null, "a": 5}', {"a": ["None", "5"]}),
    ],
)
def test_check_file_valid(tmp_path, file_content, expected_duplicates):
    file = tmp_path / "test.json"
    file.write_text(file_content, encoding="utf-8")

    filename, duplicates = check_file(str(file))
    assert filename == "test.json"
    assert duplicates == expected_duplicates


def test_check_file_not_found():
    with pytest.raises(FileNotFoundError):
        check_file("nonexistent_file.json")


if __name__ == "__main__":
    pytest.main()
