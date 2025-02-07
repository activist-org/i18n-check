# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n target JSON files have keys that are not in es-US.json.
If yes, suggest that they be removed from the their respective JSON files.

Usage:
    python3 src/i18n_check/checks/check_non_source_keys.py
"""

from i18n_check.utils import (
    read_json_file,  
    path_separator,
    en_us_json_file,
    json_file_directory,
    get_all_json_files

)

# MARK: Paths / Files

en_us_json_dict = read_json_file(en_us_json_file)
all_en_us_keys = en_us_json_dict.keys()

# MARK: Non Source Keys

non_source_keys_dict = {}
for json_file in get_all_json_files(json_file_directory, path_separator):
    if json_file.split(path_separator)[-1] != "i18n-src":
        json_dict = read_json_file(json_file)

        all_keys = json_dict.keys()

        if len(all_keys - all_en_us_keys) > 0:
            non_source_keys_dict[json_file.split(path_separator)[-1]] = (
                all_keys - all_en_us_keys
            )

# MARK: Error Outputs

if non_source_keys_dict:
    non_source_keys_string = "\n\n".join(
        f"{k}: {', '.join(non_source_keys_dict[k])}\nTotal: {len(non_source_keys_dict[k])}"
        for k in non_source_keys_dict
    )
    raise ValueError(
        f"There are some i18n target JSON files that have keys that are not in i18n-src. Please remove or rename the following keys:\n\n{non_source_keys_string}\n"
    )

else:
    print(
        "\nSuccess: No i18n target file has keys that are not in the i18n-src source file.\n"
    )
