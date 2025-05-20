# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the unused_keys.py.
"""

from pathlib import Path

import pytest

from i18n_check.check.unused_keys import (
    files_to_check_contents,
    find_unused_keys,
    print_unused_keys,
)
from i18n_check.utils import read_json_file

fail_checks_json = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_fail"
    / "test_i18n"
    / "test_i18n_src.json"
)
pass_checks_json = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_pass"
    / "test_i18n"
    / "test_i18n_src.json"
)

UNUSED_FAIL_KEYS = find_unused_keys(
    i18n_src_dict=read_json_file(file_path=fail_checks_json),
    files_to_check_contents=files_to_check_contents,
)
UNUSED_PASS_KEYS = find_unused_keys(
    i18n_src_dict=read_json_file(file_path=pass_checks_json),
    files_to_check_contents=files_to_check_contents,
)


def test_find_unused_keys_behavior() -> None:
    assert UNUSED_FAIL_KEYS == ["i18n._global.unused_i18n_key"]
    assert UNUSED_PASS_KEYS == []


# Note: capsys is a fixture for capturing system outputs.
def test_print_unused_keys_pass_output(capsys):
    print_unused_keys(UNUSED_PASS_KEYS)
    captured = capsys.readouterr()
    assert "unused_keys success" in captured.out


def test_print_unused_keys_fail_raises_value_error() -> None:
    with pytest.raises(ValueError) as exc_info:
        print_unused_keys(UNUSED_FAIL_KEYS)

    msg = str(exc_info.value)
    assert "There is 1 i18n key that is unused" in msg
    assert "i18n._global.unused_i18n_key" in msg
    assert "unused_keys failure" in msg


if __name__ == "__main__":
    pytest.main()
