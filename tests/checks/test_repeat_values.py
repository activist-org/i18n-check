# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the repeat_values.py.
"""

from pathlib import Path
from typing import Dict

import pytest

from i18n_check.check.repeat_values import (
    analyze_and_suggest_keys,
    get_repeat_value_counts,
    i18n_src_dict,
    validate_repeat_values,
)
from i18n_check.utils import read_json_file

# repeat values across the repo
json_repeat_value_counts = get_repeat_value_counts(i18n_src_dict)

fail_checks_json = read_json_file(
    file_path=Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_fail"
    / "test_i18n"
    / "test_i18n_src.json"
)
pass_checks_json = read_json_file(
    file_path=Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_pass"
    / "test_i18n"
    / "test_i18n_src.json"
)


@pytest.mark.parametrize(
    "input_dict,expected_output",
    [
        # Empty dicts.
        ({}, {}),
        # Unicode/special characters.
        ({"key1": "café", "key2": "CAFÉ", "key3": "café"}, {"café": 3}),
        (pass_checks_json, {}),
        (fail_checks_json, {"hello global!": 2}),
    ],
)
def test_get_repeat_value_counts(
    input_dict: Dict[str, str], expected_output: Dict[str, int]
) -> None:
    """
    Test get_repeat_value_counts with various scenarios.
    """
    result = get_repeat_value_counts(input_dict)
    assert result == expected_output


# Note: capsys is a fixture for capturing system outputs.
def test_multiple_repeats_with_common_prefix(capsys) -> None:
    fail_result = analyze_and_suggest_keys(
        fail_checks_json, get_repeat_value_counts(fail_checks_json)
    )
    pass_result = analyze_and_suggest_keys(
        pass_checks_json, get_repeat_value_counts(pass_checks_json)
    )

    captured = capsys.readouterr()
    assert "Repeat value: 'hello global!'" in captured.out
    assert "Number of instances: : 2" in captured.out
    assert "Suggested new key: i18n._global.IDENTIFIER_KEY" in captured.out

    # Result remain unchanged (not removed).
    assert fail_result == {"hello global!": 2}
    assert pass_result == {}


# Note: capsys is a fixture for capturing system outputs.
def test_key_with_lower_suffix_ignored(capsys) -> None:
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


# Note: capsys is a fixture for capturing system outputs.
def test_validate_repeat_values_behavior(capsys) -> None:
    with pytest.raises(
        ValueError, match=r"repeat_values failure: 1 repeat i18n value is present."
    ):
        validate_repeat_values(get_repeat_value_counts(fail_checks_json))

    validate_repeat_values(get_repeat_value_counts(pass_checks_json))
    captured = capsys.readouterr()
    assert "repeat_values success: No repeat i18n values found" in captured.out


if __name__ == "__main__":
    pytest.main()
