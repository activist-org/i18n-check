# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the missing_keys.py.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from i18n_check.check.missing_keys import (
    add_missing_keys_interactively,
    get_missing_keys_by_locale,
    missing_keys_check_and_fix,
    report_missing_keys,
)
from i18n_check.utils import read_json_file

from ..test_utils import (
    checks_fail_json_dir,
    checks_pass_json_dir,
    fail_checks_locale_json,
    fail_checks_src_json,
    pass_checks_src_json,
)

missing_keys_fail = get_missing_keys_by_locale(
    i18n_src_dict=fail_checks_src_json,
    i18n_directory=checks_fail_json_dir,
    locales_to_check=[],
)

missing_keys_pass = get_missing_keys_by_locale(
    i18n_src_dict=pass_checks_src_json,
    i18n_directory=checks_pass_json_dir,
    locales_to_check=[],
)


def test_get_missing_keys_by_locale_fail() -> None:
    """
    Test get_missing_keys_by_locale for the failing test case.
    """
    assert "test_i18n_locale" in missing_keys_fail

    missing_keys, percentage = missing_keys_fail["test_i18n_locale"]

    # The failing locale file has some keys missing and some with empty values.
    expected_missing = [
        "i18n._global.repeat_key",
        "i18n._global.repeat_value_hello_global",
        "i18n._global.unused_i18n_key",
        "i18n.repeat_value_multiple_files",
        "i18n.repeat_value_multiple_files_repeat",
        "i18n.repeat_value_single_file",
        "i18n.repeat_value_single_file_repeat",
        "i18n.sub_dir._global.hello_sub_dir",
        "i18n.sub_dir_first_file.hello_sub_dir_first_file",  # has empty value
        "i18n.sub_dir_second_file.hello_sub_dir_second_file",
        "i18n.test_file.hello_test_file",  # has empty value
        "i18n.test_file.incorrectly-formatted-key",
        "i18n.test_file.nested_example",
        "i18n.test_file.repeat_key_lower",
        "i18n.unused_keys.ignore.unused_i18n_key",
        "i18n.wrong_identifier_path.content_reference",
    ]

    assert set(missing_keys) == set(expected_missing)
    assert percentage > 70  # most keys are missing


def test_get_missing_keys_by_locale_pass() -> None:
    """
    Test get_missing_keys_by_locale for the passing test case.
    """
    # All keys should be present in the passing locale file.
    assert missing_keys_pass == {}


def test_get_missing_keys_by_locale_with_specific_locales() -> None:
    """
    Test get_missing_keys_by_locale when specific locales are specified.
    """
    # Test with a locale that doesn't exist.
    result = get_missing_keys_by_locale(
        i18n_src_dict=pass_checks_src_json,
        i18n_directory=checks_pass_json_dir,
        locales_to_check=["not_a_locale.json"],
    )
    assert result == {}

    # Test with the existing locale file.
    result = get_missing_keys_by_locale(
        i18n_src_dict=pass_checks_src_json,
        i18n_directory=checks_pass_json_dir,
        locales_to_check=["test_i18n_locale"],
    )
    assert result == {}


def test_report_missing_keys_pass(capsys) -> None:
    """
    Test report_missing_keys for the passing case.
    """
    report_missing_keys(missing_keys_pass)
    captured = capsys.readouterr()
    assert "missing-keys success" in captured.out
    assert "All checked locale files have all required keys" in captured.out


def test_report_missing_keys_fail(capsys) -> None:
    """
    Test report_missing_keys for the failing case.
    """
    with pytest.raises(SystemExit):
        report_missing_keys(missing_keys_fail)

    output_msg = capsys.readouterr().out
    assert "missing-keys error:" in output_msg
    assert "test_i18n_locale" in output_msg
    assert "Summary of missing keys by locale:" in output_msg
    assert "%" in output_msg


def test_empty_string_values_detected() -> None:
    """
    Test that keys with empty string values are detected as missing.
    """
    # In the failing test frontend, these keys have empty values.
    missing_keys, _ = missing_keys_fail["test_i18n_locale"]

    assert "i18n.sub_dir_first_file.hello_sub_dir_first_file" in missing_keys
    assert "i18n.test_file.hello_test_file" in missing_keys


def test_get_missing_keys_by_locale_with_empty_source(tmp_path: Path) -> None:
    """
    When the source i18n dict is empty, the function should report no missing keys
    and the missing percentage should be 0.0 by definition.
    """
    # Create a temporary i18n directory with a dummy locale file.
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    # Create a locale file with some keys - none should be considered missing.
    locale_file = i18n_dir / "locale.json"
    locale_file.write_text(
        '{\n  "some.key": "Some value",\n  "another.key": ""\n}\n', encoding="utf-8"
    )

    result = get_missing_keys_by_locale(
        i18n_src_dict={},
        i18n_directory=i18n_dir,
        locales_to_check=[],
    )

    assert result == {}


def test_add_missing_keys_interactively_nonexistent_locale(tmp_path: Path) -> None:
    """
    Test that add_missing_keys_interactively exits when locale file doesn't exist.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    src_file = i18n_dir / "src.json"
    src_file.write_text('{"key_0": "value_0"}', encoding="utf-8")

    with pytest.raises(SystemExit):
        add_missing_keys_interactively(
            locale="nonexistent",
            i18n_src_dict={"key_0": "value_0"},
            i18n_directory=i18n_dir,
        )


def test_add_missing_keys_interactively_no_missing_keys(tmp_path: Path, capsys) -> None:
    """
    Test that add_missing_keys_interactively handles the case when all keys are present.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    locale_file = i18n_dir / "locale.json"
    locale_file.write_text(
        '{"key_0": "locale_value_0", "key_1": "locale_value_1"}', encoding="utf-8"
    )

    add_missing_keys_interactively(
        locale="locale",
        i18n_src_dict={"key_0": "value_0", "key_1": "value_1"},
        i18n_directory=i18n_dir,
    )

    captured = capsys.readouterr()
    assert "All keys are present" in captured.out


@patch("i18n_check.check.missing_keys.Prompt.ask")
def test_add_missing_keys_interactively_with_translations(
    mock_prompt, tmp_path: Path
) -> None:
    """
    Test that add_missing_keys_interactively adds translations and sorts keys.
    """
    # Mock user input for all translations all except the first being skipped automatically or explicitly.
    mock_prompt.side_effect = ["Locale translation"] + [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]

    add_missing_keys_interactively(
        locale="test_i18n_locale",
        i18n_src_dict=fail_checks_src_json,
        i18n_directory=checks_fail_json_dir,
    )

    updated_fail_checks_locale_json = read_json_file(
        file_path=checks_fail_json_dir / "test_i18n_locale.json"
    )

    expected_content = {
        "i18n._global.hello_global": "Hello, global in another language!",
        "i18n._global.not_in_i18n_src": "A reference that can't be used.",
        "i18n._global.repeat_value_hello_global": "Locale translation",
        "i18n.sub_dir_first_file.hello_sub_dir_first_file": "",
        "i18n.test_file.form_button_aria_label": ".انقر هنا لتقديم النموذج",
        "i18n.test_file.fox_image_alt_text": "الثعلب البني السريع يقفز فوق الكلب الكسول",
        "i18n.test_file.hello_test_file": "",
    }

    assert updated_fail_checks_locale_json == expected_content

    # Revert change to test_i18n_locale.json.
    with open(
        checks_fail_json_dir / "test_i18n_locale.json", "w", encoding="utf-8"
    ) as f:
        json.dump(fail_checks_locale_json, f, indent=2, ensure_ascii=False)
        f.write("\n")


@patch("i18n_check.check.missing_keys.Prompt.ask")
def test_add_missing_keys_interactively_keyboard_interrupt(
    mock_prompt, tmp_path: Path
) -> None:
    """
    Test that add_missing_keys_interactively handles KeyboardInterrupt gracefully.
    """
    mock_prompt.side_effect = KeyboardInterrupt()

    with pytest.raises(SystemExit):
        add_missing_keys_interactively(
            locale="test_i18n_locale",
            i18n_src_dict=fail_checks_src_json,
            i18n_directory=checks_fail_json_dir,
        )


def test_missing_keys_check_and_fix_no_locale(capsys) -> None:
    """
    Test that missing_keys_check_and_fix works without locale (normal check mode).
    """
    missing_keys_check_and_fix(
        fix_locale=None,
        i18n_src_dict=pass_checks_src_json,
        i18n_directory=checks_pass_json_dir,
        locales_to_check=[],
    )

    captured = capsys.readouterr()
    assert "missing-keys success" in captured.out


@patch("i18n_check.check.missing_keys.add_missing_keys_interactively")
def test_missing_keys_check_and_fix_with_locale(mock_add_function) -> None:
    """
    Test that missing_keys_check_and_fix calls interactive function when locale is provided.
    """
    missing_keys_check_and_fix(
        fix_locale="de",
        i18n_src_dict={"key_0": "value_0"},
        i18n_directory=Path("/tmp"),
        locales_to_check=[],
    )

    # Verify the interactive function was called with correct parameters.
    mock_add_function.assert_called_once_with(
        locale="de",
        i18n_src_dict={"key_0": "value_0"},
        i18n_directory=Path("/tmp"),
    )


if __name__ == "__main__":
    pytest.main()
