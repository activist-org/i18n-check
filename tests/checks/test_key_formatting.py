# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for invalid i18n key formatting validation.
"""

import pytest

from i18n_check.check.key_formatting import (
    audit_invalid_i18n_key_formats,
    invalid_key_formats_check_and_fix,
)
from i18n_check.check.key_naming import (
    map_keys_to_files,
)
from i18n_check.utils import PATH_SEPARATOR, replace_text_in_file

from ..test_utils import (
    fail_checks_src_json_path,
    fail_checks_test_file_path,
    i18n_map_fail,
    i18n_map_pass,
)

invalid_format_fail = audit_invalid_i18n_key_formats(
    key_file_dict=i18n_map_fail, keys_to_ignore_regex=""
)

invalid_format_pass = audit_invalid_i18n_key_formats(
    key_file_dict=i18n_map_pass, keys_to_ignore_regex=""
)


@pytest.mark.parametrize(
    "i18n_map, expected_output",
    [
        (len(i18n_map_fail), 15),
        (len(map_keys_to_files()), 15),
        (
            set(i18n_map_fail["i18n._global.repeat_value_hello_global"]),
            {
                "test_file",
                f"sub_dir{PATH_SEPARATOR}sub_dir_first_file",
                f"sub_dir{PATH_SEPARATOR}sub_dir_second_file",
            },
        ),
        (
            {k: sorted(v) for k, v in i18n_map_pass.items()},
            {
                "i18n._global.hello_global": [
                    f"sub_dir{PATH_SEPARATOR}sub_dir_first_file",
                    f"sub_dir{PATH_SEPARATOR}sub_dir_second_file",
                    "test_file",
                ],
                "i18n.sub_dir._global.hello_sub_dir": [
                    f"sub_dir{PATH_SEPARATOR}sub_dir_first_file",
                    f"sub_dir{PATH_SEPARATOR}sub_dir_second_file",
                ],
                "i18n.sub_dir_first_file.hello_sub_dir_first_file": [
                    f"sub_dir{PATH_SEPARATOR}sub_dir_first_file"
                ],
                "i18n.sub_dir_second_file.hello_sub_dir_second_file": [
                    f"sub_dir{PATH_SEPARATOR}sub_dir_second_file"
                ],
                "i18n.test_file.form_button_aria_label": ["test_file"],
                "i18n.test_file.hello_test_file": ["test_file"],
                "i18n.test_file.fox_image_alt_text": ["test_file"],
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


def test_audit_invalid_i18n_keys_formatting() -> None:
    """
    Test audit_invalid_i18n_key_formats for key formatting validation.
    """
    assert invalid_format_pass == {}
    assert invalid_format_fail == {
        "i18n.test_file.incorrectly-formatted-key": "i18n.test_file.incorrectly_formatted_key"
    }


def test_invalid_key_formats_check_and_fix_fail(capsys) -> None:
    """
    Test invalid_key_formats_check_and_fix for the fail case with formatting errors.
    """
    with pytest.raises(SystemExit):
        invalid_key_formats_check_and_fix(
            invalid_keys_by_format=invalid_format_fail,
            all_checks_enabled=False,
            fix=False,
        )

    output_msg = capsys.readouterr().out

    assert "There is 1 i18n key that is not formatted correctly" in output_msg
    # Check both parts are in the output (they may be on separate lines).
    assert "i18n.test_file.incorrectly-formatted-key" in output_msg
    assert "i18n.test_file.incorrectly_formatted_key" in output_msg
    assert "->" in output_msg
    assert "💡 Tip: You can automatically fix invalid key formats" in output_msg


def test_invalid_key_formats_check_and_fix_pass(capsys) -> None:
    """
    Test invalid_key_formats_check_and_fix for the pass case.
    """
    # For pass case, it should not raise an error.
    invalid_key_formats_check_and_fix(
        invalid_keys_by_format=invalid_format_pass,
        all_checks_enabled=False,
        fix=False,
    )
    pass_result = capsys.readouterr().out

    assert "✅ key-formatting success: " in pass_result.replace("\n", "").strip()
    assert (
        " All i18n keys are formatted correctly"
        in pass_result.replace("\n", "").strip()
    )
    assert "i18n-src file." in pass_result.replace("\n", " ").strip()


def test_invalid_key_formats_check_and_fix_with_fix(
    capsys, tmp_path, monkeypatch
) -> None:
    """
    Test invalid_key_formats_check_and_fix with fix=True to ensure it attempts to fix issues.
    """
    invalid_key_formats_check_and_fix(
        invalid_keys_by_format={},
        all_checks_enabled=False,
        fix=True,
    )

    pass_result = capsys.readouterr().out
    assert "✅ key-formatting success" in pass_result


def test_invalid_key_formats_check_and_fix_fail_fix_mode(capsys):
    """
    Test invalid_key_formats_check_and_fix in fix mode for naming errors.
    """
    with pytest.raises(SystemExit):
        invalid_key_formats_check_and_fix(
            invalid_keys_by_format={
                "i18n.test_file.incorrectly-formatted-key": "i18n.test_file.incorrectly_formatted_key"
            },
            all_checks_enabled=False,
            fix=True,
        )

    output = capsys.readouterr().out
    assert "--fix (-f) flag" not in output
    assert "✨ Replaced 'i18n.test_file.incorrectly-formatted-key'" in output
    assert "'i18n.test_file.incorrectly_formatted_key'" in output

    # Return to old state before string replacement in tests:
    replace_text_in_file(
        path=fail_checks_src_json_path,
        old="i18n.test_file.incorrectly_formatted_key",
        new="i18n.test_file.incorrectly-formatted-key",
    )
    replace_text_in_file(
        path=fail_checks_test_file_path,
        old="i18n.test_file.incorrectly_formatted_key",
        new="i18n.test_file.incorrectly-formatted-key",
    )


if __name__ == "__main__":
    pytest.main()
