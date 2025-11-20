# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for invalid i18n key formatting validation.
"""

import pytest

from i18n_check.check.key_formatting import (
    audit_invalid_i18n_key_formats,
    invalid_key_formats_check,
)
from i18n_check.check.key_naming import (
    map_keys_to_files,
)
from i18n_check.utils import PATH_SEPARATOR

from ..test_utils import (
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
    assert invalid_format_pass == []
    assert invalid_format_fail == ["i18n.test_file.incorrectly-formatted-key"]


def test_invalid_keys_check_fail(capsys) -> None:
    """
    Test invalid_key_formats_check for the fail case with formatting errors.
    """
    with pytest.raises(SystemExit):
        invalid_key_formats_check(
            invalid_keys_by_format=invalid_format_fail,
            all_checks_enabled=False,
        )

    output_msg = capsys.readouterr().out

    assert "There is 1 i18n key that is not formatted correctly" in output_msg


def test_invalid_keys_check_pass(capsys) -> None:
    """
    Test invalid_key_formats_check for the pass case.
    """
    # For pass case, it should not raise an error.
    invalid_key_formats_check(
        invalid_keys_by_format=invalid_format_pass,
        all_checks_enabled=False,
    )
    pass_result = capsys.readouterr().out

    assert "✅ key-formatting success: " in pass_result.replace("\n", "").strip()
    assert (
        " All i18n keys are formatted correctly"
        in pass_result.replace("\n", "").strip()
    )
    assert "i18n-src file." in pass_result.replace("\n", "").strip()


if __name__ == "__main__":
    pytest.main()
