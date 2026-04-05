# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the non_source_keys.py.
"""

from typing import Dict
from unittest.mock import patch

import pytest

from i18n_check.check.non_source_keys import (
    get_non_source_keys,
    non_source_keys_check,
    non_source_keys_check_and_delete,
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


def test_non_source_keys_check_and_delete_function_exists():
    """
    Test that the delete function exists and can be imported.
    """
    from i18n_check.check.non_source_keys import non_source_keys_check_and_delete

    assert callable(non_source_keys_check_and_delete)


def test_non_source_keys_delete_removes_keys_from_target_files_only(tmp_path):
    """
    Test that delete functionality removes non-source keys from target files only.
    """

    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    src_file = i18n_dir / "test_src.json"
    src_file.write_text('{\n  "i18n.valid_key": "Valid value"\n}\n', encoding="utf-8")

    # Create target file with extra key.
    target_file = i18n_dir / "test_target.json"
    target_file.write_text(
        '{\n  "i18n.valid_key": "Valid value in target",\n  "i18n.non_source_key": "Should be removed"\n}\n',
        encoding="utf-8",
    )

    # Use mock configuration.
    with patch("i18n_check.check.non_source_keys.config_i18n_directory", i18n_dir):
        non_source_keys_dict = {"test_target.json": {"i18n.non_source_key"}}
        non_source_keys_check_and_delete(non_source_keys_dict=non_source_keys_dict)

        # Verify source file unchanged, target file cleaned.
        from i18n_check.utils import read_json_file

        updated_src = read_json_file(src_file)
        updated_target = read_json_file(target_file)

        assert "i18n.valid_key" in updated_src  # source unchanged
        assert "i18n.valid_key" in updated_target
        assert "i18n.non_source_key" not in updated_target  # removed from target


def test_non_source_keys_are_sorted_in_output(capsys):
    """
    Test that non-source keys are sorted alphabetically in error output.
    """
    # Create test data with keys that would be unsorted naturally.
    non_source_keys_dict = {
        "test_file.json": {"i18n.z_key", "i18n.a_key", "i18n.m_key"}
    }

    with pytest.raises(SystemExit):
        non_source_keys_check(non_source_keys_dict)

    output = capsys.readouterr().out

    # Find the section with the keys.
    lines = output.split("\n")
    key_lines = []
    in_key_section = False

    for line in lines:
        if "Non-source keys in test_file.json:" in line:
            in_key_section = True
            continue

        if in_key_section and line.strip().startswith("i18n."):
            key_lines.append(line.strip())

        elif in_key_section and not line.strip().startswith("i18n.") and line.strip():
            break

    # Verify keys are sorted.
    expected_sorted_keys = ["i18n.a_key", "i18n.m_key", "i18n.z_key"]
    assert key_lines == expected_sorted_keys, (
        f"Keys not sorted. Expected: {expected_sorted_keys}, Got: {key_lines}"
    )


if __name__ == "__main__":
    pytest.main()
