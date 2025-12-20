# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has repeat string values.

If yes, suggest that they be combined using a `_global` sub key at the lowest matching level of i18n-src.

Examples
--------
Run the following script in terminal:

>>> i18n-check -rv
"""

import itertools
import sys
from collections import Counter
from typing import Dict

from rich import print as rprint

from i18n_check.check.key_naming import audit_invalid_i18n_key_names, map_keys_to_files
from i18n_check.utils import (
    config_i18n_src_file,
    config_key_naming_regexes_to_ignore,
    config_src_directory,
    lower_and_remove_punctuation,
    read_json_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)

# MARK: Repeat Values


def get_repeat_value_counts(i18n_src_dict: Dict[str, str]) -> Dict[str, int]:
    """
    Count repeated values in the i18n source dictionary.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        The dictionary containing i18n keys and their associated values.

    Returns
    -------
    Dict[str, int]
        A dictionary with values that appear more than once, mapped to their count.
    """
    # Note: The following automatically removes repeat keys from i18n_src_dict.
    all_json_values = [
        lower_and_remove_punctuation(text=v)
        for v in list(i18n_src_dict.values())
        if isinstance(v, (str, int, float, tuple))  # include only hashable types.
    ]

    return {k: v for k, v in dict(Counter(all_json_values)).items() if v > 1}


def analyze_and_generate_repeat_value_report(
    i18n_src_dict: Dict[str, str], json_repeat_value_counts: Dict[str, int]
) -> tuple[Dict[str, int], str]:
    """
    Analyze repeated values and generates a report of repeat values with changes that should be made.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        A dictionary of i18n keys and their corresponding translation strings.

    json_repeat_value_counts : Dict[str, int]
        A dictionary of repeated values and their occurrence counts.

    Returns
    -------
    Dict[str, int], str
        The updated dictionary of repeat value counts after suggested changes and a report to be added to the error.
    """
    repeat_value_error_report = ""

    keys_to_remove = []
    for repeat_value in json_repeat_value_counts:
        repeat_value_i18n_keys = [
            k
            for k, v in i18n_src_dict.items()
            if repeat_value == lower_and_remove_punctuation(text=v)
            and k[-len("_lower") :] != "_lower"
        ]

        # Needed as we're removing keys that are set to lowercase above.
        if len(repeat_value_i18n_keys) > 1:
            repeat_value_error_report += (
                f"\n\nRepeat value: '{repeat_value}'"
                f"\nNumber of instances: {len(repeat_value_i18n_keys)}"
                f"\nKeys: {', '.join(repeat_value_i18n_keys)}"
            )

            # Use the methods from the invalid keys check to assure that results are consistent.
            repeat_values_key_file_dict = map_keys_to_files(
                i18n_src_dict={
                    k: v
                    for k, v in i18n_src_dict.items()
                    if k in repeat_value_i18n_keys
                },
                src_directory=config_src_directory,
            )

            # Replace with 'repeat_key' as a dummy for if this was the key in all files.
            repeat_key_key_file_dict = {
                "repeat_key": list(
                    itertools.chain.from_iterable(repeat_values_key_file_dict.values())
                )
            }

            invalid_keys_by_name = audit_invalid_i18n_key_names(
                key_file_dict=repeat_key_key_file_dict,
                keys_to_ignore_regex=config_key_naming_regexes_to_ignore,
            )

            # Remove dummy value and add 'content_reference' for user to replace.
            if "repeat_key" in invalid_keys_by_name:
                valid_key_stub_based_on_files = invalid_keys_by_name[
                    "repeat_key"
                ].replace(".repeat_key", "")

            else:
                # In case there are keys that aren't used in files (i.e. central i18n repo).
                valid_key_stub_based_on_files = "i18n"

            repeat_value_error_report += f"\nSuggested new key: {valid_key_stub_based_on_files}.content_reference"

        else:
            # Remove the key if the repeat is caused by a lowercase word.
            keys_to_remove.append(repeat_value)

    for k in keys_to_remove:
        json_repeat_value_counts.pop(k, None)

    return json_repeat_value_counts, repeat_value_error_report


# MARK: Error Outputs


def repeat_values_check(
    json_repeat_value_counts: Dict[str, int],
    repeat_value_error_report: str,
    all_checks_enabled: bool = False,
) -> bool:
    """
    Check and report if there are repeat translation values.

    Parameters
    ----------
    json_repeat_value_counts : Dict[str, int]
        A dictionary with repeat i18n values and their counts.

    repeat_value_error_report : str
        An error report including repeat values and changes that should be made.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if repeat values are found.
    """
    if json_repeat_value_counts:
        is_or_are = "is"
        it_or_them = "it"
        value_or_values = "value"
        if len(json_repeat_value_counts) > 1:
            is_or_are = "are"
            it_or_them = "them"
            value_or_values = "values"

        error_message = "\n[red]"
        error_message += f"❌ repeat-values error: There {is_or_are} {len(json_repeat_value_counts)} repeat i18n {value_or_values} present in the i18n source file. Please follow the directions below to combine {it_or_them} into one key:"
        error_message += repeat_value_error_report
        error_message += "[/red]"

        rprint(error_message)

        if all_checks_enabled:
            raise ValueError("The repeat values i18n check has failed.")

        else:
            sys.exit(1)

    else:
        rprint(
            "[green]✅ repeat-values success: No repeat i18n values found in the i18n-src file.[/green]"
        )

    return True


# MARK: Variables

json_repeat_value_counts = get_repeat_value_counts(i18n_src_dict)
json_repeat_value_counts, repeat_value_error_report = (
    analyze_and_generate_repeat_value_report(
        i18n_src_dict=i18n_src_dict,
        json_repeat_value_counts=json_repeat_value_counts,
    )
)
