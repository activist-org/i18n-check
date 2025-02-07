# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has keys that are not used in the codebase.
If yes, suggest that they be removed from the i18n-src.

Usage:
    python3 src/i18n_check/checks/check_unused_keys.py
"""



from i18n_check.utils import (
    read_json_file,  
    en_us_json_file,
    collect_files,
    frontend_directory,
    file_types_to_check, 
    directories_to_skip,
    read_files_to_dict,
)

# MARK: Paths / Files

files_to_skip = ["i18n-map.ts"]

en_us_json_dict = read_json_file(en_us_json_file)

files_to_check = collect_files(frontend_directory, file_types_to_check, directories_to_skip, files_to_skip)

file_to_check_contents = read_files_to_dict(files_to_check)

# MARK: Unused Keys

all_keys = list(en_us_json_dict.keys())
used_keys = []
for k in all_keys:
    # Allow for i18nMap keys that are sometimes split  to be found.
    key_search_pattern = r"[\s\S]*\.".join(k.split("."))
    for file_contents in file_to_check_contents.values():
        if re.search(key_search_pattern, file_contents):
            break

# MARK: Error Outputs

if unused_keys := list(set(all_keys) - set(used_keys)):
    to_be = "are" if len(unused_keys) > 1 else "is"
    key_to_be = "keys that are" if len(unused_keys) > 1 else "key that is"
    key_or_keys = "keys" if len(unused_keys) > 1 else "key"
    raise ValueError(
        f"\ncheck_unused_keys failure: There {to_be} {len(unused_keys)} i18n {key_to_be} unused. Please remove or assign the following {key_or_keys}:\n\n{', '.join(unused_keys)}\n"
    )

else:
    print(
        "check_unused_keys success: All i18n keys in the i18n-src file are used in the project."
    )
