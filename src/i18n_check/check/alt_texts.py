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
from pathlib import Path
from typing import Any

from rich import print as rprint

from i18n_check.utils import (
    PATH_SEPARATOR,
    config_i18n_directory,
    get_all_json_files,
    is_chinese_or_japanese_text,
    is_rtl_text,
    read_json_file,
    replace_text_in_file,
)


# MARK: Find Issues
def _assign_issue(
    alt_text_issues: dict,
    key: Any,
    json_file: str,
    value: Any,
    corrected_value: str,
    stripped_value: Any,
    punctuation_to_check: str,
    index: int,
) -> None:
    """
    Assign a punctuation issue to the alt_text_issues dictionary if required.

    Parameters
    ----------
    alt_text_issues : dict
        Running accumulator of all issues found so far across all the files.
    key : str
        The JSON key of the alt text value being checked.
    json_file : str
        The path of the current JSON file being checked, as a string.
    value : Any
        The original unstripped alt text value from the JSON file.
    corrected_value : str
        The suggested fix for the alt text value with correct punctuation applied.
    stripped_value : str
        The alt text value after stripping leading and trailing whitespace.
    punctuation_to_check : str
        The string of valid punctuation characters to check against.
    index : int
        The character position to check in.

    Returns
    -------
    None
        Check and fix the punctuation issues in alt_text_issues dictionary.
    """

    if stripped_value[index] in punctuation_to_check:
        return
    alt_text_issues.setdefault(key, {})[str(json_file)] = {
        "current_value": value,
        "correct_value": corrected_value,
    }


def _check_json_file(
    json_file_dict: dict,
    alt_text_issues: dict,
    json_file: str,
    punctuation_to_check: str,
) -> None:
    """
    Helper function to check json file and fix appropriate punctuations.

    Parameters
    ----------
    json_file_dict : dict
        The parsed contents of a single JSON file, as a flat dict.
    alt_text_issues : dict
        Running accumulator of all issues found so far across all the files.
    json_file : str
        The path of the current JSON file being checked, as a string.
    punctuation_to_check : str
        The string of valid ending/leading punctuation characters.

    Returns
    -------
    None
        The function iterates, checks and fixes the necessary fields.
    """
    for key, value in json_file_dict.items():
        if isinstance(value, str) and key.endswith("_alt_text"):
            stripped_value = value.strip()
            if not stripped_value:
                continue
            if is_rtl_text(stripped_value):
                _assign_issue(
                    alt_text_issues,
                    key,
                    json_file,
                    value,
                    f".{stripped_value}",
                    stripped_value,
                    punctuation_to_check,
                    0,
                )
            elif is_chinese_or_japanese_text(stripped_value):
                _assign_issue(
                    alt_text_issues,
                    key,
                    json_file,
                    value,
                    f"{stripped_value}\u3002",
                    stripped_value,
                    punctuation_to_check,
                    -1,
                )
            else:
                _assign_issue(
                    alt_text_issues,
                    key,
                    json_file,
                    value,
                    f"{stripped_value}.",
                    stripped_value,
                    punctuation_to_check,
                    -1,
                )


def find_alt_text_punctuation_issues(
    i18n_directory: Path = config_i18n_directory,
) -> dict[str, dict[str, dict[str, str]]]:
    """
    Find alt text keys that don't have appropriate punctuation.

    Parameters
    ----------
    i18n_directory : Path
        The directory containing the i18n JSON files.

    Returns
    -------
    dict[str, dict[str, dict[str, str]]]
        A dictionary mapping incorrect alt text values to their corrected versions.
    """
    json_files = get_all_json_files(directory=i18n_directory)

    punctuation_to_check = f"{string.punctuation}\u061f\u3002"

    alt_text_issues: dict[str, dict[str, dict[str, str]]] = {}
    for json_file in json_files:
        json_file_dict = read_json_file(file_path=json_file)
        _check_json_file(
            json_file_dict, alt_text_issues, json_file, punctuation_to_check
        )

    return alt_text_issues


# MARK: Report Issues


def report_and_fix_alt_texts(
    alt_text_issues: dict[str, dict[str, dict[str, str]]],
    all_checks_enabled: bool = False,
    fix: bool = False,
) -> None:
    """
    Report alt text punctuation issues and optionally fix them.

    Parameters
    ----------
    alt_text_issues : dict[str, dict[str, dict[str, str]]]
        Dictionary mapping keys with issues to their corrected values.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    fix : bool, optional
        Whether to automatically fix the issues, by default False.

    Raises
    ------
    ValueError
        An error is raised and the system prints error details if there are alt texts with invalid punctuation.
    """
    if not alt_text_issues:
        rprint(
            "[green]✅ alt-texts: All alt text keys have appropriate punctuation.[/green]"
        )
        return

    error_string = "\n[red]❌ alt-texts error: There are some values that do not have proper image alt text punctuation. Please follow the directions below to correct them:\n\n"
    for k in alt_text_issues:
        error_string += f"Key: {k}\n"
        for json_file in alt_text_issues[k]:
            error_string += f"  File:      '{json_file.split(PATH_SEPARATOR)[-1]}'\n"

            current_value = alt_text_issues[k][json_file]["current_value"]
            corrected_value = alt_text_issues[k][json_file]["correct_value"]
            error_string += f"  Current:   '{current_value}'\n"
            error_string += f"  Suggested: '{corrected_value}'\n\n"

    error_string += "[/red][yellow]⚠️  Note: Alt texts should end with periods for proper sentence structure and accessibility.[/yellow]"

    rprint(error_string)

    if not fix:
        rprint(
            "[yellow]💡 Tip: You can automatically fix alt text punctuation by running the --alt-texts (-at) check with the --fix (-f) flag.[/yellow]"
        )

        if all_checks_enabled:
            raise ValueError("The alt texts i18n check has failed.")

        else:
            sys.exit(1)

    else:
        total_alt_text_issues = 0
        for k in alt_text_issues:
            for json_file in alt_text_issues[k]:
                current_value = alt_text_issues[k][json_file]["current_value"]
                correct_value = alt_text_issues[k][json_file]["correct_value"]

                # Replace the full key-value pair in JSON format.
                old_pattern = f'"{k}": "{current_value}"'
                new_pattern = f'"{k}": "{correct_value}"'
                replace_text_in_file(path=json_file, old=old_pattern, new=new_pattern)

                total_alt_text_issues += 1

        rprint(
            f"\n[green]✅ Fixed {total_alt_text_issues} alt text punctuation issues.[/green]\n"
        )


# MARK: Check Function


def alt_texts_check_and_fix(
    fix: bool = False, all_checks_enabled: bool = False
) -> bool:
    """
    Main function to check alt text punctuation.

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
    alt_text_issues = find_alt_text_punctuation_issues()
    report_and_fix_alt_texts(
        alt_text_issues=alt_text_issues, all_checks_enabled=all_checks_enabled, fix=fix
    )

    return True
