# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if alt text keys (ending with '_alt_text') have appropriate punctuation.

Alt texts should end with periods as they provide descriptive content
that forms complete sentences for screen readers and accessibility tools.

Examples
--------
Run the following script in terminal:

>>> i18n-check -at
>>> i18n-check -at -f  # to fix issues automatically
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


def find_alt_text_punctuation_issues(i18n_src_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Find alt text keys that don't end with appropriate punctuation.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        The dictionary containing i18n source keys and their associated values.

    Returns
    -------
    Dict[str, str]
        A dictionary mapping incorrect alt text values to their corrected versions.
    """
    alt_text_issues = {}

    punctuation_to_check = f"{string.punctuation}؟"

    for key, value in i18n_src_dict.items():
        if isinstance(value, str) and key.endswith("_alt_text"):
            stripped_value = value.rstrip()
            if stripped_value and stripped_value[-1] not in punctuation_to_check:
                corrected_value = f"{stripped_value}."

                alt_text_issues[key] = corrected_value

    return alt_text_issues


# MARK: Report Issues


def report_and_fix_alt_texts(
    alt_text_issues: Dict[str, str], fix: bool = False
) -> None:
    """
    Report alt text punctuation issues and optionally fix them.

    Parameters
    ----------
    alt_text_issues : Dict[str, str]
        Dictionary mapping keys with issues to their corrected values.

    fix : bool, optional
        Whether to automatically fix the issues, by default False.
    """
    if not alt_text_issues:
        rprint(
            "[green]✅ alt_texts: All alt text keys have appropriate punctuation.[/green]"
        )
        return

    error_string = "\n[red]❌ alt_texts errors:\n\n"
    for key, corrected_value in alt_text_issues.items():
        current_value = read_json_file(config_i18n_src_file)[key]
        error_string += f"Key: {key}\n"
        error_string += f"  Current:   '{current_value}'\n"
        error_string += f"  Suggested: '{corrected_value}'\n\n"

    error_string += "[/red][yellow]⚠️ Note: Alt texts should end with periods for proper sentence structure and accessibility.[/yellow]"

    rprint(error_string)

    if not fix:
        rprint(
            "[yellow]💡 Tip: You can automatically fix alt text punctuation by running the --alt-texts (-at) check with the --fix (-f) flag.[/yellow]\n"
        )
        sys.exit(1)

    else:
        json_files = get_all_json_files(config_i18n_directory, path_separator)

        for key, corrected_value in alt_text_issues.items():
            current_value = read_json_file(config_i18n_src_file)[key]

            for json_file in json_files:
                # Replace the full key-value pair in JSON format.
                old_pattern = f'"{key}": "{current_value}"'
                new_pattern = f'"{key}": "{corrected_value}"'
                replace_text_in_file(path=json_file, old=old_pattern, new=new_pattern)

        rprint(
            f"\n[green]✅ Fixed {len(alt_text_issues)} alt text punctuation issues.[/green]\n"
        )
        sys.exit(0)


# MARK: Check Function


def check_alt_texts(fix: bool = False) -> None:
    """
    Main function to check alt text punctuation.

    Parameters
    ----------
    fix : bool, optional, default=False
        Whether to automatically fix issues, by default False.
    """
    i18n_src_dict = read_json_file(file_path=config_i18n_src_file)
    alt_text_issues = find_alt_text_punctuation_issues(i18n_src_dict)
    report_and_fix_alt_texts(alt_text_issues, fix)


if __name__ == "__main__":
    check_alt_texts(fix=False)
