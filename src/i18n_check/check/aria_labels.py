# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if aria label keys (ending with '_aria_label') have appropriate punctuation.

Aria labels should not end with periods as they are read aloud by screen readers
and ending punctuation can affect the reading experience.

Examples
--------
Run the following script in terminal:

>>> i18n-check -al
>>> i18n-check -al -f  # to fix issues automatically
"""

import string
import sys
from pathlib import Path
from typing import Dict

from rich import print as rprint

from i18n_check.utils import (
    PATH_SEPARATOR,
    config_i18n_directory,
    get_all_json_files,
    read_json_file,
    replace_text_in_file,
)

# MARK: Find Issues


def find_aria_label_punctuation_issues(
    i18n_directory: Path = config_i18n_directory,
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Find aria label keys that end with inappropriate punctuation.

    Parameters
    ----------
    i18n_directory : Path
        The directory containing the i18n JSON files.

    Returns
    -------
    Dict[str, Dict[str, Dict[str, str]]]
        A dictionary mapping incorrect aria label values to their corrected versions.
    """
    json_files = get_all_json_files(directory=i18n_directory)

    punctuation_to_check = f"{string.punctuation}؟"

    aria_label_issues: Dict[str, Dict[str, Dict[str, str]]] = {}
    for json_file in json_files:
        json_file_dict = read_json_file(file_path=json_file)

        for key, value in json_file_dict.items():
            if isinstance(value, str) and key.endswith("_aria_label"):
                stripped_value = value.rstrip()

                # Aria labels should not have punctuation at either end.
                has_punctuation_at_end = (
                    stripped_value and stripped_value[-1] in punctuation_to_check
                )
                has_punctuation_at_start = (
                    stripped_value and stripped_value[0] in punctuation_to_check
                )

                if stripped_value and (
                    has_punctuation_at_end or has_punctuation_at_start
                ):
                    # Remove punctuation from both ends to be thorough.
                    corrected_value = stripped_value.strip(punctuation_to_check)

                    # Preserve any trailing whitespace from original.
                    if value.endswith(" "):
                        corrected_value += " "

                    if key not in aria_label_issues:
                        aria_label_issues[key] = {}

                    if json_file not in aria_label_issues[key]:
                        aria_label_issues[key][json_file] = {}

                    aria_label_issues[key][json_file]["current_value"] = value
                    aria_label_issues[key][json_file]["correct_value"] = corrected_value

    return aria_label_issues


# MARK: Report Issues


def report_and_fix_aria_labels(
    aria_label_issues: Dict[str, Dict[str, Dict[str, str]]],
    all_checks_enabled: bool = False,
    fix: bool = False,
) -> None:
    """
    Report aria label punctuation issues and optionally fix them.

    Parameters
    ----------
    aria_label_issues : Dict[str, Dict[str, Dict[str, str]]]
        Dictionary mapping keys with issues to their corrected values.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    fix : bool, optional
        Whether to automatically fix the issues, by default False.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if there are aria labels with invalid punctuation.
    """
    if not aria_label_issues:
        rprint(
            "[green]✅ aria-labels: All aria label keys have appropriate punctuation.[/green]"
        )
        return

    error_string = "\n[red]❌ aria-labels errors:\n\n"
    for k in aria_label_issues:
        error_string += f"Key: {k}\n"
        for json_file in aria_label_issues[k]:
            error_string += f"  File:      '{json_file.split(PATH_SEPARATOR)[-1]}'\n"

            current_value = aria_label_issues[k][json_file]["current_value"]
            corrected_value = aria_label_issues[k][json_file]["correct_value"]
            error_string += f"  Current:   '{current_value}'\n"
            error_string += f"  Suggested: '{corrected_value}'\n\n"

    error_string += "[/red][yellow]⚠️  Note: Aria labels should not end with punctuation as it affects screen reader experience.[/yellow]"

    rprint(error_string)

    if not fix:
        rprint(
            "[yellow]💡 Tip: You can automatically fix aria label punctuation by running the --aria-labels (-al) check with the --fix (-f) flag.[/yellow]\n"
        )

        if all_checks_enabled:
            raise ValueError("The aria labels i18n check has failed.")

        else:
            sys.exit(1)

    else:
        total_aria_label_issues = 0
        for k in aria_label_issues:
            for json_file in aria_label_issues[k]:
                current_value = aria_label_issues[k][json_file]["current_value"]
                correct_value = aria_label_issues[k][json_file]["correct_value"]

                # Replace the full key-value pair in JSON format.
                old_pattern = f'"{k}": "{current_value}"'
                new_pattern = f'"{k}": "{correct_value}"'
                replace_text_in_file(path=json_file, old=old_pattern, new=new_pattern)

                total_aria_label_issues += 1

        rprint(
            f"\n[green]✅ Fixed {total_aria_label_issues} aria label punctuation issues.[/green]\n"
        )


# MARK: Check Function


def aria_labels_check_and_fix(
    fix: bool = False, all_checks_enabled: bool = False
) -> bool:
    """
    Main function to check aria label punctuation.

    Parameters
    ----------
    fix : bool, optional, default=False
        Whether to automatically fix issues, by default False.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Returns
    -------
    bool
        True if the check is successful.
    """
    aria_label_issues = find_aria_label_punctuation_issues()
    report_and_fix_aria_labels(
        aria_label_issues=aria_label_issues,
        all_checks_enabled=all_checks_enabled,
        fix=fix,
    )

    return True
