# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n target JSON files have keys that are not in the source file.
If yes, suggest that they be removed from the their respective JSON files.

Usage:
    python3 src/i18n_check/check/non_source_keys.py
"""

from i18n_check.utils import (
    get_all_json_files,
    i18n_directory,
    i18n_src_file,
    path_separator,
    read_json_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=i18n_src_file)
all_src_keys = i18n_src_dict.keys()

# MARK: Non Source Keys

non_source_keys_dict = {}
for json_file in get_all_json_files(i18n_directory, path_separator):
    if (
        json_file.split(path_separator)[-1]
        != str(i18n_src_file).split(path_separator)[-1]
    ):
        json_dict = read_json_file(json_file)

        all_keys = json_dict.keys()

        if len(all_keys - all_src_keys) > 0:
            non_source_keys_dict[json_file.split(path_separator)[-1]] = (
                all_keys - all_src_keys
            )

# MARK: Error Outputs

if non_source_keys_dict:
    non_source_keys_string = "\n\n".join(
        f"{k}: {', '.join(non_source_keys_dict[k])}\nTotal: {len(non_source_keys_dict[k])}"
        for k in non_source_keys_dict
    )
    raise ValueError(
        f"\nnon_source_keys failure: There are some i18n target JSON files that have keys that are not in en-US.json. Please remove or rename the following keys:\n\n{non_source_keys_string}\n"
    )

else:
    print(
        "non_source_keys success: No i18n target file has keys that are not in the en-US.json source file."
    )
