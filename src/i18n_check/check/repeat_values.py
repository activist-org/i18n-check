# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has repeat string values.

If yes, suggest that they be combined using a `_global` sub key at the lowest matching level of i18n-src.

Examples
--------
Run the following script in terminal:

>>> python src/i18n_check/check/repeat_values.py
"""

from collections import Counter
from typing import Dict

from i18n_check.utils import (
    config_i18n_src_file,
    lower_and_remove_punctuation,
    read_json_file,
)

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
    all_json_values = [
        lower_and_remove_punctuation(text=v)
        for v in list(i18n_src_dict.values())
        if isinstance(v, (str, int, float, tuple))  # include only hashable types.
    ]

    return {k: v for k, v in dict(Counter(all_json_values)).items() if v > 1}


def analyze_and_suggest_keys(
    i18n_src_dict: Dict[str, str], json_repeat_value_counts: Dict[str, int]
) -> Dict[str, int]:
    """
    Analyze repeated values and suggest solutions for key modification or removal.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        A dictionary of i18n keys and their corresponding translation strings.

    json_repeat_value_counts : Dict[str, int]
        A dictionary of repeated values and their occurrence counts.

    Returns
    -------
    Dict[str, int]
        The updated dictionary of repeat value counts after suggested changes.
    """
    keys_to_remove = []
    for repeat_value in json_repeat_value_counts:
        i18n_keys = [
            k
            for k, v in i18n_src_dict.items()
            if repeat_value == lower_and_remove_punctuation(text=v)
            and k[-len("_lower") :] != "_lower"
        ]

        # Needed as we're removing keys that are set to lowercase above.
        if len(i18n_keys) > 1:
            print(f"\nRepeat value: '{repeat_value}'")
            print(f"Number of instances: : {json_repeat_value_counts[repeat_value]}")
            print(f"Keys: {', '.join(i18n_keys)}")

            common_prefix = ""
            min_key_length = min(len(k) for k in i18n_keys)
            common_character = True
            while common_character:
                for i in range(min_key_length):
                    if len({k[i] for k in i18n_keys}) == 1:
                        common_prefix += i18n_keys[0][i]

                    else:
                        common_character = False
                        break

                common_character = False

            # Replace '._global' to allow for suggestions at the same global level without repeat globals.
            if common_prefix := ".".join(common_prefix.split(".")[:-1]).replace(
                "._global", ""
            ):
                print(f"Suggested new key: {common_prefix}._global.IDENTIFIER_KEY")

            else:
                print("Suggested new key: i18n._global.IDENTIFIER_KEY")

        else:
            # Remove the key if the repeat is caused by a lowercase word.
            keys_to_remove.append(repeat_value)

    for k in keys_to_remove:
        json_repeat_value_counts.pop(k, None)

    return json_repeat_value_counts


# MARK: Error Outputs


def validate_repeat_values(json_repeat_value_counts: Dict[str, int]) -> None:
    """
    Check and report if there are repeat translation values.

    Parameters
    ----------
    json_repeat_value_counts : Dict[str, int]
        A dictionary with repeat i18n values and their counts.

    Returns
    -------
    None
        This function either raises a ValueError or prints a success message.

    Raises
    ------
    ValueError
        If repeat values are found, a ValueError is raised with details.
    """
    if json_repeat_value_counts:
        if len(json_repeat_value_counts) == 1:
            value_to_be = "value is"

        else:
            value_to_be = "values are"

        raise ValueError(
            f"\nrepeat_values failure: {len(json_repeat_value_counts)} repeat i18n {value_to_be} present. Please combine given the suggestions above.\n"
        )

    else:
        print(
            "repeat_values success: No repeat i18n values found in the i18n-src file."
        )


# MARK: Main


if __name__ == "__main__":
    json_repeat_value_counts = get_repeat_value_counts(i18n_src_dict)
    analyze_and_suggest_keys(
        i18n_src_dict=i18n_src_dict, json_repeat_value_counts=json_repeat_value_counts
    )
    validate_repeat_values(json_repeat_value_counts=json_repeat_value_counts)
