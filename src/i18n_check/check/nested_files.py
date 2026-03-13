# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if i18n-dir contains JSON files with nested JSON objects.

If yes, warns the user that this structure makes replacing invalid keys more difficult.

Examples
--------
Run the following script in terminal:

>>> i18n-check -nf
>>> i18n-check -nf -f  # to fix issues automatically
"""

import json
from pathlib import Path
from typing import Any, Dict, Union

from rich import print as rprint

from i18n_check.utils import config_i18n_directory, read_json_file

# MARK: Is Nested


def is_nested_json(data: dict[str, Any]) -> bool:
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


# MARK: Flatten Nested JSON


def flatten_json(
    data: Dict[str, Any], parent_key: str = ""
) -> tuple[Dict[str, Any], bool]:
    """
    Flatten a nested JSON dictionary by joining nested keys with the period separator.

    Parameters
    ----------
    data : Dict[str, Any]
        The data JSON object to flatten.

    parent_key : str, default=''
        The parent key of a sub-object within the data.

    Returns
    -------
    tuple[Dict[str, Any], bool]
        (flattened_dict, has_collision) - The flattened dict and whether there were duplicate keys.
    """
    items: list[tuple[str, Any]] = []
    has_collision = False

    for key, value in data.items():
        new_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            nested_result, nested_collision = flatten_json(value, new_key)
            if nested_collision:
                has_collision = True
            items.extend(nested_result.items())

        else:
            items.append((new_key, value))

    flattened = dict(items)
    if len(flattened) != len(items):
        has_collision = True

    return flattened, has_collision


def derive_nested_files(
    directory: Union[str, Path] = config_i18n_directory,
) -> list[Path]:
    """
    Derive if nested files exist in the source and target JSON files.

    Parameters
    ----------
    directory : str | Path, default=config_i18n_directory
        The directory path to check for JSON files.

    Returns
    -------
    list[Path]
        The list of files that are nested or an empty list.
    """
    if not Path(directory).exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    nested_files: list[Path] = []

    for file_path in Path(directory).rglob("*.json"):
        try:
            data = read_json_file(file_path=file_path)
            if is_nested_json(data):
                nested_files.append(file_path)

        except (json.JSONDecodeError, IOError) as e:
            print(f"Error processing {file_path}: {e}")

    return nested_files


def nested_files_check(directory: Union[str, Path] = config_i18n_directory) -> bool:
    """
    Check all JSON files in the given directory for nested structures.

    Parameters
    ----------
    directory : str | Path, default=config_i18n_directory
        The directory path to check for JSON files.

    Returns
    -------
    bool
        True if the check is successful.
    """
    if nested_files := derive_nested_files(directory=directory):
        for file_path in nested_files:
            rprint(
                f"\n[red]❌ nested-files error: Nested JSON structure detected in {file_path}[/red]"
            )
        rprint(
            "[yellow]💡 i18n-check recommends using flat JSON files to make replacing invalid keys easier.[/yellow]"
        )
        return True

    return False


def nested_files_check_and_fix(
    directory: Union[str, Path] = config_i18n_directory,
) -> bool:
    """
    Check all JSON files in the given directory for nested structures.

    Parameters
    ----------
    directory : str | Path, default=config_i18n_directory
        The directory path to check for JSON files.

    Returns
    -------
    bool
        True if the check is successful.
    """
    if not (nested_files := derive_nested_files(directory=directory)):
        return False

    file_or_files = "file" if len(nested_files) == 1 else "files"
    rprint(
        f"\n[yellow]Flattening nested JSON in {len(nested_files)} {file_or_files}:[/yellow]"
    )

    failed: list[Path] = []
    for file_path in nested_files:
        try:
            data = read_json_file(file_path=file_path)

            flattened, has_collision = flatten_json(data)
            if has_collision:
                rprint(
                    f"[yellow]⚠️ Key collision detected in {file_path}. Manual fix required.[/yellow]"
                )
                failed.append(file_path)
                continue

            with file_path.open("w", encoding="utf-8") as file_obj:
                json.dump(flattened, file_obj, indent=2, ensure_ascii=False)
                file_obj.write("\n")

            rprint(f"[green]✅ Flattened nested keys in {file_path}[/green]")

        except Exception as e:
            rprint(f"[red]❌ Failed to flatten {file_path}: {e}[/red]")
            failed.append(file_path)

    if failed:
        rprint(f"\n[red]❌ {len(failed)} file(s) failed to flatten.[/red]")
        return False

    return True
