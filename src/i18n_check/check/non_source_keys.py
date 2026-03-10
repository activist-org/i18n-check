# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n target JSON files have keys that are not in the source file.

If yes, suggest that they be removed from the their respective JSON files.

Examples
--------
Run the following script in terminal:

>>> i18n-check -nsk
"""

import json
import sys
from pathlib import Path
from typing import Dict

from rich import print as rprint

from i18n_check.utils import (
    PATH_SEPARATOR,
    config_i18n_directory,
    config_i18n_src_file,
    config_i18n_src_file_name,
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
    non_source_keys_dict: Dict[str, str] = {}
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

        is_an_or_are = "is an" if len(non_source_keys_dict) == 1 else "are"
        has_or_have = "has" if len(non_source_keys_dict) == 1 else "have"
        file_or_files = "file" if len(non_source_keys_dict) == 1 else "files"

        error_message = (
            "\n"
            + f"[red]❌ non-source-keys error: There {is_an_or_are} i18n target JSON {file_or_files} that {has_or_have} keys that are not in the {config_i18n_src_file_name} i18n source file. Please remove or rename the following keys:"
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


def non_source_keys_check_and_delete(
    non_source_keys_dict: Dict[str, str], all_checks_enabled: bool = False
) -> bool:
    """
    Delete non-source keys from target JSON files.

    Parameters
    ----------
    non_source_keys_dict : Dict[str, str]
        A dictionary with non-source keys found in the JSON files.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Returns
    -------
    bool
        True if the operation is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if there are issues with file operations.
    """
    if not non_source_keys_dict:
        rprint(
            "[green]✅ non-source-keys delete success: No non-source keys to delete.[/green]"
        )
        return True

    try:
        files_updated = 0
        total_keys_removed = 0

        # Process each file that has non-source keys.
        for filename, keys_to_remove in non_source_keys_dict.items():
            file_path = config_i18n_directory / filename

            # Load the target file.
            target_data = read_json_file(file_path=file_path)
            keys_removed_from_file = 0

            # Remove non-source keys.
            for key in keys_to_remove:
                if key in target_data:
                    del target_data[key]
                    keys_removed_from_file += 1

            if keys_removed_from_file > 0:
                # Write updated target file.
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(target_data, f, indent=2, ensure_ascii=False)
                    f.write("\n")

                files_updated += 1
                total_keys_removed += keys_removed_from_file

        # Check if sorted-keys is enabled and sort target files if needed.
        try:
            from i18n_check.utils import config

            if config.get("checks", {}).get("sorted-keys", {}).get("active", False):
                from i18n_check.check.sorted_keys import fix_sorted_keys

                # Sort only the target files that were updated.
                for filename in non_source_keys_dict.keys():
                    file_path = config_i18n_directory / filename
                    fix_sorted_keys(file_path)

                rprint(
                    "[green]✨ Target files sorted alphabetically as sorted-keys check is enabled.[/green]"
                )
        except Exception:
            # If sorting fails, continue - deletion was successful.
            pass

        key_or_keys = "keys" if total_keys_removed > 1 else "key"
        file_or_files = "files" if files_updated > 1 else "file"

        rprint(
            f"[green]✅ non-source-keys delete success: Removed {total_keys_removed} non-source {key_or_keys} "
            f"from {files_updated} target {file_or_files}.[/green]"
        )

        return True

    except Exception as e:
        error_message = f"[red]❌ non-source-keys delete error: Failed to delete keys. {str(e)}[/red]"
        rprint(error_message)

        if all_checks_enabled:
            raise ValueError("The non-source keys delete operation has failed.")

        else:
            sys.exit(1)


# MARK: Variables

non_source_keys_dict = get_non_source_keys(
    i18n_src_dict=i18n_src_dict,
    i18n_directory=config_i18n_directory,
)
