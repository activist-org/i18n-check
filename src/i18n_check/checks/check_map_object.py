# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks the i18nMap object to make sure that it's in sync with the base localization file.

Usage:
    python3 src/i18n_check/checks/check_map_object.py
"""

import json
from i18n_check.utils import (
    read_json_file,
    en_us_json_file,
    frontend_types_dir,
    flatten_nested_dict,
    )
# MARK: Load Base i18n

en_us_json_dict = read_json_file(en_us_json_file)

flat_en_us_json_dict = {k: k for k, _ in en_us_json_dict.items()}

# MARK: Load i18n Map

with open(frontend_types_dir / "i18n-map.ts", encoding="utf-8") as f:
    i18n_object_list = f.readlines()

    i18n_object_list_with_key_quotes = []
    for i, line in enumerate(i18n_object_list):
        if i != 0 or i != len(i18n_object_list):
            line = line.strip()
            if line and line[0] != '"':
                line = '"' + line.replace(":", '":', 1)
            i18n_object_list_with_key_quotes.append(line)

    i18n_object = (
        "".join(i18n_object_list_with_key_quotes)
        .replace("export const i18nMap = ", "")
        .replace("};", "}")
        .replace('"{', "{")
        .replace('"}', "}")
        .replace(",}", "}")
    )
    i18n_object_dict = json.loads(i18n_object)


# MARK: Flatten i18n Obj





flat_i18n_object_dict = flatten_nested_dict(i18n_object_dict)

# MARK: Compare Dicts

assert flat_en_us_json_dict == flat_i18n_object_dict, (
    "\nThe current i18nMap object doesn't match the base i18n JSON file. Please re-generate the i18nMap object.\n"
)

print("\nSuccess: The current i18nMap object matches the base i18n JSON file.\n")
