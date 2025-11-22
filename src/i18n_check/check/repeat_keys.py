# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks for duplicate keys in i18n JSON files using JSON parsing.

Identifies exact key duplicates that might occur during mass replacements.

Examples
--------
Run the following script in terminal:

>>> i18n-check -rk
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from rich import print as rprint

from i18n_check.utils import config_i18n_directory, get_all_json_files

# MARK: Repeat Keys


def find_repeat_keys(json_input: Union[str, Path]) -> Dict[str, List[str]]:
    """
    Identify duplicate keys in a JSON string using a custom JSON parser hook.

    Parameters
    ----------
    json_input : Union[str, Path]
        A JSON string or a Path to a JSON file to analyze for duplicate keys.

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
    >>> find_repeat_keys('{"a": 1, "a": 2, "b": 3}')
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
        if isinstance(json_input, Path):
            if not json_input.exists():
                raise ValueError(f"File does not exist: {json_input}")

            json_str = Path(json_input).read_text(encoding="utf-8")

        else:
            json_str = json_input

        json.loads(json_str, object_pairs_hook=create_key_values_dict)
        duplicates = {
            k: sorted(values_list)
            for k, values_list in grouped.items()
            if len(values_list) > 1
        }
        return duplicates

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


# MARK: Check File


def check_file_keys_repeated(file_path: str) -> Tuple[str, Dict[str, List[str]]]:
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
    >>> check_file_keys_repeated("example.json")
    ('example.json', {'duplicate_key': ['value1', 'value2']})
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return (Path(file_path).name, find_repeat_keys(content))


# MARK: Error Outputs


def repeat_keys_check(
    directory: str | Path = config_i18n_directory, all_checks_enabled: bool = False
) -> bool:
    """
    Main check execution.

    Parameters
    ----------
    directory : str | Path, default=config_i18n_directory
        The directory path to check for JSON files.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if any duplicate keys found.
    """
    json_files = get_all_json_files(directory=directory)
    has_errors = False

    error_message = ""
    file_duplicate_keys_messages = ""
    for json_file in json_files:
        filename, duplicates = check_file_keys_repeated(json_file)
        if duplicates:
            has_errors = True
            file_duplicate_keys_messages += f"\n[red]Repeat keys in {filename}:[/red]"

            for key, values in duplicates.items():
                file_duplicate_keys_messages += f"[red]\n  {key} appears {len(values)} times with values: {values}[/red]"

    if has_errors:
        error_message += "\n[red]❌ repeat-keys error: Repeat i18n keys found. All i18n keys must be unique.[/red]\n"
        error_message += file_duplicate_keys_messages
        rprint(error_message)

        if all_checks_enabled:
            raise ValueError("The repeat keys i18n check has failed.")

        else:
            sys.exit(1)

    rprint(
        "[green]✅ repeat-keys success: No duplicate keys found in i18n files.[/green]"
    )

    return True
