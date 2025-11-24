# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has invalid keys given their formatting.

Examples
--------
Run the following script in terminal:

>>> i18n-check -kf
>>> i18n-check -kf -f  # to fix issues automatically
"""

import json
import re
import sys
from typing import Dict, List, Optional

from rich import print as rprint

from i18n_check.check.key_naming import invalid_keys_key_file_dict
from i18n_check.check.repeat_keys import check_file_keys_repeated
from i18n_check.check.sorted_keys import check_file_keys_sorted
from i18n_check.utils import (
    collect_files_to_check,
    config_file_types_to_check,
    config_global_directories_to_skip,
    config_global_files_to_skip,
    config_i18n_directory,
    config_i18n_src_file,
    config_key_formatting_regexes_to_ignore,
    config_repeat_keys_active,
    config_sorted_keys_active,
    config_src_directory,
    get_all_json_files,
    is_valid_key,
    read_json_file,
    replace_text_in_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)


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


def audit_invalid_i18n_key_formats(
    key_file_dict: Dict[str, List[str]],
    keys_to_ignore_regex: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    Audit i18n keys for formatting conventions.

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
        A dictionary mapping invalid keys to their corrected format.
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

    invalid_keys_by_format = {}
    for k in filtered_key_file_dict:
        if not is_valid_key(k):
            # Convert hyphens to underscores and any other invalid characters.
            corrected_key = k.replace("-", "_")
            # Remove any other invalid characters (keep only alphanumeric, dots, and underscores).
            corrected_key = re.sub(r"[^a-zA-Z0-9._]", "_", corrected_key)
            invalid_keys_by_format[k] = corrected_key

    return invalid_keys_by_format


# MARK: Error Outputs


def invalid_key_formats_check_and_fix(
    invalid_keys_by_format: Dict[str, str],
    all_checks_enabled: bool = False,
    fix: bool = False,
) -> bool:
    """
    Report and correct invalid i18n keys based on their formatting conventions.

    Parameters
    ----------
    invalid_keys_by_format : Dict[str, str]
        A dictionary mapping i18n keys that are not formatted correctly to their suggested corrections.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    fix : bool, optional, default=False
        If True, automatically corrects the invalid key formats in the source files.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if there are invalid keys by format.
    """
    invalid_keys_by_format_string = "".join(
        f"\n{k} -> {v}" for k, v in invalid_keys_by_format.items()
    )
    format_to_be = "are" if len(invalid_keys_by_format) > 1 else "is"
    format_key_to_be = (
        "keys that are" if len(invalid_keys_by_format) > 1 else "key that is"
    )
    format_key_or_keys = "keys" if len(invalid_keys_by_format) > 1 else "key"

    invalid_keys_by_format_error = f"""❌ key-formatting error: There {format_to_be} {len(invalid_keys_by_format)} i18n {format_key_to_be} not formatted correctly.
Please reformat the following {format_key_or_keys} [current_key -> suggested_correction]:\n{invalid_keys_by_format_string}"""

    if not invalid_keys_by_format:
        rprint(
            "[green]✅ key-formatting success: All i18n keys are formatted correctly in the i18n-src file.[/green]"
        )

    else:
        error_string = "\n[red]"
        error_string += invalid_keys_by_format_error
        error_string += "[/red]"
        rprint(error_string)

        if not fix:
            rprint(
                "\n[yellow]💡 Tip: You can automatically fix invalid key formats by running the --key-formatting (-kf) check with the --fix (-f) flag.[/yellow]\n"
            )

            if all_checks_enabled:
                raise ValueError("The key formatting i18n check has failed.")

            else:
                sys.exit(1)

    if fix and invalid_keys_by_format:
        files_to_fix = collect_files_to_check(
            directory=config_src_directory,
            file_types_to_check=config_file_types_to_check,
            directories_to_skip=config_global_directories_to_skip,
            files_to_skip=config_global_files_to_skip,
        )

        json_files = get_all_json_files(directory=config_i18n_directory)
        all_files_to_fix = json_files + files_to_fix

        # Replace each incorrect key with the corrected format.
        for current, correct in invalid_keys_by_format.items():
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
            raise ValueError("The key formatting i18n check has failed.")

        else:
            sys.exit(1)

    return True


# MARK: Variables

invalid_keys_by_format = audit_invalid_i18n_key_formats(
    key_file_dict=invalid_keys_key_file_dict,
    keys_to_ignore_regex=config_key_formatting_regexes_to_ignore,
)
