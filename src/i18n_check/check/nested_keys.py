# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if i18n-dir contains JSON files with nested JSON objects.

If yes, warns the user that this structure makes replacing invalid keys more difficult.

Examples
--------
Run the following script in terminal:

>>> i18n-check -nk
"""

import json
from pathlib import Path
from typing import Dict

from rich import print as rprint

from i18n_check.utils import PATH_SEPARATOR, config_i18n_directory, read_json_file

# MARK: Is Nested


def is_nested_json(data: Dict[str, str]) -> bool:
    """
    Check if the JSON structure is nested.

    Parameters
    ----------
    data : dict
        The JSON data to check.

    Returns
    -------
    bool
        True if the JSON structure is nested, False otherwise.
    """
    if isinstance(data, dict):
        return any(isinstance(value, dict) for value in data.values())

    return False


def validate_nested_keys(directory: str | Path) -> None:
    """
    Check all JSON files in the given directory for nested structures.

    Parameters
    ----------
    directory : str
        The directory path to check for JSON files.
    """
    if not Path(directory).exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    for file_path in Path(directory).rglob("*.json"):
        try:
            data = read_json_file(file_path=file_path)
            if is_nested_json(data):
                error_message = (
                    "[red]\n❌ nested_keys error: Nested JSON structure detected in "
                    + str(file_path).split(PATH_SEPARATOR)[-1]
                    + ". i18n-check recommends using flat JSON files to allow easy find-and-replace operations. You can disable this check in your i18n-check.yaml configuration file.[/red]"
                )
                rprint(error_message)

        except (json.JSONDecodeError, IOError) as e:
            print(f"Error processing {file_path}: {e}")


# MARK: Main


if __name__ == "__main__":
    validate_nested_keys(config_i18n_directory)
