# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has keys that are not used in the codebase.

If yes, suggest that they be removed from the i18n-src.

Examples
--------
Run the following script in terminal:

>>> i18n-check -uk
"""

import re
import sys
from typing import Dict, List

from rich import print as rprint

from i18n_check.utils import (
    collect_files_to_check,
    config_file_types_to_check,
    config_i18n_src_file,
    config_src_directory,
    config_unused_keys_directories_to_skip,
    config_unused_keys_files_to_skip,
    read_files_to_dict,
    read_json_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)
files_to_check = collect_files_to_check(
    directory=config_src_directory,
    file_types_to_check=config_file_types_to_check,
    directories_to_skip=config_unused_keys_directories_to_skip,
    files_to_skip=config_unused_keys_files_to_skip,
)
files_to_check_contents = read_files_to_dict(files=files_to_check)

# MARK: Unused Keys


def find_unused_keys(
    i18n_src_dict: Dict[str, str], files_to_check_contents: Dict[str, str]
) -> List[str]:
    """
    Identify unused translation keys from the i18n source dictionary.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        A dictionary of all translation keys and their corresponding strings.

    files_to_check_contents : Dict[str, str]
        A mapping of filenames to their contents, used to search for key usage.

    Returns
    -------
    List[str]
        A list of keys that are not used in any of the provided file contents.
    """
    all_keys = list(i18n_src_dict.keys())
    used_keys: List[str] = []

    for k in all_keys:
        key_search_pattern = r"[\S]*\.".join(k.split("."))

        for file_contents in files_to_check_contents.values():
            if re.search(key_search_pattern, file_contents):
                used_keys.append(k)
                break

    return list(set(all_keys) - set(used_keys))


# MARK: Error Outputs


def unused_keys_check(unused_keys: List[str], all_checks_enabled: bool = False) -> bool:
    """
    Print a message reporting unused translation keys or success.

    Parameters
    ----------
    unused_keys : List[str]
        A list of keys that are unused in the project.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if there are unused keys.
    """
    if unused_keys:
        to_be = "are" if len(unused_keys) > 1 else "is"
        key_or_keys = "keys" if len(unused_keys) > 1 else "key"

        error_message = (
            "[red]\n❌ unused-keys error: There "
            + f"{to_be} {len(unused_keys)} unused i18n {key_or_keys} in the i18n source file. Please remove or assign the following {key_or_keys}:"
            + "\n\n"
            + "\n".join(unused_keys)
            + "[/red]"
        )
        rprint(error_message)

        if all_checks_enabled:
            raise ValueError("The unused keys i18n check has failed.")

        else:
            sys.exit(1)

    else:
        rprint(
            "[green]✅ unused-keys success: All i18n keys in the i18n-src file are used in the project.[/green]"
        )

    return True


# MARK: Variables

unused_keys = find_unused_keys(
    i18n_src_dict=i18n_src_dict, files_to_check_contents=files_to_check_contents
)
