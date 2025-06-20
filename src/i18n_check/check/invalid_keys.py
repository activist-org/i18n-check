# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks the i18n keys used in the project and makes sure that each of them appears in the i18n-src file.

If there are invalid keys, alert the user to their presence.

Examples
--------
Run the following script in terminal:

>>> python3 src/i18n_check/check/invalid_keys.py
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Set

from i18n_check.utils import (
    collect_files_to_check,
    config_file_types_to_check,
    config_i18n_src_file,
    config_invalid_keys_directories_to_skip,
    config_invalid_keys_files_to_skip,
    config_src_directory,
    read_json_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)


# MARK: Key Comparisons


def get_used_i18n_keys(
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    src_directory: Path = config_src_directory,
) -> Set[str]:
    """
    Get all i18n keys that are used in the project.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        The dictionary containing i18n source keys and their associated values.

    src_directory : Path
        The source directory where the files are located.

    Returns
    -------
    Set[str]
        A set of all i18n keys that are used in the project.
    """

    i18n_key_pattern_quote = r"\'i18n\.[_\S\.]+?\'"
    i18n_key_pattern_double_quote = r"\"i18n\.[_\S\.]+?\""
    i18n_key_pattern_back_tick = r"\`i18n\.[_\S\.]+?\`"
    all_i18n_key_patterns = [
        i18n_key_pattern_quote,
        i18n_key_pattern_double_quote,
        i18n_key_pattern_back_tick,
    ]

    files_to_check = collect_files_to_check(
        directory=src_directory,
        file_types=config_file_types_to_check,
        directories_to_skip=config_invalid_keys_directories_to_skip,
        files_to_skip=config_invalid_keys_files_to_skip,
    )
    files_to_check_contents = {}
    for frontend_file in files_to_check:
        with open(frontend_file, "r", encoding="utf-8") as f:
            files_to_check_contents[frontend_file] = f.read()

    all_used_i18n_keys: Set[Any] = set()
    for v in files_to_check_contents.values():
        all_file_i18n_keys: List[Any] = []
        all_file_i18n_keys.extend(
            re.findall(i18n_kp, v) for i18n_kp in all_i18n_key_patterns
        )
        # Remove the first and last characters that are the quotes or back ticks.
        all_file_i18n_keys = [k[1:-1] for ks in all_file_i18n_keys for k in ks]

        all_used_i18n_keys.update(all_file_i18n_keys)

    return set(all_used_i18n_keys)


# MARK: Error Outputs


def validate_i18n_keys(
    all_used_i18n_keys: Set[str],
    i18n_src_dict: Dict[str, str],
) -> None:
    """
    Validate that all used i18n keys are present in the source file.

    Parameters
    ----------
    all_used_i18n_keys : Set[str]
        A set of all i18n keys that are used in the project.

    i18n_src_dict : Dict[str, str]
        The dictionary containing i18n source keys and their associated values.

    Raises
    ------
    ValueError
        If there are any i18n keys that are used in the project but not defined in the source file.
    """
    all_keys = i18n_src_dict.keys()
    if invalid_keys := list(all_used_i18n_keys - all_keys):
        to_be = "are" if len(invalid_keys) > 1 else "is"
        key_to_be = "keys that are" if len(invalid_keys) > 1 else "key that is"
        key_or_keys = "keys" if len(invalid_keys) > 1 else "key"
        raise ValueError(
            f"\ninvalid_keys failure: There {to_be} {len(invalid_keys)} i18n {key_to_be} not in the i18n source file. Please check the validity of the following {key_or_keys}:\n\n{', '.join(invalid_keys)}\n"
        )

    else:
        print(
            "invalid_keys success: All i18n keys that are used in the project are in the i18n source file."
        )


if __name__ == "__main__":
    all_used_i18n_keys = get_used_i18n_keys(
        i18n_src_dict=i18n_src_dict, src_directory=config_src_directory
    )
    validate_i18n_keys(
        all_used_i18n_keys=all_used_i18n_keys, i18n_src_dict=i18n_src_dict
    )
