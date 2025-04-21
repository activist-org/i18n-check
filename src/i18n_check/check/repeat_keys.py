# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks for duplicate keys in i18n JSON files using JSON parsing.

Identifies exact key duplicates that might occur during mass replacements.

Examples
--------
Run the following script in terminal:

>>> python3 src/i18n_check/check/non_source_keys.py
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

from i18n_check.utils import get_all_json_files, i18n_directory, path_separator


def find_duplicate_keys(json_str: str) -> Dict[str, List[str]]:
    """
    Identify duplicate keys in a JSON string using a custom JSON parser hook.

    Parameters
    ----------
    json_str : str
        The JSON string to analyze for duplicate keys.

    Returns
    -------
    Dict[str, List[str]]
        A dictionary where keys are the duplicate keys found in the JSON and values
        are lists of string representations of all corresponding values.

    Raises
    ------
    ValueError
        If the input string is not valid JSON.

    Notes
    -----
    This function uses a custom object_pairs_hook with json.loads to track all
    key-value pairs, including duplicates that would normally be overwritten
    in a standard dictionary.

    Examples
    --------
    >>> find_duplicate_keys('{"a": 1, "a": 2, "b": 3}')
    {'a': ['1', '2']}
    """
    grouped = defaultdict(list)

    def create_key_values_dict(pairs: List[Tuple[Any, Any]]) -> Dict[str, Any]:
        """
        Create a dictionary while tracking all key-value pairs for duplicate detection.

        Parameters
        ----------
        pairs : List[Tuple[Any, Any]]
            List of key-value pairs from the JSON parser.

        Returns
        -------
        Dict[str, Any]
            A standard dictionary constructed from the pairs (last value wins for duplicates).
        """
        for key, value in pairs:
            grouped[key].append(str(value))

        return dict(pairs)

    try:
        json.loads(json_str, object_pairs_hook=create_key_values_dict)
        duplicates = {
            k: values_list for k, values_list in grouped.items() if len(values_list) > 1
        }
        return duplicates

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def check_file(file_path: str) -> Tuple[str, Dict[str, List[str]]]:
    """
    Check a single JSON file for duplicate keys.

    Parameters
    ----------
    file_path : str
        Path to the JSON file to be checked for duplicate keys.

    Returns
    -------
    Tuple[str, Dict[str, List[str]]]
        A tuple containing:
        - The filename (str)
        - A dictionary of duplicate keys with their values (Dict[str, List[str]])

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.

    ValueError
        If the file contains invalid JSON.

    Examples
    --------
    >>> check_file("example.json")
    ('example.json', {'duplicate_key': ['value1', 'value2']})
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return (Path(file_path).name, find_duplicate_keys(content))


def main() -> None:
    """
    Main check execution.

    Raises
    ------
    ValueError
        If any duplicate keys found.
    """
    json_files = get_all_json_files(i18n_directory, path_separator)
    has_errors = False

    for json_file in json_files:
        filename, duplicates = check_file(json_file)
        if duplicates:
            has_errors = True
            print(f"\nDuplicate keys in {filename}:")

            for key, values in duplicates.items():
                print(f"  '{key}' appears {len(values)} times with values: {values}")

    if has_errors:
        raise ValueError(
            "\nrepeat_keys failure: Duplicate keys found. All i18n keys must be unique."
        )

    print("repeat_keys success: No duplicate keys found in i18n files.")


if __name__ == "__main__":
    main()
