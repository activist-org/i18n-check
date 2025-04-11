# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks for duplicate keys in i18n JSON files using JSON parsing.
Identifies exact key duplicates that might occur during mass replacements.

Usage
-----
python3 src/i18n_check/check/non_source_keys.py
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from i18n_check.utils import get_all_json_files, i18n_directory, path_separator


def find_duplicate_keys(json_str: str) -> Dict[str, List[str]]:
    """
    Identifies duplicate keys using JSON parser with custom hook.
    """
    grouped = defaultdict(list)

    def check_duplicates(pairs) -> Dict:
        for key, value in pairs:
            grouped[key].append(str(value))

        return dict(pairs)

    try:
        json.loads(json_str, object_pairs_hook=check_duplicates)
        duplicates = {
            k: values_list for k, values_list in grouped.items() if len(values_list) > 1
        }
        return duplicates

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def check_file(file_path: str) -> Tuple[str, Dict[str, List[str]]]:
    """
    Checks a single JSON file for duplicates.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return (Path(file_path).name, find_duplicate_keys(content))


def main() -> None:
    """
    Main check execution.
    """
    json_files = get_all_json_files(i18n_directory, path_separator)
    has_errors = False

    for json_file in json_files:
        filename, duplicates = check_file(json_file)
        if duplicates:
            has_errors = True
            print(f"\nDuplicate keys in {filename}:")

            for key, values in duplicates.items():
                print(f"  '{key}' appears {len(values)} times with values: {values}")

    if has_errors:
        raise ValueError(
            "\nrepeat_keys failure: Duplicate keys found. All i18n keys must be unique."
        )

    print("repeat_keys success: No duplicate keys found in i18n files.")


if __name__ == "__main__":
    main()
