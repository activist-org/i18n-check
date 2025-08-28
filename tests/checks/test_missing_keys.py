# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the missing_keys.py.
"""

from pathlib import Path

import pytest

from i18n_check.check.missing_keys import (
    get_missing_keys_by_locale,
    report_missing_keys,
)
from i18n_check.utils import read_json_file

fail_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_fail"
    / "test_i18n"
)

pass_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_pass"
    / "test_i18n"
)

fail_checks_json = read_json_file(file_path=fail_dir / "test_i18n_src.json")
pass_checks_json = read_json_file(file_path=pass_dir / "test_i18n_src.json")

missing_keys_fail = get_missing_keys_by_locale(
    i18n_src_dict=fail_checks_json,
    i18n_directory=fail_dir,
    locales_to_check=[],
)
missing_keys_pass = get_missing_keys_by_locale(
    i18n_src_dict=pass_checks_json,
    i18n_directory=pass_dir,
    locales_to_check=[],
)


def test_get_missing_keys_by_locale_fail() -> None:
    """
    Test get_missing_keys_by_locale for the failing test case.
    """
    assert "test_i18n_locale.json" in missing_keys_fail

    missing_keys, percentage = missing_keys_fail["test_i18n_locale.json"]

    # The failing locale file has some keys missing and some with empty values
    expected_missing = [
        "i18n._global.hello_global_repeat_value",
        "i18n._global.repeat_key",
        "i18n._global.unused_i18n_key",
        "i18n.sub_dir._global.hello_sub_dir",
        "i18n.sub_dir_first_file.hello_sub_dir_first_file",  # Has empty value
        "i18n.sub_dir_second_file.hello_sub_dir_second_file",
        'i18n.test_file.fox_image_alt_text',
        "i18n.test_file.hello_test_file",  # Has empty value
        "i18n.test_file.incorrectly-formatted-key",
        "i18n.test_file.nested_example",
        "i18n.test_file.repeat_key_lower",
        "i18n.wrong_identifier_path.content_reference",
    ]

    assert set(missing_keys) == set(expected_missing)
    assert percentage > 70  # Most keys are missing


def test_get_missing_keys_by_locale_pass() -> None:
    """
    Test get_missing_keys_by_locale for the passing test case.
    """
    # All keys should be present in the passing locale file
    assert missing_keys_pass == {}


def test_get_missing_keys_by_locale_with_specific_locales() -> None:
    """
    Test get_missing_keys_by_locale when specific locales are specified.
    """
    # Test with a locale that doesn't exist
    result = get_missing_keys_by_locale(
        i18n_src_dict=pass_checks_json,
        i18n_directory=pass_dir,
        locales_to_check=["fr.json"],  # This file doesn't exist
    )
    assert result == {}

    # Test with the existing locale file
    result = get_missing_keys_by_locale(
        i18n_src_dict=pass_checks_json,
        i18n_directory=pass_dir,
        locales_to_check=["test_i18n_locale.json"],
    )
    assert result == {}  # Should pass


def test_report_missing_keys_pass(capsys) -> None:
    """
    Test report_missing_keys for the passing case.
    """
    report_missing_keys(missing_keys_pass)
    captured = capsys.readouterr()
    assert "missing_keys success" in captured.out
    assert "All checked locale files have all required keys" in captured.out


def test_report_missing_keys_fail(capsys) -> None:
    """
    Test report_missing_keys for the failing case.
    """
    with pytest.raises(SystemExit):
        report_missing_keys(missing_keys_fail)

    output_msg = capsys.readouterr().out
    assert "missing_keys error:" in output_msg
    assert "test_i18n_locale.json" in output_msg
    assert "Summary of missing keys by locale:" in output_msg
    assert "%" in output_msg  # Check that percentage is shown


def test_empty_string_values_detected() -> None:
    """
    Test that keys with empty string values are detected as missing.
    """
    # In the failing test frontend, these keys have empty values
    missing_keys, _ = missing_keys_fail["test_i18n_locale.json"]

    assert "i18n.sub_dir_first_file.hello_sub_dir_first_file" in missing_keys
    assert "i18n.test_file.hello_test_file" in missing_keys


def test_get_missing_keys_by_locale_with_empty_source(tmp_path: Path) -> None:
    """
    When the source i18n dict is empty, the function should report no missing keys
    and the missing percentage should be 0.0 by definition. This specifically
    exercises the code path at missing_keys.py line 89.
    """
    # Arrange: create a temporary i18n directory with a dummy locale file
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    # Create a locale file with some keys; since the source dict is empty, none
    # should be considered missing regardless of this file's content.
    locale_file = i18n_dir / "locale.json"
    locale_file.write_text(
        '{\n  "some.key": "Some value",\n  "another.key": ""\n}\n', encoding="utf-8"
    )

    # Act: call with an empty source dict
    result = get_missing_keys_by_locale(
        i18n_src_dict={},
        i18n_directory=i18n_dir,
        locales_to_check=[],
    )

    # Assert: no locale should be flagged since there are no source keys to compare
    assert result == {}


if __name__ == "__main__":
    pytest.main()
