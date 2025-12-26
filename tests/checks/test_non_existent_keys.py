# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the nonexistent_keys.py.
"""

import json
import re
from pathlib import Path
from unittest.mock import patch

import pytest

from i18n_check.check.nonexistent_keys import (
    add_nonexistent_keys_interactively,
    get_used_i18n_keys,
    nonexistent_keys_check,
    nonexistent_keys_check_and_fix,
)
from i18n_check.utils import read_json_file

from ..test_utils import (
    checks_fail_dir,
    checks_pass_dir,
    fail_checks_src_json,
    pass_checks_src_json,
    pass_checks_src_json_path,
)

i18n_used_fail = get_used_i18n_keys(
    i18n_src_dict=fail_checks_src_json, src_directory=checks_fail_dir
)

i18n_used_pass = get_used_i18n_keys(
    i18n_src_dict=pass_checks_src_json, src_directory=checks_pass_dir
)

all_i18n_used = get_used_i18n_keys()


@pytest.mark.parametrize(
    "used_keys, expected_output",
    [
        (len(i18n_used_pass), 7),
        (len(i18n_used_fail), 15),
        (len(all_i18n_used), 15),
        (
            i18n_used_fail,
            {
                "i18n._global.hello_global",
                "i18n._global.repeat_value_hello_global",
                "i18n._global.repeat_key",
                "i18n.sub_dir._global.hello_sub_dir",
                "i18n.sub_dir_first_file.hello_sub_dir_first_file",
                "i18n.sub_dir_second_file.hello_sub_dir_second_file",
                "i18n.test_file.form_button_aria_label",
                "i18n.test_file.fox_image_alt_text",
                "i18n.test_file.incorrectly-formatted-key",
                "i18n.test_file.nested_example",
                "i18n.test_file.not_in_i18n_source_file",
                "i18n.test_file.repeat_key_lower",
                "i18n.wrong_identifier_path.content_reference",
                "i18n.repeat_value_single_file",
                "i18n.repeat_value_multiple_files",
            },
        ),
    ],
)
def test_get_used_i18n_keys(used_keys, expected_output) -> None:
    """
    Test get_used_i18n_keys with various scenarios.
    """
    assert used_keys == expected_output


def test_all_keys_include_fail_and_pass_sets():
    """
    Test that all the i18n keys used in testing contain the fail and pass keys.
    """
    assert all_i18n_used >= i18n_used_fail
    assert (
        not all_i18n_used >= i18n_used_pass
    )  # i18n.test_file.hello_test_file is correct in pass


def test_validate_fail_i18n_keys(capsys) -> None:
    """
    Test nonexistent_keys_check for the fail case.
    """
    with pytest.raises(SystemExit):
        nonexistent_keys_check(
            all_used_i18n_keys=i18n_used_fail, i18n_src_dict=fail_checks_src_json
        )

    msg = capsys.readouterr().out.replace("\n", "")
    assert "Please check the validity of the following" in msg
    assert "key:" in msg
    assert (
        " There is 1 i18n key that is not in the test_i18n_src.json i18n source file."
        in msg
    )
    assert "i18n.test_file.not_in_i18n_source_file" in msg


def test_validate_pass_i18n_keys(capsys) -> None:
    """
    Test nonexistent_keys_check for the pass case.
    """
    # For pass case, it should not raise an error.
    nonexistent_keys_check(
        all_used_i18n_keys=i18n_used_pass, i18n_src_dict=pass_checks_src_json
    )
    pass_result = capsys.readouterr().out
    cleaned_pass_result = re.sub(r"\x1b\[.*?m", "", pass_result).strip()

    assert "✅ nonexistent-keys success: " in cleaned_pass_result.replace("\n", "")
    assert "All i18n keys that are used in the project" in cleaned_pass_result.replace(
        "\n", ""
    )
    assert "i18n source file." in cleaned_pass_result.replace("\n", "")


def test_add_nonexistent_keys_interactively_no_nonexistent_keys(capsys) -> None:
    """
    Test add_nonexistent_keys_interactively for the pass case (case when all keys exist).
    """
    add_nonexistent_keys_interactively(
        all_used_i18n_keys=i18n_used_pass,
        i18n_src_dict=pass_checks_src_json,
        i18n_src_file=pass_checks_src_json_path,
        src_directory=checks_pass_dir,
    )

    i18n_src_dict = read_json_file(file_path=pass_checks_src_json_path)

    # The i18n source file should not be modified.
    assert i18n_src_dict == pass_checks_src_json

    captured = capsys.readouterr()
    assert "nonexistent-keys success" in captured.out.replace("\n", "")
    assert (
        "All i18n keys that are used in the project are in the i18n source file"
        in captured.out.replace("\n", "")
    )


@patch("i18n_check.check.nonexistent_keys.Prompt.ask")
def test_add_nonexistent_keys_interactively_with_values_when_keys_were_originally_sorted(
    mock_prompt, tmp_path: Path, capsys
) -> None:
    """
    Test that add_nonexistent_keys_interactively adds values for nonexistent keys
    and keys in the i18n source file are sorted when they were originally sorted in the input dictionary.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    i18n_src_file = i18n_dir / "src.json"
    i18n_src_dict = {
        "i18n.a_existing_key": "Existing value 1",
        "i18n.c_existing_key": "Existing value 2",
    }
    i18n_src_file.write_text(
        json.dumps(i18n_src_dict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Create a file that uses these keys.
    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)
    test_file = src_dir / "test.ts"
    test_file.write_text(
        "const text1 = 'i18n.a_existing_key'; const text2 = 'i18n.b_nonexistent_key'; const text3 = 'i18n.c_existing_key'; const text4 = 'i18n.d_nonexistent_key';",
        encoding="utf-8",
    )

    used_keys = {
        "i18n.a_existing_key",
        "i18n.b_nonexistent_key",
        "i18n.c_existing_key",
        "i18n.d_nonexistent_key",
    }

    # Mock user input.
    mock_prompt.side_effect = [
        "Nonexistent value 1",
        "Nonexistent value 2",
    ]

    add_nonexistent_keys_interactively(
        all_used_i18n_keys=used_keys,
        i18n_src_dict=i18n_src_dict,
        i18n_src_file=i18n_src_file,
        src_directory=src_dir,
    )

    updated_i18n_src_dict = read_json_file(file_path=i18n_src_file)

    expected_content = {
        "i18n.a_existing_key": "Existing value 1",
        "i18n.b_nonexistent_key": "Nonexistent value 1",
        "i18n.c_existing_key": "Existing value 2",
        "i18n.d_nonexistent_key": "Nonexistent value 2",
    }

    assert updated_i18n_src_dict == expected_content

    # Also check order.
    assert list(updated_i18n_src_dict.keys()) == list(expected_content.keys())

    captured = capsys.readouterr()
    assert "All keys have been added to the i18n source file" in captured.out.replace(
        "\n", ""
    )


@patch("i18n_check.check.nonexistent_keys.Prompt.ask")
def test_add_nonexistent_keys_interactively_with_values_when_keys_were_originally_unsorted(
    mock_prompt, tmp_path: Path
) -> None:
    """
    Test that add_nonexistent_keys_interactively adds values for nonexistent keys
    and keys in the i18n source file are sorted when they were originally unsorted in the input dictionary.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    i18n_src_file = i18n_dir / "src.json"
    i18n_src_dict = {
        "i18n.c_existing_key": "Existing value 1",
        "i18n.a_existing_key": "Existing value 2",
    }
    i18n_src_file.write_text(
        json.dumps(i18n_src_dict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Create a file that uses these keys.
    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)
    test_file = src_dir / "test.ts"
    test_file.write_text(
        "const text1 = 'i18n.a_existing_key'; const text2 = 'i18n.b_nonexistent_key'; const text3 = 'i18n.c_existing_key'; const text4 = 'i18n.d_nonexistent_key';",
        encoding="utf-8",
    )

    used_keys = {
        "i18n.a_existing_key",
        "i18n.b_nonexistent_key",
        "i18n.c_existing_key",
        "i18n.d_nonexistent_key",
    }

    # Mock user input.
    mock_prompt.side_effect = [
        "Nonexistent value 1",
        "Nonexistent value 2",
    ]

    add_nonexistent_keys_interactively(
        all_used_i18n_keys=used_keys,
        i18n_src_dict=i18n_src_dict,
        i18n_src_file=i18n_src_file,
        src_directory=src_dir,
    )

    updated_i18n_src_dict = read_json_file(file_path=i18n_src_file)

    expected_content = {
        "i18n.a_existing_key": "Existing value 2",
        "i18n.b_nonexistent_key": "Nonexistent value 1",
        "i18n.c_existing_key": "Existing value 1",
        "i18n.d_nonexistent_key": "Nonexistent value 2",
    }

    assert updated_i18n_src_dict == expected_content

    # Also check order.
    assert list(updated_i18n_src_dict.keys()) == list(expected_content.keys())


@patch("i18n_check.check.nonexistent_keys.Prompt.ask")
def test_add_nonexistent_keys_interactively_skip(
    mock_prompt, tmp_path: Path, capsys
) -> None:
    """
    Test that add_nonexistent_keys_interactively skips keys correctly when empty value is provided.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    i18n_src_file = i18n_dir / "src.json"
    i18n_src_dict = {
        "i18n.a_existing_key": "Existing value 1",
        "i18n.c_existing_key": "Existing value 2",
    }
    i18n_src_file.write_text(
        json.dumps(i18n_src_dict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Create a file that uses these keys.
    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)
    test_file = src_dir / "test.ts"
    test_file.write_text(
        "const text1 = 'i18n.a_existing_key'; const text2 = 'i18n.b_skipped_nonexistent_key'; const text3 = 'i18n.c_existing_key'; const text4 = 'i18n.d_nonexistent_key';",
        encoding="utf-8",
    )

    used_keys = {
        "i18n.a_existing_key",
        "i18n.b_skipped_nonexistent_key",
        "i18n.c_existing_key",
        "i18n.d_nonexistent_key",
    }

    # Mock user input.
    mock_prompt.side_effect = [
        "",
        "Nonexistent value 2",
    ]

    add_nonexistent_keys_interactively(
        all_used_i18n_keys=used_keys,
        i18n_src_dict=i18n_src_dict,
        i18n_src_file=i18n_src_file,
        src_directory=src_dir,
    )

    updated_i18n_src_dict = read_json_file(file_path=i18n_src_file)

    expected_content = {
        "i18n.a_existing_key": "Existing value 1",
        "i18n.c_existing_key": "Existing value 2",
        "i18n.d_nonexistent_key": "Nonexistent value 2",
    }

    assert "i18n.b_skipped_nonexistent_key" not in updated_i18n_src_dict
    assert updated_i18n_src_dict == expected_content

    captured = capsys.readouterr()
    assert "Skipped 'i18n.b_skipped_nonexistent_key'" in captured.out.replace("\n", "")
    assert (
        "1 key still missing in the test_i18n_src.json i18n source file"
        in captured.out.replace("\n", "")
    )


@patch("i18n_check.check.nonexistent_keys.Prompt.ask")
def test_add_nonexistent_keys_interactively_keyboard_interrupt(
    mock_prompt, tmp_path: Path, capsys
) -> None:
    """
    Test that add_nonexistent_keys_interactively handles KeyboardInterrupt gracefully.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    i18n_src_file = i18n_dir / "src.json"
    i18n_src_dict = {
        "i18n.a_existing_key": "Existing value 1",
        "i18n.c_existing_key": "Existing value 2",
    }
    i18n_src_file.write_text(
        json.dumps(i18n_src_dict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Create a file that uses these keys.
    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)
    test_file = src_dir / "test.ts"
    test_file.write_text(
        "const text1 = 'i18n.a_existing_key'; const text2 = 'i18n.b_nonexistent_key'; const text3 = 'i18n.c_existing_key'; const text4 = 'i18n.d_nonexistent_key';",
        encoding="utf-8",
    )

    used_keys = {
        "i18n.a_existing_key",
        "i18n.b_nonexistent_key",
        "i18n.c_existing_key",
        "i18n.d_nonexistent_key",
    }

    # Mock user input.
    mock_prompt.side_effect = [
        "Nonexistent value 1",
        KeyboardInterrupt(),
    ]

    with pytest.raises(SystemExit):
        add_nonexistent_keys_interactively(
            all_used_i18n_keys=used_keys,
            i18n_src_dict=i18n_src_dict,
            i18n_src_file=i18n_src_file,
            src_directory=src_dir,
        )

    updated_i18n_src_dict = read_json_file(file_path=i18n_src_file)

    expected_content = {
        "i18n.a_existing_key": "Existing value 1",
        "i18n.b_nonexistent_key": "Nonexistent value 1",
        "i18n.c_existing_key": "Existing value 2",
    }

    assert "i18n.d_nonexistent_key" not in updated_i18n_src_dict
    assert updated_i18n_src_dict == expected_content

    captured = capsys.readouterr()
    assert "Cancelled by user" in captured.out.replace("\n", "")


@patch("i18n_check.check.nonexistent_keys.nonexistent_keys_check")
def test_nonexistent_keys_check_and_fix_no_fix(
    mock_nonexistent_keys_check, tmp_path: Path
) -> None:
    """
    Test that nonexistent_keys_check_and_fix calls normal check function when fix=False.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    i18n_src_file = i18n_dir / "src.json"
    i18n_src_dict = {"i18n.a_existing_key": "Existing value 1"}

    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)

    used_keys = {"i18n.a_existing_key"}

    nonexistent_keys_check_and_fix(
        all_used_i18n_keys=used_keys,
        i18n_src_dict=i18n_src_dict,
        i18n_src_file=i18n_src_file,
        src_directory=src_dir,
        all_checks_enabled=True,
        fix=False,
    )

    # Verify the normal check function was called with correct parameters.
    mock_nonexistent_keys_check.assert_called_once_with(
        all_used_i18n_keys=used_keys,
        i18n_src_dict=i18n_src_dict,
        all_checks_enabled=True,
    )


@patch("i18n_check.check.nonexistent_keys.add_nonexistent_keys_interactively")
def test_nonexistent_keys_check_and_fix_with_fix(
    mock_add_nonexistent_keys_interactively, tmp_path: Path
) -> None:
    """
    Test that nonexistent_keys_check_and_fix calls interactive fix function when fix=True.
    """
    i18n_dir = tmp_path / "i18n"
    i18n_dir.mkdir(parents=True)

    i18n_src_file = i18n_dir / "src.json"
    i18n_src_dict = {"i18n.a_existing_key": "Existing value 1"}

    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)

    used_keys = {"i18n.a_existing_key"}

    nonexistent_keys_check_and_fix(
        all_used_i18n_keys=used_keys,
        i18n_src_dict=i18n_src_dict,
        i18n_src_file=i18n_src_file,
        src_directory=src_dir,
        fix=True,
    )

    # Verify the interactive fix function was called with correct parameters.
    mock_add_nonexistent_keys_interactively.assert_called_once_with(
        all_used_i18n_keys=used_keys,
        i18n_src_dict=i18n_src_dict,
        i18n_src_file=i18n_src_file,
        src_directory=src_dir,
    )


if __name__ == "__main__":
    pytest.main()
