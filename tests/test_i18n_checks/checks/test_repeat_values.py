# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for the repeat_values.py.
"""

from typing import Dict

import pytest

from i18n_check.check.repeat_values import (
    analyze_and_suggest_keys,
    get_repeat_value_counts,
    validate_repeats,
)


@pytest.mark.parametrize(
    "input_dict,expected_output",
    [
        # Empty dicts.
        ({}, {}),
        # No repeated values
        ({"key1": "Hello", "key2": "World", "key3": "Python"}, {}),
        # All values repeated
        ({"a": "x", "b": "x", "c": "x"}, {"x": 3}),
        # Case sensitivity and punctuation variations.
        (
            {
                "key1": "apple",
                "key2": "APPLE",
                "key3": "banana",
                "key4": "BANANA!",
                "key5": "cherry",
                "key6": "apple",
            },
            {"apple": 3},
        ),
        # Mixed types (including non-string values).
        (
            {"key1": "Test", "key2": "test", "key3": 123, "key4": 123},
            {"test": 2, 123: 2},
        ),
        # Non-hashable types filtered out.
        ({"key1": "test", "key2": ["list", "ignored"], "key3": "test"}, {"test": 2}),
        # Unicode/special characters.
        ({"key1": "café", "key2": "CAFÉ", "key3": "café"}, {"café": 3}),
    ],
)
def test_get_repeat_value_counts(
    input_dict: Dict[str, str], expected_output: Dict[str, int]
):
    """Test get_repeat_value_counts with various scenarios."""
    result = get_repeat_value_counts(input_dict)
    assert result == expected_output


def test_multiple_repeats_with_common_prefix(capsys):
    i18n_src_dict = {
        "foo.bar.one": "Test.",
        "foo.bar.two": "test",
        "foo.bar_lower": "test",
    }
    json_repeat_value_counts = {"test": 3}
    result = analyze_and_suggest_keys(i18n_src_dict, json_repeat_value_counts.copy())

    captured = capsys.readouterr()
    assert "Repeat value: 'test'" in captured.out
    assert "foo.bar.one" in captured.out
    assert "foo.bar.two" in captured.out
    assert "Suggested new key: foo.bar._global.IDENTIFIER_KEY" in captured.out

    # Result remain unchanged (not removed).
    assert result == {"test": 3}


def test_single_repeat_removed():
    i18n_src_dict = {
        "key1": "Hello!",
    }
    json_repeat_value_counts = {"hello": 1}
    result = analyze_and_suggest_keys(i18n_src_dict, json_repeat_value_counts.copy())

    # Single lowercase value should be removed.
    assert result == {}


def test_key_with_lower_suffix_ignored(capsys):
    i18n_src_dict = {
        "one.lower": "Test",
        "two.lower": "Test",
        "three_lower": "Test",
    }
    json_repeat_value_counts = {"test": 3}

    result = analyze_and_suggest_keys(i18n_src_dict, json_repeat_value_counts.copy())

    captured = capsys.readouterr()
    assert "three_lower" not in captured.out
    assert "Suggested new key" in captured.out
    assert result == {"test": 3}


def test_no_common_prefix(capsys):
    i18n_src_dict = {
        "one": "Repeat",
        "two": "Repeat",
    }
    json_repeat_value_counts = {"repeat": 2}

    result = analyze_and_suggest_keys(i18n_src_dict, json_repeat_value_counts.copy())

    captured = capsys.readouterr()
    assert "Suggested new key: _global.IDENTIFIER_KEY" in captured.out
    assert result == {"repeat": 2}


def test_validate_repeats_with_values():
    # One repeat.
    with pytest.raises(
        ValueError, match=r"repeat_values failure: 1 repeat i18n value is present"
    ):
        validate_repeats({"hello": 2})

    # Multiple repeats.
    with pytest.raises(
        ValueError, match=r"repeat_values failure: 2 repeat i18n values are present"
    ):
        validate_repeats({"hello": 2, "world": 3})


def test_validate_repeats_without_values(capsys):
    validate_repeats({})
    captured = capsys.readouterr()
    assert "repeat_values success: No repeat i18n values found" in captured.out


if __name__ == "__main__":
    pytest.main()
