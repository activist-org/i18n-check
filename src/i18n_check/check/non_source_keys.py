# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n target JSON files have keys that are not in the source file.

If yes, suggest that they be removed from the their respective JSON files.

Examples
--------
Run the following script in terminal:

>>> i18n-check -nsk
"""

import sys
from pathlib import Path
from typing import Dict

from rich import print as rprint

from i18n_check.utils import (
    PATH_SEPARATOR,
    config_i18n_directory,
    config_i18n_src_file,
    get_all_json_files,
    read_json_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)

# MARK: Non Source Keys


def get_non_source_keys(
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    i18n_directory: Path = config_i18n_directory,
) -> Dict[str, str]:
    """
    Get non-source keys from a JSON file compared to the source dictionary.

    Parameters
    ----------
    i18n_src_dict : dict
        The dictionary containing i18n source keys and their associated values.

    i18n_directory : str, optional, default=`i18n-dir`
        The directory containing the i18n JSON files.

    Returns
    -------
    dict
        A dictionary with non-source keys found in the JSON file.
    """
    all_src_keys = i18n_src_dict.keys()
    non_source_keys_dict = {}
    for json_file in get_all_json_files(directory=i18n_directory):
        if (
            json_file.split(PATH_SEPARATOR)[-1]
            != str(config_i18n_src_file).split(PATH_SEPARATOR)[-1]
        ):
            json_dict = read_json_file(file_path=json_file)

            all_keys = json_dict.keys()

            if len(all_keys - all_src_keys) > 0:
                non_source_keys_dict[json_file.split(PATH_SEPARATOR)[-1]] = (
                    all_keys - all_src_keys
                )
    return non_source_keys_dict


# MARK: Error Outputs


def non_source_keys_check(
    non_source_keys_dict: Dict[str, str], all_checks_enabled: bool = False
) -> bool:
    """
    Report non-source keys found in the JSON file.

    Parameters
    ----------
    non_source_keys_dict : dict
        A dictionary with non-source keys found in the JSON file.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if the input dictionary is not empty.
    """
    if non_source_keys_dict:
        non_source_keys_string = "\n\n".join(
            (
                f"Non-source keys in {k}:"
                + " \n  "
                + "\n  ".join(non_source_keys_dict[k])
            )
            for k in non_source_keys_dict
        )
        is_an_or_are = "is an"
        has_or_have = "has"
        if len(non_source_keys_dict) > 1:
            is_an_or_are = "are"
            has_or_have = "have"

        error_message = (
            "\n"
            + f"[red]❌ non-source-keys error: There {is_an_or_are} i18n target JSON files that {has_or_have} keys that are not in the i18n source file. Please remove or rename the following keys:"
            + "\n\n"
            + non_source_keys_string
            + "[/red]"
        )
        rprint(error_message)

        if all_checks_enabled:
            raise ValueError("The non source keys i18n check has failed.")

        else:
            sys.exit(1)

    else:
        rprint(
            "[green]✅ non-source-keys success: No i18n target file has keys that are not in the i18n source file.[/green]"
        )

    return True


# MARK: Variables

non_source_keys_dict = get_non_source_keys(
    i18n_src_dict=i18n_src_dict,
    i18n_directory=config_i18n_directory,
)
