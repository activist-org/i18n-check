# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has invalid keys given their usage or formatting.

If yes, suggest new names for the keys at the lowest possible level of usage.

Examples
--------
Run the following script in terminal:

>>> python3 src/i18n_check/check/key_identifiers.py
"""

from collections import defaultdict
from typing import Dict, List

from i18n_check.utils import (
    collect_files_to_check,
    file_types_to_check,
    files_to_skip,
    filter_valid_key_parts,
    i18n_src_file,
    is_valid_key,
    key_identifiers_skip,
    path_to_valid_key,
    read_json_file,
    src_directory,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=i18n_src_file)

files_to_check = collect_files_to_check(
    directory=src_directory,
    file_types=file_types_to_check,
    directories_to_skip=key_identifiers_skip,
    files_to_skip=files_to_skip,
)

file_to_check_contents = {}
for frontend_file in files_to_check:
    with open(frontend_file, "r", encoding="utf-8") as f:
        file_to_check_contents[frontend_file] = f.read()

# MARK: Key-Files Dict

all_keys = list(i18n_src_dict.keys())
key_file_dict: Dict[str, List[str]] = defaultdict()
for k in all_keys:
    key_file_dict[k] = []
    for i, v in file_to_check_contents.items():
        if k in v:
            filepath_from_src = i.split(str(src_directory))[1]
            filepath_from_src = filepath_from_src[1:]
            for file_type in file_types_to_check:
                filepath_from_src = filepath_from_src.replace(file_type, "")

            key_file_dict[k].append(filepath_from_src)

# Note: This removes empty lists that are unused keys as this is handled by i18n_check_unused_keys.
key_file_dict = {k: list(set(v)) for k, v in key_file_dict.items() if len(v) > 0}

# MARK: Reduce Keys

invalid_keys_by_format = []
invalid_keys_by_name = {}
for k in key_file_dict:
    if not is_valid_key(k):
        invalid_keys_by_format.append(k)

    # Key is used in one file.
    if len(key_file_dict[k]) == 1:
        formatted_potential_key = path_to_valid_key(key_file_dict[k][0])
        potential_key_parts: List[str] = formatted_potential_key.split(".")
        # Is the part in the last key part such that it's a parent directory that's included in the file name.
        valid_key_parts = filter_valid_key_parts(potential_key_parts)

        # Get rid of repeat key parts for files that are the same name as their directory.
        valid_key_parts = [p for p in valid_key_parts if valid_key_parts.count(p) == 1]

        ideal_key_base = ".".join(valid_key_parts) + "."

    # Key is used in multiple files.
    else:
        formatted_potential_keys = [path_to_valid_key(p) for p in key_file_dict[k]]
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

    if k[: len(ideal_key_base)] != ideal_key_base:
        ideal_key = f"{ideal_key_base}{k.split('.')[-1]}"
        invalid_keys_by_name[k] = ideal_key

# MARK: Error Outputs

invalid_keys_by_format_string = ", ".join(invalid_keys_by_format)
format_to_be = "are" if len(invalid_keys_by_format) > 1 else "is"
format_key_to_be = "keys that are" if len(invalid_keys_by_format) > 1 else "key that is"
format_key_or_keys = "keys" if len(invalid_keys_by_format) > 1 else "key"

invalid_keys_by_format_error = f"""
There {format_to_be} {len(invalid_keys_by_format)} i18n {format_key_to_be} not formatted correctly. Please reformat the following {format_key_or_keys}:\n\n{invalid_keys_by_format_string}
"""

invalid_keys_by_name_string = "".join(
    f"\n{k} -> {v}" for k, v in invalid_keys_by_name.items()
)
name_to_be = "are" if len(invalid_keys_by_name) > 1 else "is"
name_key_to_be = "keys that are" if len(invalid_keys_by_name) > 1 else "key that is"
name_key_or_keys = "keys" if len(invalid_keys_by_name) > 1 else "key"

invalid_keys_by_name_error = f"""
There {name_to_be} {len(invalid_keys_by_name)} i18n {name_key_to_be} not named correctly. Please rename the following {name_key_or_keys} [current_key -> suggested_correction]:\n{invalid_keys_by_name_string}
"""

error_string = ""

if not invalid_keys_by_format and not invalid_keys_by_name:
    print(
        "key_identifiers success: All i18n keys are formatted and named correctly in the i18n-src file."
    )

elif invalid_keys_by_format and invalid_keys_by_name:
    error_string += invalid_keys_by_format_error
    error_string += invalid_keys_by_name_error
    raise ValueError(error_string)

else:
    if invalid_keys_by_format:
        error_string += invalid_keys_by_format_error

    else:
        print(
            "\nkey_identifiers failure: There is an error with key names, but all i18n keys are formatted correctly in the i18n-src file.\n"
        )

    if invalid_keys_by_name:
        error_string += invalid_keys_by_name_error

    else:
        print(
            "\nkey_identifiers failure: There is an error with key formatting, but all i18n keys are named appropriately in the i18n-src file.\n"
        )

    raise ValueError(error_string)
