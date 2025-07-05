# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the invalid_keys.py.
"""

import re
from pathlib import Path

import pytest

from i18n_check.check.invalid_keys import (
    get_used_i18n_keys,
    validate_i18n_keys,
)
from i18n_check.utils import read_json_file

fail_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_fail"
)

pass_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_pass"
)
fail_checks_json = read_json_file(
    file_path=fail_dir / "test_i18n" / "test_i18n_src.json"
)
pass_checks_json = read_json_file(
    file_path=pass_dir / "test_i18n" / "test_i18n_src.json"
)


i18n_used_fail = get_used_i18n_keys(
    i18n_src_dict=fail_checks_json, src_directory=fail_dir
)
i18n_used_pass = get_used_i18n_keys(
    i18n_src_dict=pass_checks_json, src_directory=pass_dir
)
all_i18n_used = get_used_i18n_keys()


@pytest.mark.parametrize(
    "used_keys, expected_output",
    [
        (len(i18n_used_pass), 0),
        (len(i18n_used_fail), 8),
        (len(all_i18n_used), 8),
        (
            i18n_used_fail,
            {
                "i18n.sub_dir._global.hello_sub_dir",
                "i18n._global.hello_global",
                "i18n.sub_dir.second_file.hello_sub_dir_second_file",
                "i18n._global.nested_example",
                "i18n.test_file.hello_test_file",
                "i18n._global.hello_global_repeat_value",
                "i18n._global.incorrectly_named_key",
                "i18n._global.incorrectly-formatted-key",
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
    assert all_i18n_used >= i18n_used_fail
    assert all_i18n_used >= i18n_used_pass


def test_validate_fail_i18n_keys(capsys) -> None:
    """
    Test validate_i18n_keys for the fail case.
    """
    with pytest.raises(SystemExit):
        validate_i18n_keys(
            all_used_i18n_keys=i18n_used_fail, i18n_src_dict=fail_checks_json
        )

    msg = capsys.readouterr().out.replace("\n", "")
    assert "Please check the validity of the following key:" in msg
    assert " There is 1 i18n key that is not in the i18n source file." in msg
    assert "i18n._global.hello_global_repeat_value" in msg


def test_validate_pass_i18n_keys(capsys) -> None:
    """
    Test validate_i18n_keys for the pass case.
    """
    # For pass case, it should not raise an error.
    validate_i18n_keys(
        all_used_i18n_keys=i18n_used_pass, i18n_src_dict=pass_checks_json
    )
    pass_result = capsys.readouterr().out
    cleaned_pass_result = re.sub(r"\x1b\[.*?m", "", pass_result).strip()

    success_message = "invalid_keys success: All i18n keys that are used in the project are in the i18n source file."
    assert success_message in cleaned_pass_result.replace("\n", " ")


if __name__ == "__main__":
    pytest.main()
