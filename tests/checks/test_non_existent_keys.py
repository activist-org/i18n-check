# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the nonexistent_keys.py.
"""

import re

import pytest

from i18n_check.check.nonexistent_keys import (
    get_used_i18n_keys,
    nonexistent_keys_check,
)

from ..test_utils import (
    checks_fail_dir,
    checks_pass_dir,
    fail_checks_src_json,
    pass_checks_src_json,
)

i18n_used_fail = get_used_i18n_keys(
    i18n_src_dict=fail_checks_src_json, src_directory=checks_fail_dir
)

i18n_used_pass = get_used_i18n_keys(
    i18n_src_dict=pass_checks_src_json, src_directory=checks_pass_dir
)

all_i18n_used = get_used_i18n_keys()


@pytest.mark.parametrize(
    "used_keys, expected_output",
    [
        (len(i18n_used_pass), 7),
        (len(i18n_used_fail), 15),
        (len(all_i18n_used), 15),
        (
            i18n_used_fail,
            {
                "i18n._global.hello_global",
                "i18n._global.repeat_value_hello_global",
                "i18n._global.repeat_key",
                "i18n.sub_dir._global.hello_sub_dir",
                "i18n.sub_dir_first_file.hello_sub_dir_first_file",
                "i18n.sub_dir_second_file.hello_sub_dir_second_file",
                "i18n.test_file.form_button_aria_label",
                "i18n.test_file.fox_image_alt_text",
                "i18n.test_file.incorrectly-formatted-key",
                "i18n.test_file.nested_example",
                "i18n.test_file.not_in_i18n_source_file",
                "i18n.test_file.repeat_key_lower",
                "i18n.wrong_identifier_path.content_reference",
                "i18n.repeat_value_single_file",
                "i18n.repeat_value_multiple_files",
            },
        ),
    ],
)
def test_get_used_i18n_keys(used_keys, expected_output) -> None:
    """
    Test get_used_i18n_keys with various scenarios.
    """
    assert used_keys == expected_output


def test_all_keys_include_fail_and_pass_sets():
    """
    Test that all the i18n keys used in testing contain the fail and pass keys.
    """
    assert all_i18n_used >= i18n_used_fail
    assert (
        not all_i18n_used >= i18n_used_pass
    )  # i18n.test_file.hello_test_file is correct in pass


def test_validate_fail_i18n_keys(capsys) -> None:
    """
    Test nonexistent_keys_check for the fail case.
    """
    with pytest.raises(SystemExit):
        nonexistent_keys_check(
            all_used_i18n_keys=i18n_used_fail, i18n_src_dict=fail_checks_src_json
        )

    msg = capsys.readouterr().out.replace("\n", "")
    assert "Please check the validity of the following key:" in msg
    assert " There is 1 i18n key that is not in the i18n source file." in msg
    assert "i18n.test_file.not_in_i18n_source_file" in msg


def test_validate_pass_i18n_keys(capsys) -> None:
    """
    Test nonexistent_keys_check for the pass case.
    """
    # For pass case, it should not raise an error.
    nonexistent_keys_check(
        all_used_i18n_keys=i18n_used_pass, i18n_src_dict=pass_checks_src_json
    )
    pass_result = capsys.readouterr().out
    cleaned_pass_result = re.sub(r"\x1b\[.*?m", "", pass_result).strip()

    assert "✅ nonexistent_keys success: " in cleaned_pass_result.replace("\n", "")
    assert "All i18n keys that are used in the project" in cleaned_pass_result.replace(
        "\n", ""
    )
    assert "i18n source file." in cleaned_pass_result.replace("\n", "")


if __name__ == "__main__":
    pytest.main()
