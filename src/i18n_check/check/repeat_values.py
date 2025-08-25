# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has repeat string values.

If yes, suggest that they be combined using a `_global` sub key at the lowest matching level of i18n-src.

Examples
--------
Run the following script in terminal:

>>> i18n-check -rv
"""

import sys
from collections import Counter
from typing import Dict, List

from rich import print as rprint

from i18n_check.check.invalid_keys import (
    map_keys_to_files,
)
from i18n_check.utils import (
    config_i18n_src_file,
    config_src_directory,
    filter_valid_key_parts,
    lower_and_remove_punctuation,
    path_to_valid_key,
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
    key_file_dict = map_keys_to_files(
        i18n_src_dict=i18n_src_dict,
        src_directory=config_src_directory,
    )
    for repeat_value in json_repeat_value_counts:
        i18n_keys = [
            k
            for k, v in i18n_src_dict.items()
            if repeat_value == lower_and_remove_punctuation(text=v)
            and k[-len("_lower") :] != "_lower"
        ]

        # Needed as we're removing keys that are set to lowercase above.
        if len(i18n_keys) > 1:
            repeat_value_error_report += (
                f"\n\nRepeat value: '{repeat_value}'"
                f"\nNumber of instances: : {json_repeat_value_counts[repeat_value]}"
                f"\nKeys: {', '.join(i18n_keys)}"
            )

        else:
            # Remove the key if the repeat is caused by a lowercase word.
            keys_to_remove.append(repeat_value)

        for k in i18n_keys:
            if k in key_file_dict:
                # Key is used in one file.
                if len(key_file_dict[k]) == 1:
                    formatted_potential_key = path_to_valid_key(key_file_dict[k][0])
                    potential_key_parts: List[str] = formatted_potential_key.split(".")
                    # Is the part in the last key part such that it's a parent directory that's included in the file name.
                    valid_key_parts = filter_valid_key_parts(potential_key_parts)

                    # Get rid of repeat key parts for files that are the same name as their directory.
                    valid_key_parts = [
                        p for p in valid_key_parts if valid_key_parts.count(p) == 1
                    ]

                    ideal_key_base = ".".join(valid_key_parts) + "."

                # Key is used in multiple files.
                else:
                    formatted_potential_keys = [
                        path_to_valid_key(p) for p in key_file_dict[k]
                    ]
                    potential_key_parts = [
                        part for k in formatted_potential_keys for part in k.split(".")
                    ]
                    # Match all entries with their counterparts from other valid key parts.
                    corresponding_valid_key_parts = list(
                        zip(*(k.split(".") for k in formatted_potential_keys))
                    )
                    # Append all parts in order so long as all valid keys share the same part.
                    extended_key_base = ""
                    global_added = False
                    for current_parts in corresponding_valid_key_parts:
                        if len(set(current_parts)) != 1 and not global_added:
                            extended_key_base += "_global."
                            global_added = True

                        if len(set(current_parts)) == 1:
                            extended_key_base += f"{(current_parts)[0]}."
                    # Don't include a key part if it's included in the final one (i.e. organizational sub dir).
                    extended_key_base_split = extended_key_base.split()
                    valid_key_parts = filter_valid_key_parts(extended_key_base_split)

                    ideal_key_base = ".".join(valid_key_parts)

                ideal_key_base = f"i18n.{ideal_key_base}"
                if k[: len(ideal_key_base)] != ideal_key_base:
                    ideal_key = f"{ideal_key_base}{k.split('.')[-1]}"
                    repeat_value_error_report += (
                        f"\nSuggested key change: {k} -> {ideal_key}"
                    )

    for k in keys_to_remove:
        json_repeat_value_counts.pop(k, None)

    return json_repeat_value_counts, repeat_value_error_report


# MARK: Error Outputs


def validate_repeat_values(
    json_repeat_value_counts: Dict[str, int], repeat_value_error_report: str
) -> None:
    """
    Check and report if there are repeat translation values.

    Parameters
    ----------
    json_repeat_value_counts : Dict[str, int]
        A dictionary with repeat i18n values and their counts.

    repeat_value_error_report : str
        An error report including repeat values and changes that should be made.

    Returns
    -------
    None
        This function either exits or prints a success message.

    Raises
    ------
    sys.exit(1)
        The system exits with 1 and prints error details if repeat values are found.
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
        error_message += f"❌ repeat_values error: There {is_or_are} {len(json_repeat_value_counts)} repeat i18n {value_or_values} present in the i18n source file. Please follow the directions below to combine {it_or_them} into one key:\n"
        error_message += repeat_value_error_report
        error_message += "[/red]"

        rprint(error_message)

        sys.exit(1)

    else:
        rprint(
            "[green]✅ repeat_values success: No repeat i18n values found in the i18n-src file.[/green]"
        )


# MARK: Main


if __name__ == "__main__":
    json_repeat_value_counts = get_repeat_value_counts(i18n_src_dict)
    json_repeat_value_counts, repeat_value_error_report = (
        analyze_and_generate_repeat_value_report(
            i18n_src_dict=i18n_src_dict,
            json_repeat_value_counts=json_repeat_value_counts,
        )
    )
    validate_repeat_values(
        json_repeat_value_counts=json_repeat_value_counts,
        repeat_value_error_report=repeat_value_error_report,
    )
