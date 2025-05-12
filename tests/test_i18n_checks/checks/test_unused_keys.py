# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for the unused_keys.py.
"""

from pathlib import Path

import pytest

from i18n_check.check.unused_keys import (
    file_to_check_contents,
    find_unused_keys,
    print_unused_keys,
)
from i18n_check.utils import (
    read_json_file,
)

fail_checks_json = (
    Path(__file__).parent.parent.parent
    / "test_frontends"
    / "all_checks_fail"
    / "test_i18n"
    / "test_i18n_src.json"
)
pass_checks_json = (
    Path(__file__).parent.parent.parent
    / "test_frontends"
    / "all_checks_pass"
    / "test_i18n"
    / "test_i18n_src.json"
)

UNUSED_PASS_KEYS = find_unused_keys(
    read_json_file(pass_checks_json), file_to_check_contents
)
UNUSED_FAIL_KEYS = find_unused_keys(
    read_json_file(fail_checks_json), file_to_check_contents
)


def test_find_unused_keys_behavior():
    assert UNUSED_FAIL_KEYS == ["_global.unused_i18n_key"]
    assert UNUSED_PASS_KEYS == []


def test_print_unused_keys_pass_output(capfd):
    print_unused_keys(UNUSED_PASS_KEYS)
    captured = capfd.readouterr()
    assert "unused_keys success" in captured.out


def test_print_unused_keys_fail_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        print_unused_keys(UNUSED_FAIL_KEYS)
    msg = str(exc_info.value)
    assert "There is 1 i18n key that is unused" in msg
    assert "_global.unused_i18n_key" in msg
    assert "unused_keys failure" in msg


if __name__ == "__main__":
    pytest.main()
