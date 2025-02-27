# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if i18n-dir contains JSON files with nested JSON objects.
If yes, warns the user that this structure makes replacing invalid keys more difficult.

Usage:
    python3 src/i18n_check/check/nested_i18n_src.py
"""

import json
from pathlib import Path
from typing import Dict

from i18n_check.utils import i18n_directory, read_json_file, warn_on_nested_i18n_src


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


def check_i18n_files(directory: str | Path) -> None:
    """
    Check all JSON files in the given directory for nested structures.

    Parameters
    ----------
    directory : str
        The directory path to check for JSON files.

    Returns
    -------
    None
    """
    for file_path in Path(directory).rglob("*.json"):
        try:
            data = read_json_file(file_path)
            if is_nested_json(data) and warn_on_nested_i18n_src:
                print(f"Warning: Nested JSON structure detected in {file_path}")
                print(
                    "i18n-check recommends using flat JSON files to allow easy find-and-replace operations."
                )

        except (json.JSONDecodeError, IOError) as e:
            print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    check_i18n_files(i18n_directory)
