# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for invalid i18n key naming validation.
"""

import pytest

from i18n_check.check.key_naming import (
    audit_invalid_i18n_key_names,
    invalid_key_names_check_and_fix,
)
from i18n_check.utils import PATH_SEPARATOR, replace_text_in_file

from ..test_utils import (
    fail_checks_src_json_path,
    fail_checks_sub_dir_first_file_path,
    fail_checks_sub_dir_second_file_path,
    fail_checks_test_file_path,
    i18n_map_fail,
    i18n_map_pass,
)

invalid_name_fail = audit_invalid_i18n_key_names(
    key_file_dict=i18n_map_fail, keys_to_ignore_regex=""
)

invalid_name_pass = audit_invalid_i18n_key_names(
    key_file_dict=i18n_map_pass, keys_to_ignore_regex=""
)


def test_audit_invalid_i18n_keys_naming() -> None:
    """
    Test audit_invalid_i18n_key_names for key naming validation.
    """
    assert len(invalid_name_fail) == 3
    assert invalid_name_pass == {}
    assert (
        invalid_name_fail["i18n.wrong_identifier_path.content_reference"]
        == "i18n.test_file.content_reference"
    )


def test_invalid_key_names_check_and_fix_fail(capsys) -> None:
    """
    Test invalid_key_names_check_and_fix for the fail case with naming errors.
    """
    with pytest.raises(SystemExit):
        invalid_key_names_check_and_fix(
            invalid_keys_by_name=invalid_name_fail,
            all_checks_enabled=False,
        )

    output_msg = capsys.readouterr().out

    assert "There are 3 i18n keys that are not named correctly." in output_msg
    assert (
        "Please rename the following keys [current_key -> suggested_correction]:"
        in output_msg
    )
    assert "i18n.wrong_identifier_path.content_reference" in output_msg
    assert "i18n.test_file.content_reference" in output_msg


def test_invalid_key_names_check_and_fix_fail_with_tip(capsys):
    """
    Test that fix tip is shown when not in fix mode.
    """
    with pytest.raises(SystemExit):
        invalid_key_names_check_and_fix(
            invalid_keys_by_name=invalid_name_fail,
            all_checks_enabled=False,
        )

    output = capsys.readouterr().out
    assert "not named correctly" in output
    assert "i18n.wrong_identifier_path.content_reference" in output
    assert "i18n.test_file.content_reference" in output
    assert "--fix (-f) flag" in output


def test_invalid_key_names_check_and_fix_fail_fix_mode(capsys):
    """
    Test invalid_key_names_check_and_fix in fix mode for naming errors.
    """
    with pytest.raises(SystemExit):
        invalid_key_names_check_and_fix(
            invalid_keys_by_name=invalid_name_fail,
            all_checks_enabled=False,
            fix=True,
        )

    output = capsys.readouterr().out
    assert "--fix (-f) flag" not in output
    assert "✨ Replaced 'i18n.wrong_identifier_path.content_reference'" in output
    assert "'i18n.test_file.content_reference'" in output

    # Return to old state before string replacement in tests:
    replace_text_in_file(
        path=fail_checks_src_json_path,
        old="i18n.test_file.content_reference",
        new="i18n.wrong_identifier_path.content_reference",
    )
    replace_text_in_file(
        path=fail_checks_test_file_path,
        old="i18n.test_file.content_reference",
        new="i18n.wrong_identifier_path.content_reference",
    )

    # Repeat value keys as well:
    replace_text_in_file(
        path=fail_checks_src_json_path,
        old="i18n.sub_dir._global.repeat_value_multiple_files",
        new="i18n.repeat_value_multiple_files",
    )
    replace_text_in_file(
        path=fail_checks_src_json_path,
        old="i18n.test_file.repeat_value_single_file",
        new="i18n.repeat_value_single_file",
    )

    replace_text_in_file(
        path=fail_checks_test_file_path,
        old="i18n.sub_dir._global.repeat_value_multiple_files",
        new="i18n.repeat_value_multiple_files",
    )
    replace_text_in_file(
        path=fail_checks_sub_dir_first_file_path,
        old="i18n.sub_dir._global.repeat_value_multiple_files",
        new="i18n.repeat_value_multiple_files",
    )
    replace_text_in_file(
        path=fail_checks_sub_dir_second_file_path,
        old="i18n.sub_dir._global.repeat_value_multiple_files",
        new="i18n.repeat_value_multiple_files",
    )

    replace_text_in_file(
        path=fail_checks_test_file_path,
        old="i18n.test_file.repeat_value_single_file",
        new="i18n.repeat_value_single_file",
    )


def test_audit_invalid_i18n_keys_regex_ignore() -> None:
    """
    Test that keys matching regex pattern are ignored during validation.
    """
    test_key_file_dict = {
        "i18n.legacy.old_component.title": [f"legacy{PATH_SEPARATOR}old_component.ts"],
        "i18n.temp.test_component.label": [f"temp{PATH_SEPARATOR}test_component.ts"],
        "i18n.valid.component.title": [f"src{PATH_SEPARATOR}component.ts"],
        "i18n.temp.another_test.message": [f"temp{PATH_SEPARATOR}another_test.ts"],
        "i18n.legacy.deprecated.button": [f"legacy{PATH_SEPARATOR}deprecated.ts"],
        "i18n.current.modern_component.title": [
            f"src{PATH_SEPARATOR}modern_component.ts"
        ],
    }

    invalid_name_all = audit_invalid_i18n_key_names(
        key_file_dict=test_key_file_dict, keys_to_ignore_regex=""
    )

    invalid_name_filtered = audit_invalid_i18n_key_names(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=r"i18n\.(legacy|temp)\.",
    )

    assert len(invalid_name_filtered) < len(invalid_name_all)

    ignored_keys = [k for k in test_key_file_dict if "legacy" in k or "temp" in k]
    for ignored_key in ignored_keys:
        assert ignored_key not in invalid_name_filtered, (
            f"Ignored key {ignored_key} should not appear in results"
        )

    invalid_name_legacy_only = audit_invalid_i18n_key_names(
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


def test_audit_invalid_i18n_keys_regex_ignore_list() -> None:
    """
    Test that keys matching any regex pattern in a list are ignored during validation.
    """
    test_key_file_dict = {
        "i18n.legacy.old_component.title": [f"legacy{PATH_SEPARATOR}old_component.ts"],
        "i18n.temp.test_component.label": [f"temp{PATH_SEPARATOR}test_component.ts"],
        "i18n.valid.component.title": [f"src{PATH_SEPARATOR}component.ts"],
        "i18n.temp.another_test.message": [f"temp{PATH_SEPARATOR}another_test.ts"],
        "i18n.legacy.deprecated.button": [f"legacy{PATH_SEPARATOR}deprecated.ts"],
        "i18n.deprecated.old_feature.text": [
            f"deprecated{PATH_SEPARATOR}old_feature.ts"
        ],
        "i18n.current.modern_component.title": [
            f"src{PATH_SEPARATOR}modern_component.ts"
        ],
    }

    invalid_name_empty = audit_invalid_i18n_key_names(
        key_file_dict=test_key_file_dict, keys_to_ignore_regex=[]
    )

    invalid_name_filtered = audit_invalid_i18n_key_names(
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

    invalid_name_single = audit_invalid_i18n_key_names(
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


def test_audit_invalid_i18n_keys_regex_ignore_backward_compatibility() -> None:
    """
    Test that the function still accepts string input for backward compatibility.
    """
    test_key_file_dict = {
        "i18n.legacy.old_component.title": [f"legacy{PATH_SEPARATOR}old_component.ts"],
        "i18n.temp.test_component.label": [f"temp{PATH_SEPARATOR}test_component.ts"],
        "i18n.valid.component.title": [f"src{PATH_SEPARATOR}component.ts"],
    }

    invalid_name_string = audit_invalid_i18n_key_names(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=r"i18n\.(legacy|temp)\.",
    )

    invalid_name_list = audit_invalid_i18n_key_names(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=[r"i18n\.(legacy|temp)\."],
    )

    assert invalid_name_string == invalid_name_list


def test_audit_invalid_i18n_keys_regex_ignore_empty_patterns() -> None:
    """
    Test that empty patterns in the list are handled correctly.
    """
    test_key_file_dict = {
        "i18n.legacy.old_component.title": [f"legacy{PATH_SEPARATOR}old_component.ts"],
        "i18n.temp.test_component.label": [f"temp{PATH_SEPARATOR}test_component.ts"],
        "i18n.valid.component.title": [f"src{PATH_SEPARATOR}component.ts"],
    }

    invalid_name_mixed = audit_invalid_i18n_key_names(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=["", r"i18n\.legacy\.", "", r"i18n\.temp\.", ""],
    )

    invalid_name_clean = audit_invalid_i18n_key_names(
        key_file_dict=test_key_file_dict,
        keys_to_ignore_regex=[r"i18n\.legacy\.", r"i18n\.temp\."],
    )

    assert invalid_name_mixed == invalid_name_clean


if __name__ == "__main__":
    pytest.main()
