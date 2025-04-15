# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks the i18n keys used in the project and makes sure that each of them appears in the i18n-src file.

If there are invalid keys, alert the user to their presence.

Usage
-----
python3 src/i18n_check/check/invalid_keys.py
"""

import os
import re
from typing import Any, List, Set

from i18n_check.utils import (
    collect_files_to_check,
    file_types_to_check,
    files_to_skip,
    i18n_src_file,
    invalid_keys_skip,
    read_json_file,
    src_directory,
)

# MARK: Paths / Files

# Check for Windows and derive directory path separator.
path_separator = "\\" if os.name == "nt" else "/"

i18n_src_dict = read_json_file(file_path=i18n_src_file)

files_to_check = collect_files_to_check(
    directory=src_directory,
    file_types=file_types_to_check,
    directories_to_skip=invalid_keys_skip,
    files_to_skip=files_to_skip,
)

file_to_check_contents = {}
for frontend_file in files_to_check:
    with open(frontend_file, "r", encoding="utf-8") as f:
        file_to_check_contents[frontend_file] = f.read()

# MARK: Key Comparisons

all_keys = i18n_src_dict.keys()

i18n_key_pattern_quote = r"\'i18n\.[_\S\.]+?\'"
i18n_key_pattern_double_quote = r"\"i18n\.[_\S\.]+?\""
i18n_key_pattern_back_tick = r"\`i18n\.[_\S\.]+?\`"
all_i18n_key_patterns = [
    i18n_key_pattern_quote,
    i18n_key_pattern_double_quote,
    i18n_key_pattern_back_tick,
]

all_used_i18n_keys: Set[Any] = set()
for v in file_to_check_contents.values():
    all_file_i18n_keys: List[Any] = []
    all_file_i18n_keys.extend(
        re.findall(i18n_kp, v) for i18n_kp in all_i18n_key_patterns
    )
    # Remove the first and last characters that are the quotes or back ticks.
    all_file_i18n_keys = [k[1:-1] for ks in all_file_i18n_keys for k in ks]

    all_used_i18n_keys.update(all_file_i18n_keys)

all_used_i18n_keys = set(all_used_i18n_keys)

if invalid_keys := list(all_used_i18n_keys - all_keys):
    to_be = "are" if len(invalid_keys) > 1 else "is"
    key_to_be = "keys that are" if len(invalid_keys) > 1 else "key that is"
    key_or_keys = "keys" if len(invalid_keys) > 1 else "key"
    raise ValueError(
        f"\ninvalid_keys failure: There {to_be} {len(invalid_keys)} i18n {key_to_be} not in the en-US source file. Please check the validity of the following {key_or_keys}:\n\n{', '.join(invalid_keys)}\n"
    )

else:
    print(
        "invalid_keys success: All i18n keys that are used in the project are in the en-US source file."
    )
