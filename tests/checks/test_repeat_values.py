# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the repeat_values.py.
"""

from typing import Dict

import pytest

from i18n_check.check.repeat_values import (
    analyze_and_generate_repeat_value_report,
    get_repeat_value_counts,
    i18n_src_dict,
    repeat_values_check,
)

from ..test_utils import (
    fail_checks_src_json,
    pass_checks_src_json,
)

json_repeat_value_counts = get_repeat_value_counts(i18n_src_dict)


@pytest.mark.parametrize(
    "input_dict,expected_output",
    [
        # Empty dicts.
        ({}, {}),
        # Unicode/special characters.
        ({"key_0": "café", "key_1": "CAFÉ", "key_2": "café"}, {"café": 3}),
        (pass_checks_src_json, {}),
        # The second value will be filtered out by analyze_and_generate_repeat_value_report.
        (
            fail_checks_src_json,
            {
                "hello global!": 2,
                "hello single file!": 2,
                "hello multiple files!": 2,
                "this key is duplicated but the value is not": 2,
            },
        ),
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


def test_multiple_repeats_with_common_prefix(capsys) -> None:
    fail_result, fail_report = analyze_and_generate_repeat_value_report(
        fail_checks_src_json, get_repeat_value_counts(fail_checks_src_json)
    )
    pass_result, pass_report = analyze_and_generate_repeat_value_report(
        pass_checks_src_json, get_repeat_value_counts(pass_checks_src_json)
    )

    assert "Repeat value: 'hello global!'" in fail_report
    assert "Number of instances: 2" in fail_report
    assert (
        "Keys: i18n._global.hello_global, i18n._global.repeat_value_hello_global"
        in fail_report
    )
    assert "Suggested new key: i18n.sub_dir._global.content_reference" in fail_report

    # Result remain unchanged (not removed).
    assert fail_result == {
        "hello global!": 2,
        "hello single file!": 2,
        "hello multiple files!": 2,
    }
    assert pass_result == {}


def test_key_with_lower_suffix_ignored(capsys) -> None:
    i18n_src_dict = {
        "i18n.repeat_value_multiple_files": "Test",
        "i18n.repeat_value_single_file": "Test",
        "i18n.test_file.repeat_key_lower": "Test",
    }
    json_repeat_value_counts = {"test": 3}

    result, report = analyze_and_generate_repeat_value_report(
        i18n_src_dict, json_repeat_value_counts.copy()
    )

    assert "i18n.test_file.repeat_key_lower" not in report
    assert "Number of instances: 2" in report
    assert (
        "Keys: i18n.repeat_value_multiple_files, i18n.repeat_value_single_file"
        in report
    )
    assert "Suggested new key: i18n._global.content_reference" in report


def test_repeat_values_check_behavior(capsys) -> None:
    with pytest.raises(SystemExit):
        repeat_values_check(
            json_repeat_value_counts=get_repeat_value_counts(fail_checks_src_json),
            repeat_value_error_report="",
        )
        assert (
            "❌ repeat-values error: 1 repeat i18n value is present."
            in capsys.readouterr().out
        )

    repeat_values_check(
        json_repeat_value_counts=get_repeat_value_counts(pass_checks_src_json),
        repeat_value_error_report="",
    )
    output = capsys.readouterr().out
    assert "✅ repeat-values success: No repeat i18n values found" in output


if __name__ == "__main__":
    pytest.main()
