# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has invalid keys given the files in which they're used.

If yes, suggest new names for the keys based on the lowest possible file level usage.

Examples
--------
Run the following script in terminal:

>>> i18n-check -kn
>>> i18n-check -kn -f  # to fix issues automatically
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from rich import print as rprint

from i18n_check.check.repeat_keys import check_file_keys_repeated
from i18n_check.check.sorted_keys import check_file_keys_sorted
from i18n_check.utils import (
    collect_files_to_check,
    config_file_types_to_check,
    config_global_directories_to_skip,
    config_global_files_to_skip,
    config_i18n_directory,
    config_i18n_src_file,
    config_key_naming_directories_to_skip,
    config_key_naming_files_to_skip,
    config_key_naming_regexes_to_ignore,
    config_repeat_keys_active,
    config_sorted_keys_active,
    config_src_directory,
    filter_valid_key_parts,
    get_all_json_files,
    path_to_valid_key,
    read_json_file,
    replace_text_in_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)

# MARK: Key-Files Dict


def map_keys_to_files(
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    src_directory: Path = config_src_directory,
) -> Dict[str, List[str]]:
    """
    Map i18n keys to the files they are used in.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        The dictionary containing i18n source keys and their associated values.

    src_directory : Path
        The source directory where the files are located.

    Returns
    -------
    Dict[str, List[str]]
        A dictionary where keys are i18n keys and values are lists of file paths where those keys are used.
    """
    files_to_check = collect_files_to_check(
        directory=src_directory,
        file_types_to_check=config_file_types_to_check,
        directories_to_skip=config_key_naming_directories_to_skip,
        files_to_skip=config_key_naming_files_to_skip,
    )

    files_to_check_contents = {}
    for frontend_file in files_to_check:
        with open(frontend_file, "r", encoding="utf-8") as f:
            files_to_check_contents[frontend_file] = f.read()

    all_keys = list(i18n_src_dict.keys())
    key_file_dict: Dict[str, List[str]] = defaultdict(list)
    for k in all_keys:
        key_file_dict[k] = []
        for i, v in files_to_check_contents.items():
            if k in v:
                filepath_from_src = i.split(str(src_directory))[1]
                filepath_from_src = filepath_from_src[1:]
                for file_type in config_file_types_to_check:
                    filepath_from_src = filepath_from_src.replace(file_type, "")

                key_file_dict[k].append(filepath_from_src)

    # Note: This removes empty lists that are unused keys as this is handled by i18n_check_unused_keys.
    return {k: list(set(v)) for k, v in key_file_dict.items() if len(v) > 0}


# MARK: Reduce Keys


def _ignore_key(key: str, keys_to_ignore_regex: List[str]) -> bool:
    """
    Derive whether the key being checked is within the patterns to ignore.

    Parameters
    ----------
    key : str
        The key to that might be ignored if it matches the patterns to skip.

    keys_to_ignore_regex : List[str]
        A list of regex patterns to match with keys that should be ignored during validation.
        Keys matching any of these patterns will be skipped during the audit.
        For backward compatibility, a single string is also accepted and will be converted to a list.

    Returns
    -------
    bool
        Whether the key should be ignored or not in the invalid keys check.
    """
    return any(pattern and re.search(pattern, key) for pattern in keys_to_ignore_regex)


def audit_invalid_i18n_key_names(
    key_file_dict: Dict[str, List[str]],
    keys_to_ignore_regex: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    Audit i18n keys for naming conventions.

    Parameters
    ----------
    key_file_dict : Dict[str, List[str]]
        A dictionary where keys are i18n keys and values are lists of file paths where those keys are used.

    keys_to_ignore_regex : List[str], optional, default=None
        A list of regex patterns to match with keys that should be ignored during validation.
        Keys matching any of these patterns will be skipped during the audit.
        For backward compatibility, a single string is also accepted and will be converted to a list.

    Returns
    -------
    Dict[str, str]
        A dictionary mapping keys that are not named correctly to their suggested corrections.
    """
    if keys_to_ignore_regex is None:
        keys_to_ignore_regex = []

    if isinstance(keys_to_ignore_regex, str):
        keys_to_ignore_regex = [keys_to_ignore_regex] if keys_to_ignore_regex else []

    filtered_key_file_dict = (
        {
            k: v
            for k, v in key_file_dict.items()
            if not _ignore_key(key=k, keys_to_ignore_regex=keys_to_ignore_regex)
        }
        if keys_to_ignore_regex
        else key_file_dict
    )

    invalid_keys_by_name = {}
    for k in filtered_key_file_dict:
        # Key is used in one file.
        if len(filtered_key_file_dict[k]) == 1:
            formatted_potential_key = path_to_valid_key(filtered_key_file_dict[k][0])
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
                path_to_valid_key(p) for p in filtered_key_file_dict[k]
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
            invalid_keys_by_name[k] = ideal_key

    return invalid_keys_by_name


# MARK: Error Outputs


def invalid_key_names_check_and_fix(
    invalid_keys_by_name: Dict[str, str],
    all_checks_enabled: bool = False,
    fix: bool = False,
) -> bool:
    """
    Report and correct invalid i18n key names based on their naming conventions.

    Parameters
    ----------
    invalid_keys_by_name : Dict[str, str]
        A dictionary mapping i18n keys that are not named correctly to their suggested corrections.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    fix : bool, optional, default=False
        If True, automatically corrects the invalid key names in the source files.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if there are invalid keys by name.
    """
    invalid_keys_by_name_string = "".join(
        f"\n{k} -> {v}" for k, v in invalid_keys_by_name.items()
    )
    name_to_be = "are" if len(invalid_keys_by_name) > 1 else "is"
    name_key_to_be = "keys that are" if len(invalid_keys_by_name) > 1 else "key that is"
    name_key_or_keys = "keys" if len(invalid_keys_by_name) > 1 else "key"

    invalid_keys_by_name_error = f"""❌ key-naming error: There {name_to_be} {len(invalid_keys_by_name)} i18n {name_key_to_be} not named correctly.
Please rename the following {name_key_or_keys} \\[current_key -> suggested_correction]:\n{invalid_keys_by_name_string}"""

    if not invalid_keys_by_name:
        rprint(
            "[green]✅ key-naming success: All i18n keys are named correctly in the i18n-src file.[/green]"
        )

    else:
        error_string = "\n[red]"
        error_string += invalid_keys_by_name_error
        error_string += "[/red]"
        rprint(error_string)

        if not fix:
            rprint(
                "\n[yellow]💡 Tip: You can automatically fix invalid key names by running the --key-naming (-kn) check with the --fix (-f) flag.[/yellow]\n"
            )

            if all_checks_enabled:
                raise ValueError("The key naming i18n check has failed.")

            else:
                sys.exit(1)

    if fix and invalid_keys_by_name:
        files_to_fix = collect_files_to_check(
            directory=config_src_directory,
            file_types_to_check=config_file_types_to_check,
            directories_to_skip=config_global_directories_to_skip,
            files_to_skip=config_global_files_to_skip,  # global as we want to fix all instances
        )

        json_files = get_all_json_files(directory=config_i18n_directory)
        all_files_to_fix = json_files + files_to_fix

        # If incorrect key, replace it with the suggested key and give feedback with the replacement.
        for current, correct in invalid_keys_by_name.items():
            for f in all_files_to_fix:
                replace_text_in_file(path=f, old=current, new=correct)

        # Sort all locale files if the sorted-keys and repeat-keys checks are activated.
        if config_sorted_keys_active:
            for json_file in json_files:
                locale_dict = read_json_file(json_file)
                is_sorted, _ = check_file_keys_sorted(locale_dict)

                if not is_sorted:
                    if (
                        config_repeat_keys_active
                        and not check_file_keys_repeated(json_file)[1]
                    ):
                        sorted_locale_dict = dict(sorted(locale_dict.items()))

                        with open(json_file, "w", encoding="utf-8") as lf:
                            json.dump(
                                sorted_locale_dict, lf, indent=2, ensure_ascii=False
                            )
                            lf.write("\n")

                    else:
                        rprint(
                            "\n[yellow]⚠️  Note: JSON key sorting skipped as there are repeat keys (i18n-check -rk)[/yellow]"
                        )

        if all_checks_enabled:
            raise ValueError("The invalid keys i18n check has failed.")

        else:
            sys.exit(1)

    return True


# MARK: Variables

invalid_keys_key_file_dict = map_keys_to_files(
    i18n_src_dict=i18n_src_dict,
    src_directory=config_src_directory,
)
invalid_keys_by_name = audit_invalid_i18n_key_names(
    key_file_dict=invalid_keys_key_file_dict,
    keys_to_ignore_regex=config_key_naming_regexes_to_ignore,
)
