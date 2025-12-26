# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the unused_keys.py.
"""

import pytest

from i18n_check.check.unused_keys import (
    files_to_check_contents,
    find_unused_keys,
    unused_keys_check,
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
    assert set(UNUSED_FAIL_KEYS) == {
        "i18n._global.unused_i18n_key",
        "i18n.repeat_value_multiple_files_repeat",
        "i18n.repeat_value_single_file_repeat",
    }
    assert UNUSED_PASS_KEYS == []


def test_unused_keys_check_pass_output(capsys):
    unused_keys_check(UNUSED_PASS_KEYS)
    output = capsys.readouterr().out
    assert "unused-keys success" in output


def test_unused_keys_check_fail_raises_value_error(capsys) -> None:
    with pytest.raises(SystemExit):
        unused_keys_check(UNUSED_FAIL_KEYS)

    output = capsys.readouterr().out
    assert (
        "❌ unused-keys error: There are 3 unused i18n keys in the test_i18n_src.json"
        in output
    )
    assert "i18n source file" in output
    assert "i18n._global.unused_i18n_key" in output


if __name__ == "__main__":
    pytest.main()
