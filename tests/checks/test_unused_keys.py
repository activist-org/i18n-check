# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the unused_keys.py.
"""

from unittest.mock import patch

import pytest

from i18n_check.check.unused_keys import (
    files_to_check_contents,
    find_unused_keys,
    unused_keys_check,
    unused_keys_check_and_delete,
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
    assert "💡 Tip: You can automatically delete unused keys" in output

    # Test that keys are sorted in the output.
    lines = output.split("\n")
    key_lines = [line.strip() for line in lines if line.strip().startswith("i18n.")]
    expected_sorted_keys = sorted(
        [
            "i18n._global.unused_i18n_key",
            "i18n.repeat_value_multiple_files_repeat",
            "i18n.repeat_value_single_file_repeat",
        ]
    )
    assert key_lines == expected_sorted_keys, (
        f"Keys not sorted. Expected: {expected_sorted_keys}, Got: {key_lines}"
    )


def test_unused_keys_check_and_delete_function_exists():
    """
    Test that the delete function exists and can be imported.
    """
    from i18n_check.check.unused_keys import unused_keys_check_and_delete

    assert callable(unused_keys_check_and_delete)


def test_unused_keys_delete_removes_keys_from_json_files(tmp_path):
    """
    Test that delete functionality removes unused keys from JSON files.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    # Create source file.
    src_file = i18n_dir / "test_src.json"
    src_file.write_text(
        '{\n  "i18n.used_key": "Used value",\n  "i18n.unused_key": "Unused value"\n}\n',
        encoding="utf-8",
    )

    # Create target file.
    target_file = i18n_dir / "test_target.json"
    target_file.write_text(
        '{\n  "i18n.used_key": "Used value in target",\n  "i18n.unused_key": "Unused value in target"\n}\n',
        encoding="utf-8",
    )

    # Mock configuration to use our temp files.
    with (
        patch("i18n_check.check.unused_keys.config_i18n_src_file", src_file),
        patch("i18n_check.check.unused_keys.config_i18n_directory", i18n_dir),
    ):
        unused_keys = ["i18n.unused_key"]
        unused_keys_check_and_delete(unused_keys=unused_keys)

        # Verify keys were removed.
        updated_src = read_json_file(src_file)
        updated_target = read_json_file(target_file)

        assert "i18n.used_key" in updated_src
        assert "i18n.unused_key" not in updated_src
        assert "i18n.used_key" in updated_target
        assert "i18n.unused_key" not in updated_target


if __name__ == "__main__":
    pytest.main()
