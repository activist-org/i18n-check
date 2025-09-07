# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the unused_keys.py.
"""

import pytest

from i18n_check.check.unused_keys import (
    files_to_check_contents,
    find_unused_keys,
    print_unused_keys,
)
from i18n_check.utils import read_json_file

from ..test_utils import fail_checks_src_json_path, pass_checks_src_json_path

UNUSED_FAIL_KEYS = find_unused_keys(
    i18n_src_dict=read_json_file(file_path=fail_checks_src_json_path),
    files_to_check_contents=files_to_check_contents,
)
UNUSED_PASS_KEYS = find_unused_keys(
    i18n_src_dict=read_json_file(file_path=pass_checks_src_json_path),
    files_to_check_contents=files_to_check_contents,
)


def test_find_unused_keys_behavior() -> None:
    assert set(UNUSED_FAIL_KEYS) == set(
        [
            "i18n._global.unused_i18n_key",
            "i18n.repeat_value_multiple_files_repeat",
            "i18n.repeat_value_single_file_repeat",
        ]
    )
    assert UNUSED_PASS_KEYS == []


def test_print_unused_keys_pass_output(capsys):
    print_unused_keys(UNUSED_PASS_KEYS)
    output = capsys.readouterr().out
    assert "unused_keys success" in output


def test_print_unused_keys_fail_raises_value_error(capsys) -> None:
    with pytest.raises(SystemExit):
        print_unused_keys(UNUSED_FAIL_KEYS)

    output = capsys.readouterr().out
    assert "❌ unused_keys error: There are 3 i18n keys that are unused" in output
    assert "i18n._global.unused_i18n_key" in output


if __name__ == "__main__":
    pytest.main()
