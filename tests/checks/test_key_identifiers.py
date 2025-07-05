# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the key_identifiers.py.
"""

from pathlib import Path

import pytest

from i18n_check.check.key_identifiers import (
    audit_i18n_keys,
    map_keys_to_files,
    report_and_correct_keys,
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

i18n_map_fail = map_keys_to_files(
    i18n_src_dict=fail_checks_json, src_directory=fail_dir
)
i18n_map_pass = map_keys_to_files(
    i18n_src_dict=pass_checks_json, src_directory=pass_dir
)

invalid_format_pass, invalid_name_pass = audit_i18n_keys(key_file_dict=i18n_map_pass)

invalid_format_fail, invalid_name_fail = audit_i18n_keys(key_file_dict=i18n_map_fail)


@pytest.mark.parametrize(
    "i18n_map, expected_output",
    [
        (len(i18n_map_fail), 9),
        (len(map_keys_to_files()), 9),
        (i18n_map_fail["i18n._global.hello_global_repeat"], ["test_file"]),
        (i18n_map_pass, {}),
        (
            map_keys_to_files()["i18n._global.incorrectly_named_key"],
            ["all_checks_fail/test_file"],
        ),
    ],
)
def test_map_keys_to_files(i18n_map, expected_output) -> None:
    """
    Test get_non_source_keys with various scenarios.
    """
    assert i18n_map == expected_output


def test_audit_i18n_keys() -> None:
    """
    Test audit_i18n_keys with various scenarios.
    """
    assert invalid_format_pass == []
    assert len(invalid_name_fail) == 6
    assert invalid_name_pass == {}
    assert invalid_format_fail == ["i18n._global.incorrectly-formatted-key"]
    assert (
        invalid_name_fail["i18n._global.hello_global_repeat"]
        == "i18n.test_file.hello_global_repeat"
    )


def test_report_and_correct_keys_fail(capsys) -> None:
    """
    Test report_and_correct_keys for the fail case.
    """
    with pytest.raises(SystemExit):
        report_and_correct_keys(invalid_format_fail, invalid_name_fail)

    output_msg = capsys.readouterr().out
    print(output_msg)
    assert "There is 1 i18n key that is not formatted correctly" in output_msg
    assert "There are 6 i18n keys that are not named correctly." in output_msg
    assert (
        "Please rename the following keys [current_key -> suggested_correction]:"
        in output_msg
    )
    assert (
        "i18n._global.hello_global_repeat -> i18n.test_file.hello_global_repeat"
        in output_msg
    )
    assert "i18n._global.hello_global_repeat" in output_msg


def test_report_and_correct_keys_pass(capsys) -> None:
    """
    Test report_and_correct_keys for the pass case.
    """
    # For pass case, it should not raise an error.
    report_and_correct_keys(invalid_format_pass, invalid_name_pass)
    pass_result = capsys.readouterr().out
    success_message = "key_identifiers success: All i18n keys are formatted and named correctly in the i18n-src file."
    assert pass_result.replace("\n", "").strip() == success_message


if __name__ == "__main__":
    pytest.main()
