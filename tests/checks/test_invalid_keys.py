# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the invalid_keys.py.
"""

from pathlib import Path

import pytest

from i18n_check.check.invalid_keys import (
    audit_i18n_keys,
    map_keys_to_files,
    report_and_correct_keys,
)
from i18n_check.utils import read_json_file, replace_text_in_file

fail_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_fail"
)
fail_checks_json = read_json_file(
    file_path=fail_dir / "test_i18n" / "test_i18n_src.json"
)
i18n_map_fail = map_keys_to_files(
    i18n_src_dict=fail_checks_json, src_directory=fail_dir
)
fail_checks_json_path = fail_dir / "test_i18n" / "test_i18n_src.json"
fail_checks_test_file_path = fail_dir / "test_file.ts"

invalid_format_fail, invalid_name_fail = audit_i18n_keys(
    key_file_dict=i18n_map_fail, keys_to_ignore_regex=""
)

pass_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_pass"
)
pass_checks_json = read_json_file(
    file_path=pass_dir / "test_i18n" / "test_i18n_src.json"
)
i18n_map_pass = map_keys_to_files(
    i18n_src_dict=pass_checks_json, src_directory=pass_dir
)

invalid_format_pass, invalid_name_pass = audit_i18n_keys(
    key_file_dict=i18n_map_pass, keys_to_ignore_regex=""
)


@pytest.mark.parametrize(
    "i18n_map, expected_output",
    [
        (len(i18n_map_fail), 15),
        (len(map_keys_to_files()), 15),
        (
            set(i18n_map_fail["i18n._global.hello_global_repeat_value"]),
            {"test_file", "sub_dir/sub_dir_first_file", "sub_dir/sub_dir_second_file"},
        ),
        (
            {k: sorted(v) for k, v in i18n_map_pass.items()},
            {
                "i18n._global.hello_global": [
                    "sub_dir/sub_dir_first_file",
                    "sub_dir/sub_dir_second_file",
                    "test_file",
                ],
                "i18n.sub_dir._global.hello_sub_dir": [
                    "sub_dir/sub_dir_first_file",
                    "sub_dir/sub_dir_second_file",
                ],
                "i18n.sub_dir_first_file.hello_sub_dir_first_file": [
                    "sub_dir/sub_dir_first_file"
                ],
                "i18n.sub_dir_second_file.hello_sub_dir_second_file": [
                    "sub_dir/sub_dir_second_file"
                ],
                "i18n.test_file.form_button_aria_label": ["test_file"],
                "i18n.test_file.hello_test_file": ["test_file"],
            },
        ),
        (
            map_keys_to_files()["i18n.wrong_identifier_path.content_reference"],
            ["test_file"],
        ),
    ],
)
def test_map_keys_to_files(i18n_map, expected_output) -> None:
    """
    Test get_non_source_keys with various scenarios.
    """
    assert i18n_map == expected_output


def test_audit_i18n_keys() -> None:
    """
    Test audit_i18n_keys with various scenarios.
    """
    assert invalid_format_pass == []
    assert len(invalid_name_fail) == 4
    assert invalid_name_pass == {}
    assert invalid_format_fail == ["i18n.test_file.incorrectly-formatted-key"]
    assert (
        invalid_name_fail["i18n.wrong_identifier_path.content_reference"]
        == "i18n.test_file.content_reference"
    )


def test_report_and_correct_keys_fail(capsys) -> None:
    """
    Test report_and_correct_keys for the fail case.
    """
    with pytest.raises(SystemExit):
        report_and_correct_keys(invalid_format_fail, invalid_name_fail)

    output_msg = capsys.readouterr().out

    assert "There is 1 i18n key that is not formatted correctly" in output_msg
    assert "There are 4 i18n keys that are not named correctly." in output_msg
    assert (
        "Please rename the following keys [current_key -> suggested_correction]:"
        in output_msg
    )
    assert "i18n.wrong_identifier_path.content_reference" in output_msg
    assert "i18n.test_file.content_reference" in output_msg


def test_report_and_correct_keys_pass(capsys) -> None:
    """
    Test report_and_correct_keys for the pass case.
    """
    # For pass case, it should not raise an error.
    report_and_correct_keys(invalid_format_pass, invalid_name_pass)
    pass_result = capsys.readouterr().out
    success_message = "✅ invalid_keys success: All i18n keys are formatted and named correctly in the i18n-src file."
    assert pass_result.replace("\n", "").strip() == success_message


def test_report_and_correct_keys_fail_with_tip(capsys):
    with pytest.raises(SystemExit):
        report_and_correct_keys(invalid_format_fail, invalid_name_fail)

    output = capsys.readouterr().out
    assert "not formatted correctly" in output
    assert "not named correctly" in output
    assert "i18n.wrong_identifier_path.content_reference" in output
    assert "i18n.test_file.content_reference" in output
    assert "--fix (-f) flag" in output


def test_report_and_correct_keys_fail_fix_mode(capsys):
    with pytest.raises(SystemExit):
        report_and_correct_keys(invalid_format_fail, invalid_name_fail, fix=True)

    output = capsys.readouterr().out
    assert "--fix (-f) flag" not in output
    assert "✨ Replaced 'i18n.wrong_identifier_path.content_reference'" in output
    assert "'i18n.test_file.content_reference'" in output

    # Return to old state before string replacement:
    replace_text_in_file(
        path=fail_checks_json_path,
        old="i18n.test_file.content_reference",
        new="i18n.wrong_identifier_path.content_reference",
    )
    replace_text_in_file(
        path=fail_checks_test_file_path,
        old="i18n.test_file.content_reference",
        new="i18n.wrong_identifier_path.content_reference",
    )


def test_audit_i18n_keys_regex_ignore() -> None:
    """
    Test that keys matching regex pattern are ignored during validation.
    """
    test_key_file_dict = {
        "i18n.legacy.old_component.title": ["legacy/old_component.ts"],
        "i18n.temp.test_component.label": ["temp/test_component.ts"],
        "i18n.valid.component.title": ["src/component.ts"],
        "i18n.temp.another_test.message": ["temp/another_test.ts"],
        "i18n.legacy.deprecated.button": ["legacy/deprecated.ts"],
        "i18n.current.modern_component.title": ["src/modern_component.ts"],
    }

    invalid_format_all, invalid_name_all = audit_i18n_keys(
        key_file_dict=test_key_file_dict, keys_to_ignore_regex=""
    )

    invalid_format_filtered, invalid_name_filtered = audit_i18n_keys(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=r"i18n\.(legacy|temp)\.",
    )

    assert len(invalid_name_filtered) < len(invalid_name_all)

    ignored_keys = [k for k in test_key_file_dict if "legacy" in k or "temp" in k]
    for ignored_key in ignored_keys:
        assert ignored_key not in invalid_name_filtered, (
            f"Ignored key {ignored_key} should not appear in results"
        )

    invalid_format_legacy_only, invalid_name_legacy_only = audit_i18n_keys(
        key_file_dict=test_key_file_dict, keys_to_ignore_regex=r"i18n\.legacy\."
    )

    legacy_keys = [k for k in test_key_file_dict if "legacy" in k]
    temp_keys = [k for k in test_key_file_dict if "temp" in k]
    for legacy_key in legacy_keys:
        assert legacy_key not in invalid_name_legacy_only, (
            f"Legacy key {legacy_key} should be ignored"
        )

    temp_key_found = any(temp_key in invalid_name_legacy_only for temp_key in temp_keys)
    assert temp_key_found, (
        "At least one temp key should still be processed when only legacy keys are ignored"
    )


def test_audit_i18n_keys_regex_ignore_list() -> None:
    """
    Test that keys matching any regex pattern in a list are ignored during validation.
    """
    test_key_file_dict = {
        "i18n.legacy.old_component.title": ["legacy/old_component.ts"],
        "i18n.temp.test_component.label": ["temp/test_component.ts"],
        "i18n.valid.component.title": ["src/component.ts"],
        "i18n.temp.another_test.message": ["temp/another_test.ts"],
        "i18n.legacy.deprecated.button": ["legacy/deprecated.ts"],
        "i18n.deprecated.old_feature.text": ["deprecated/old_feature.ts"],
        "i18n.current.modern_component.title": ["src/modern_component.ts"],
    }

    invalid_format_empty, invalid_name_empty = audit_i18n_keys(
        key_file_dict=test_key_file_dict, keys_to_ignore_regex=[]
    )

    invalid_format_filtered, invalid_name_filtered = audit_i18n_keys(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=[
            r"i18n\.legacy\.",
            r"i18n\.temp\.",
            r"i18n\.deprecated\.",
        ],
    )

    assert len(invalid_name_filtered) < len(invalid_name_empty)

    ignored_keys = [
        k
        for k in test_key_file_dict
        if any(pattern in k for pattern in ["legacy", "temp", "deprecated"])
    ]
    for ignored_key in ignored_keys:
        assert ignored_key not in invalid_name_filtered, (
            f"Ignored key {ignored_key} should not appear in results"
        )

    invalid_format_single, invalid_name_single = audit_i18n_keys(
        key_file_dict=test_key_file_dict, keys_to_ignore_regex=[r"i18n\.legacy\."]
    )

    legacy_keys = [k for k in test_key_file_dict if "legacy" in k]
    for legacy_key in legacy_keys:
        assert legacy_key not in invalid_name_single, (
            f"Legacy key {legacy_key} should be ignored"
        )

    temp_keys = [k for k in test_key_file_dict if "temp" in k]
    deprecated_keys = [
        k for k in test_key_file_dict if "deprecated" in k and "legacy" not in k
    ]

    temp_or_deprecated_found = any(
        key in invalid_name_single for key in temp_keys + deprecated_keys
    )
    assert temp_or_deprecated_found, (
        "At least one temp or deprecated key should still be processed when only legacy keys are ignored"
    )


def test_audit_i18n_keys_regex_ignore_backward_compatibility() -> None:
    """
    Test that the function still accepts string input for backward compatibility.
    """
    test_key_file_dict = {
        "i18n.legacy.old_component.title": ["legacy/old_component.ts"],
        "i18n.temp.test_component.label": ["temp/test_component.ts"],
        "i18n.valid.component.title": ["src/component.ts"],
    }

    invalid_format_string, invalid_name_string = audit_i18n_keys(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=r"i18n\.(legacy|temp)\.",
    )

    invalid_format_list, invalid_name_list = audit_i18n_keys(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=[r"i18n\.(legacy|temp)\."],
    )

    assert invalid_format_string == invalid_format_list
    assert invalid_name_string == invalid_name_list


def test_audit_i18n_keys_regex_ignore_empty_patterns() -> None:
    """
    Test that empty patterns in the list are handled correctly.
    """
    test_key_file_dict = {
        "i18n.legacy.old_component.title": ["legacy/old_component.ts"],
        "i18n.temp.test_component.label": ["temp/test_component.ts"],
        "i18n.valid.component.title": ["src/component.ts"],
    }

    invalid_format_mixed, invalid_name_mixed = audit_i18n_keys(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=["", r"i18n\.legacy\.", "", r"i18n\.temp\.", ""],
    )

    invalid_format_clean, invalid_name_clean = audit_i18n_keys(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=[r"i18n\.legacy\.", r"i18n\.temp\."],
    )

    assert invalid_format_mixed == invalid_format_clean
    assert invalid_name_mixed == invalid_name_clean


if __name__ == "__main__":
    pytest.main()
