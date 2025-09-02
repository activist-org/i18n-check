# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if i18n JSON files have keys ordered alphabetically.

If not, reports the files that need ordering and optionally fixes them.

Examples
--------
Run the following script in terminal:

>>> i18n-check -ok
>>> i18n-check -ok -f  # to fix issues automatically
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from rich import print as rprint

from i18n_check.utils import (
    config_i18n_directory,
    get_all_json_files,
    path_separator,
    read_json_file,
)

# MARK: Check Ordered Keys


def check_keys_are_ordered(json_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Check if the keys in a JSON dictionary are ordered alphabetically.

    Parameters
    ----------
    json_data : Dict[str, any]
        The JSON data to check for key ordering.

    Returns
    -------
    Tuple[bool, List[str]]
        A tuple containing:
        - bool: True if keys are ordered, False otherwise
        - List[str]: List of keys in their correct alphabetical order
    """
    keys = list(json_data.keys())
    sorted_keys = sorted(keys)

    return keys == sorted_keys, sorted_keys


def check_file_ordered_keys(file_path: str | Path) -> Tuple[bool, List[str]]:
    """
    Check if keys in a specific JSON file are ordered alphabetically.

    Parameters
    ----------
    file_path : str | Path
        Path to the JSON file to check.

    Returns
    -------
    Tuple[bool, List[str]]
        A tuple containing:
        - bool: True if keys are ordered, False otherwise
        - List[str]: List of keys in their correct alphabetical order
    """
    try:
        json_data = read_json_file(file_path)
        return check_keys_are_ordered(json_data)
    except Exception as e:
        rprint(f"[red]Error reading {file_path}: {e}[/red]")
        return False, []


def fix_ordered_keys(file_path: str | Path) -> bool:
    """
    Fix the ordering of keys in a JSON file by sorting them alphabetically.

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

        # Create a new dictionary with sorted keys
        sorted_data = dict(sorted(json_data.items()))

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(sorted_data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        return True
    except Exception as e:
        rprint(f"[red]Error fixing {file_path}: {e}[/red]")
        return False


def check_ordered_keys(fix: bool = False) -> None:
    """
    Check if all i18n JSON files have keys ordered alphabetically.

    Parameters
    ----------
    fix : bool, optional, default=False
        If True, automatically fix key ordering in files that are not ordered.

    Raises
    ------
    sys.exit(1)
        If any files have unordered keys and fix is False.
    """
    json_files = get_all_json_files(
        directory=config_i18n_directory, path_separator=path_separator
    )

    if not json_files:
        rprint("[yellow]No JSON files found in the i18n directory.[/yellow]")
        return

    unordered_files = []

    for file_path in json_files:
        is_ordered, sorted_keys = check_file_ordered_keys(file_path)

        if not is_ordered:
            unordered_files.append(file_path)

            if fix:
                rprint(f"[yellow]Fixing key order in: {file_path}[/yellow]")
                if fix_ordered_keys(file_path):
                    rprint(f"[green]✅ Fixed key order in: {file_path}[/green]")
                else:
                    rprint(f"[red]❌ Failed to fix key order in: {file_path}[/red]")
            else:
                rprint(f"[red]❌ Keys not ordered alphabetically in: {file_path}[/red]")

    if unordered_files and not fix:
        files_count = len(unordered_files)
        file_word = "file" if files_count == 1 else "files"

        rprint(
            f"\n[red]❌ ordered_keys error: {files_count} i18n JSON {file_word} have keys that are not ordered alphabetically.[/red]"
        )
        rprint(
            "[yellow]💡 Tip: Use the --fix (-f) flag to automatically order the keys alphabetically.[/yellow]"
        )
        sys.exit(1)

    elif unordered_files and fix:
        rprint(
            f"\n[green]✅ Fixed key ordering in {len(unordered_files)} file(s).[/green]"
        )

    else:
        rprint(
            "[green]✅ ordered_keys success: All i18n JSON files have keys ordered alphabetically.[/green]"
        )


# MARK: Main

if __name__ == "__main__":
    check_ordered_keys()
