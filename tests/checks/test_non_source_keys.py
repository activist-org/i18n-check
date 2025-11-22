# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the non_source_keys.py.
"""

from typing import Dict

import pytest

from i18n_check.check.non_source_keys import (
    get_non_source_keys,
    non_source_keys_check,
)

from ..test_utils import (
    checks_fail_json_dir,
    checks_pass_json_dir,
    fail_checks_src_json,
    pass_checks_src_json,
)

non_source_keys_fail = get_non_source_keys(
    i18n_src_dict=fail_checks_src_json,
    i18n_directory=checks_fail_json_dir,
)
non_source_keys_pass = get_non_source_keys(
    i18n_src_dict=pass_checks_src_json,
    i18n_directory=checks_pass_json_dir,
)


@pytest.mark.parametrize(
    "non_source_keys,expected_output",
    [
        (non_source_keys_pass, {}),
        (
            non_source_keys_fail,
            {
                "test_i18n_locale.json": {
                    "i18n._global.not_in_i18n_src",
                }
            },
        ),
        (
            get_non_source_keys(),
            {
                "test_i18n_locale.json": {
                    "i18n._global.not_in_i18n_src",
                }
            },
        ),
    ],
)
def test_get_non_source_keys(
    non_source_keys: Dict[str, Dict[str, str]],
    expected_output: Dict[str, Dict[str, str]],
) -> None:
    """
    Test get_non_source_keys with various scenarios.
    """
    assert non_source_keys == expected_output


def test_non_source_keys_check_pass_output(capsys):
    non_source_keys_check(non_source_keys_pass)
    output = capsys.readouterr().out
    assert "non-source-keys success" in output


def test_non_source_keys_check_fail_output(capsys):
    with pytest.raises(SystemExit):
        non_source_keys_check(non_source_keys_fail)

    output_msg = capsys.readouterr().out
    assert "non-source-keys error:" in output_msg
    assert "i18n._global.not_in_i18n_src" in output_msg


if __name__ == "__main__":
    pytest.main()
