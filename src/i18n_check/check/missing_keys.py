# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if target locale files are missing keys that exist in the source file.

A key is considered missing if it's not present or if its value is an empty string.

Examples
--------
Run the following script in terminal:

>>> i18n-check -mk
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

from rich import print as rprint

from i18n_check.utils import (
    config_i18n_directory,
    config_i18n_src_file,
    config_missing_keys_locales_to_check,
    get_all_json_files,
    path_separator,
    read_json_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)

# MARK: Missing Keys


def get_missing_keys_by_locale(
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    i18n_directory: Path = config_i18n_directory,
    locales_to_check: List[str] = config_missing_keys_locales_to_check,
) -> Dict[str, Tuple[List[str], float]]:
    """
    Get missing keys for each locale file compared to the source dictionary.

    Parameters
    ----------
    i18n_src_dict : dict
        The dictionary containing i18n source keys and their associated values.

    i18n_directory : Path
        The directory containing the i18n JSON files.

    locales_to_check : list
        List of locale files to check. If empty, all locale files are checked.

    Returns
    -------
    dict
        A dictionary where keys are locale filenames and values are tuples containing:
        - A list of missing keys (including keys with empty string values)
        - The percentage of missing keys (0-100)
    """
    all_src_keys = set(i18n_src_dict.keys())
    missing_keys_by_locale = {}

    for json_file in get_all_json_files(i18n_directory, path_separator):
        filename = json_file.split(path_separator)[-1]

        # Skip the source file itself.
        if filename == str(config_i18n_src_file).split(path_separator)[-1]:
            continue

        # Skip if locales_to_check is specified and this file isn't in the list.
        if locales_to_check and filename not in locales_to_check:
            continue

        locale_dict = read_json_file(file_path=json_file)
        locale_keys = set(locale_dict.keys())

        # Find keys that are missing or have empty string values.
        missing_keys = []
        missing_keys.extend(
            key
            for key in all_src_keys
            if key not in locale_keys or locale_dict.get(key) == ""
        )

        # Calculate the percentage of missing keys.
        if all_src_keys:
            missing_percentage = (len(missing_keys) / len(all_src_keys)) * 100
        else:
            missing_percentage = 0.0

        if missing_keys:
            missing_keys_by_locale[filename] = (
                sorted(missing_keys),
                missing_percentage,
            )

    return missing_keys_by_locale


# MARK: Error Outputs


def report_missing_keys(
    missing_keys_by_locale: Dict[str, Tuple[List[str], float]],
) -> None:
    """
    Report missing keys found in locale files.

    Parameters
    ----------
    missing_keys_by_locale : dict
        A dictionary with locale filenames as keys and tuples of (missing keys, percentage) as values.

    Raises
    ------
    sys.exit(1)
        The system exits with 1 and prints error details if any locale files have missing keys.
    """
    if missing_keys_by_locale:
        error_message = (
            "\n[red]❌ missing_keys error: There are locale files with missing keys. "
            "Keys are considered missing if they don't exist or have empty string values.\n\n"
        )

        # Report missing keys for each locale.
        for locale_file, (missing_keys, percentage) in missing_keys_by_locale.items():
            error_message += f"Missing keys in {locale_file} ({len(missing_keys)} keys, {percentage:.1f}% missing):\n"
            for key in missing_keys:
                error_message += f"  - {key}\n"
            error_message += "\n"

        error_message += "Summary of missing keys by locale:\n"
        for locale_file, (missing_keys, percentage) in missing_keys_by_locale.items():
            error_message += f"  {locale_file}: {percentage:.1f}% missing\n"

        error_message += "[/red]"
        rprint(error_message)

        sys.exit(1)

    else:
        rprint(
            "[green]✅ missing_keys success: All checked locale files have all required keys with non-empty values.[/green]"
        )


# MARK: Main


if __name__ == "__main__":
    missing_keys_by_locale = get_missing_keys_by_locale(
        i18n_src_dict=i18n_src_dict,
        i18n_directory=config_i18n_directory,
        locales_to_check=config_missing_keys_locales_to_check,
    )
    report_missing_keys(missing_keys_by_locale=missing_keys_by_locale)
