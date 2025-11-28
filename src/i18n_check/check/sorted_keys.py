# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if i18n JSON files have keys sorted alphabetically.

If not, reports the files that need sorting and optionally fixes them.

Examples
--------
Run the following script in terminal:

>>> i18n-check -sk
>>> i18n-check -sk -f  # to fix issues automatically
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from rich import print as rprint

from i18n_check.utils import (
    config_i18n_directory,
    get_all_json_files,
    read_json_file,
)

# MARK: Check Sorted Keys


def check_file_keys_sorted(json_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Check if the keys in a JSON dictionary are sorted alphabetically.

    Parameters
    ----------
    json_data : Dict[str, any]
        The JSON data to check for sorted keys.

    Returns
    -------
    Tuple[bool, List[str]]
        A tuple containing:
        - bool: True if keys are sorted, False otherwise
        - List[str]: List of keys in their correct alphabetical order for testing
    """
    keys = list(json_data.keys())
    sorted_keys = sorted(keys)

    return keys == sorted_keys, sorted_keys


def check_file_sorted(file_path: str | Path) -> Tuple[bool, List[str]]:
    """
    Check if keys in a specific JSON file are sorted alphabetically.

    Parameters
    ----------
    file_path : str | Path
        Path to the JSON file to check.

    Returns
    -------
    Tuple[bool, List[str]]
        A tuple containing:
        - bool: True if keys are sorted, False otherwise
        - List[str]: List of keys in their correct alphabetical order
    """
    try:
        json_data = read_json_file(file_path)
        return check_file_keys_sorted(json_data)

    except Exception as e:
        rprint(f"[red]Error reading {file_path}: {e}[/red]")
        return False, []


def fix_sorted_keys(file_path: str | Path) -> bool:
    """
    Fix the sorting of keys in a JSON file by sorting them alphabetically.

    Parameters
    ----------
    file_path : str | Path
        Path to the JSON file to fix.

    Returns
    -------
    bool
        True if the file was successfully fixed, False otherwise.
    """
    try:
        json_data = read_json_file(file_path)

        # Create a new dictionary with sorted keys.
        sorted_data = dict(sorted(json_data.items()))

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(sorted_data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        return True

    except Exception as e:
        rprint(f"[red]Error fixing {file_path}: {e}[/red]")
        return False


def sorted_keys_check_and_fix(
    all_checks_enabled: bool = False, fix: bool = False
) -> bool:
    """
    Check if all i18n JSON files have keys sorted alphabetically.

    Parameters
    ----------
    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    fix : bool, optional, default=False
        If True, automatically fix unsorted key in files that are not sorted.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        If any files have unsorted keys and fix is False.
    """
    json_files = get_all_json_files(directory=config_i18n_directory)

    if Path(".i18n-check.yaml").is_file():
        config_file_name = ".i18n-check.yaml"

    else:
        config_file_name = ".i18n-check.yml"

    if not json_files:
        ValueError(
            f"No JSON files found in the i18n directory. Did you define i18n-dir incorrectly in {config_file_name}?"
        )

    unsorted_files = []
    for file_path in json_files:
        is_sorted, sorted_keys = check_file_sorted(file_path)

        if not is_sorted:
            unsorted_files.append(file_path)

    if unsorted_files and not fix:
        files_count = len(unsorted_files)
        file_or_files = "file" if files_count == 1 else "files"
        has_or_have = "has" if files_count == 1 else "have"

        rprint(
            f"\n[red]❌ sorted-keys error: {files_count} i18n JSON {file_or_files} {has_or_have} keys that are not sorted alphabetically.[/red]\n"
        )

        for f in unsorted_files:
            rprint(f"[red]Keys not sorted alphabetically in: {f}[/red]")

        rprint(
            "\n[yellow]💡 Tip: Use the --fix (-f) flag to automatically sort the keys alphabetically.[/yellow]\n"
        )

        if all_checks_enabled:
            raise ValueError("The sorted keys i18n check has failed.")

        else:
            sys.exit(1)

    elif unsorted_files and fix:
        file_or_files = "file" if len(unsorted_files) == 1 else "files"
        rprint(
            f"\n[green]Fixing key sorting in {len(unsorted_files)} {file_or_files}:[/green]"
        )

        for f in unsorted_files:
            if fix_sorted_keys(f):
                rprint(f"[green]✅ Fixed key order in {f}[/green]")

            else:
                rprint(f"[red]Failed to fix key order in {f}[/red]")

    else:
        rprint(
            "[green]✅ sorted-keys success: All i18n JSON files have keys sorted alphabetically.[/green]"
        )

    return True
