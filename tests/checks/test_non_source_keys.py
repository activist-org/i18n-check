# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the non_source_keys.py.
"""

from pathlib import Path
from typing import Dict

import pytest

from i18n_check.check.non_source_keys import (
    get_non_source_keys,
    report_non_source_keys,
)
from i18n_check.utils import read_json_file

fail_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_fail"
    / "test_i18n"
)

pass_dir = (
    Path(__file__).parent.parent.parent
    / "src"
    / "i18n_check"
    / "test_frontends"
    / "all_checks_pass"
    / "test_i18n"
)
fail_checks_json = read_json_file(file_path=fail_dir / "test_i18n_src.json")
pass_checks_json = read_json_file(file_path=pass_dir / "test_i18n_src.json")

non_source_keys_fail = get_non_source_keys(
    i18n_src_dict=fail_checks_json,
    i18n_directory=fail_dir,
)
non_source_keys_pass = get_non_source_keys(
    i18n_src_dict=pass_checks_json,
    i18n_directory=pass_dir,
)


@pytest.mark.parametrize(
    "non_source_keys,expected_output",
    [
        (non_source_keys_pass, {}),
        (
            non_source_keys_fail,
            {"test_i18n_locale.json": {"i18n._global.not_in_i18n_src"}},
        ),
        (
            get_non_source_keys(),
            {"test_i18n_locale.json": {"i18n._global.not_in_i18n_src"}},
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


def test_report_non_source_keys_pass_output(capsys):
    report_non_source_keys(non_source_keys_pass)
    captured = capsys.readouterr()
    assert "non_source_keys success" in captured.out


def test_report_non_source_keys_fail_output(capsys):
    with pytest.raises(SystemExit):
        report_non_source_keys(non_source_keys_fail)

    output_msg = capsys.readouterr().out
    assert "non_source_keys error:" in output_msg
    assert "i18n._global.not_in_i18n_src" in output_msg


if __name__ == "__main__":
    pytest.main()
