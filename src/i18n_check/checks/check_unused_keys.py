# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has keys that are not used in the codebase.
If yes, suggest that they be removed from the i18n-src.

Usage:
    python3 src/i18n_check/checks/check_unused_keys.py
"""

import json
import os
import re
from pathlib import Path

# MARK: Paths / Files

i18n_check_dir = str(Path(__file__).parent.resolve())
json_file_directory = Path(__file__).parent.parent.resolve()
frontend_directory = Path(__file__).parent.parent.parent.resolve()

file_types_to_check = [".vue", ".ts", ".js"]
directories_to_skip = [
    i18n_check_dir,
    str((frontend_directory / ".nuxt").resolve()),
    str((frontend_directory / ".output").resolve()),
    str((frontend_directory / "node_modules").resolve()),
]
files_to_skip = ["i18n-map.ts"]

with open(json_file_directory / "i18n-src", encoding="utf-8") as f:
    en_us_json_dict = json.loads(f.read())

files_to_check = []
for root, dirs, files in os.walk(frontend_directory):
    files_to_check.extend(
        os.path.join(root, file)
        for file in files
        if all(root[: len(d)] != d for d in directories_to_skip)
        and any(file[-len(t) :] == t for t in file_types_to_check)
        and file not in files_to_skip
    )

file_to_check_contents = {}
for frontend_file in files_to_check:
    with open(frontend_file, "r", encoding="utf-8") as f:
        file_to_check_contents[frontend_file] = f.read()

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
        f"There {to_be} {len(unused_keys)} i18n {key_to_be} unused. Please remove or assign the following {key_or_keys}:\n\n{', '.join(unused_keys)}\n"
    )

else:
    print(
        "\nSuccess: All i18n keys in the en-US source file are used in the project.\n"
    )
