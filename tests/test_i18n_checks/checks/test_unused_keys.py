# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for the unused_keys.py.
"""

import pytest

from i18n_check.check.unused_keys import find_unused_keys, print_unused_keys


def test_find_unused_keys_detects_unused_keys():
    i18n_keys = {
        "_global.hello_global": "Hello, global!",
        "i18n.key2": "value2",
        "i18n.key3": "value3",
        "i18n.unused_key": "value4",
    }

    files = {
        "main.py": "i18n._global.hello_global \n i18n.key3",
        "utils.py": "_global.hello_global \n i18n.key2",
    }

    unused = find_unused_keys(i18n_keys, files)
    assert unused == ["i18n.unused_key"]


def test_print_unused_keys_raises_error():
    unused = ["i18n.unused_key"]
    with pytest.raises(ValueError) as exc_info:
        print_unused_keys(unused)

    assert "unused_keys failure" in str(exc_info.value)
    assert "i18n.unused_key" in str(exc_info.value)


def test_print_unused_keys_passes_on_empty_list(capfd):
    print_unused_keys([])
    captured = capfd.readouterr()
    assert "unused_keys success" in captured.out


def test_print_unused_keys_raises():
    with pytest.raises(ValueError) as exc_info:
        print_unused_keys(["key1", "key2"])
    assert "There are 2 i18n keys that are unused" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
