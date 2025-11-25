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
import unicodedata
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

# MARK: Text Direction


def is_rtl_text(text: str) -> bool:
    """
    Check if the text contains RTL (right-to-left) characters.

    Parameters
    ----------
    text : str
        The text to check.

    Returns
    -------
    bool
        True if the text contains RTL characters, False otherwise.
    """
    if not text:
        return False

    rtl_categories = [
        "R",  # right-to-left (e.g. Arabic, Hebrew)
        "AL",  # right-to-left Arabic
    ]

    for char in text:
        bc = unicodedata.bidirectional(char)
        if bc in rtl_categories:
            return True

    return False


# MARK: Find Issues


def find_alt_text_punctuation_issues(
    i18n_directory: Path = config_i18n_directory,
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Find alt text keys that don't have appropriate punctuation.

    Parameters
    ----------
    i18n_directory : Path
        The directory containing the i18n JSON files.

    Returns
    -------
    Dict[str, Dict[str, Dict[str, str]]]
        A dictionary mapping incorrect alt text values to their corrected versions.
    """
    json_files = get_all_json_files(directory=i18n_directory)

    punctuation_to_check = f"{string.punctuation}؟"

    alt_text_issues: Dict[str, Dict[str, Dict[str, str]]] = {}
    for json_file in json_files:
        json_file_dict = read_json_file(file_path=json_file)

        for key, value in json_file_dict.items():
            if isinstance(value, str) and key.endswith("_alt_text"):
                stripped_value = value.strip()
                if not stripped_value:
                    continue

                if is_rtl_text(stripped_value):
                    # The period should be at position 0 for RTL text.
                    if stripped_value[0] not in punctuation_to_check:
                        corrected_value = f".{stripped_value}"

                        if key not in alt_text_issues:
                            alt_text_issues[key] = {}

                        alt_text_issues[key][str(json_file)] = {
                            "current_value": value,
                            "correct_value": corrected_value,
                        }

                elif stripped_value[-1] not in punctuation_to_check:
                    corrected_value = f"{stripped_value}."

                    if key not in alt_text_issues:
                        alt_text_issues[key] = {}

                    alt_text_issues[key][str(json_file)] = {
                        "current_value": value,
                        "correct_value": corrected_value,
                    }

    return alt_text_issues


# MARK: Report Issues


def report_and_fix_alt_texts(
    alt_text_issues: Dict[str, Dict[str, Dict[str, str]]],
    all_checks_enabled: bool = False,
    fix: bool = False,
) -> None:
    """
    Report alt text punctuation issues and optionally fix them.

    Parameters
    ----------
    alt_text_issues : Dict[str, Dict[str, Dict[str, str]]]
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

    error_string = "\n[red]❌ alt-texts errors:\n\n"
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
            "[yellow]💡 Tip: You can automatically fix alt text punctuation by running the --alt-texts (-at) check with the --fix (-f) flag.[/yellow]\n"
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
