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
from typing import Dict

from rich import print as rprint

from i18n_check.utils import (
    config_i18n_directory,
    config_i18n_src_file,
    get_all_json_files,
    path_separator,
    read_json_file,
    replace_text_in_file,
)

# MARK: Find Issues


def find_aria_label_punctuation_issues(i18n_src_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Find aria label keys that end with inappropriate punctuation.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        The dictionary containing i18n source keys and their associated values.

    Returns
    -------
    Dict[str, str]
        A dictionary mapping incorrect aria label values to their corrected versions.
    """
    aria_label_issues = {}

    punctuation_to_check = f"{string.punctuation}؟"

    for key, value in i18n_src_dict.items():
        if isinstance(value, str) and key.endswith("_aria_label"):
            stripped_value = value.rstrip()
            if stripped_value and stripped_value[-1] in punctuation_to_check:
                # Remove the trailing punctuation.
                corrected_value = stripped_value.rstrip(punctuation_to_check)
                # Preserve any trailing whitespace from original.
                if value.endswith(" "):
                    corrected_value += " "

                aria_label_issues[key] = corrected_value

    return aria_label_issues


# MARK: Report Issues


def report_and_fix_aria_labels(
    aria_label_issues: Dict[str, str], fix: bool = False
) -> None:
    """
    Report aria label punctuation issues and optionally fix them.

    Parameters
    ----------
    aria_label_issues : Dict[str, str]
        Dictionary mapping keys with issues to their corrected values.

    fix : bool, optional
        Whether to automatically fix the issues, by default False.
    """
    if not aria_label_issues:
        rprint(
            "[green]✅ aria_labels: All aria label keys have appropriate punctuation.[/green]"
        )
        return

    error_string = "\n[red]❌ aria_labels errors:\n\n"
    for key, corrected_value in aria_label_issues.items():
        current_value = read_json_file(config_i18n_src_file)[key]
        error_string += f"Key: {key}\n"
        error_string += f"  Current:   '{current_value}'\n"
        error_string += f"  Suggested: '{corrected_value}'\n\n"

    error_string += "[/red][yellow]⚠️ Note: Aria labels should not end with punctuation as it affects screen reader experience.[/yellow]"

    rprint(error_string)

    if not fix:
        rprint(
            "[yellow]💡 Tip: You can automatically fix aria label punctuation by running the --aria-labels (-al) check with the --fix (-f) flag.[/yellow]\n"
        )
        sys.exit(1)

    else:
        json_files = get_all_json_files(config_i18n_directory, path_separator)

        for key, corrected_value in aria_label_issues.items():
            current_value = read_json_file(config_i18n_src_file)[key]

            for json_file in json_files:
                # Replace the full key-value pair in JSON format.
                old_pattern = f'"{key}": "{current_value}"'
                new_pattern = f'"{key}": "{corrected_value}"'
                replace_text_in_file(path=json_file, old=old_pattern, new=new_pattern)

        rprint(
            f"\n[green]✅ Fixed {len(aria_label_issues)} aria label punctuation issues.[/green]\n"
        )
        sys.exit(0)


# MARK: Check Function


def check_aria_labels(fix: bool = False) -> None:
    """
    Main function to check aria label punctuation.

    Parameters
    ----------
    fix : bool, optional, default=False
        Whether to automatically fix issues, by default False.
    """
    i18n_src_dict = read_json_file(file_path=config_i18n_src_file)
    aria_label_issues = find_aria_label_punctuation_issues(i18n_src_dict)
    report_and_fix_aria_labels(aria_label_issues, fix)


if __name__ == "__main__":
    check_aria_labels(fix=False)
