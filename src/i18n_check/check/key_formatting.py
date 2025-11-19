# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if the i18n-src file has invalid keys given their formatting.

Examples
--------
Run the following script in terminal:

>>> i18n-check -kf
>>> i18n-check -kf -f  # to fix issues automatically
"""

import re
import sys
from typing import Dict, List, Optional

from rich import print as rprint

from i18n_check.check.key_naming import invalid_keys_key_file_dict
from i18n_check.utils import (
    config_i18n_src_file,
    config_invalid_key_regexes_to_ignore,
    is_valid_key,
    read_json_file,
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
) -> List[str]:
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
    List[str]
        A list of keys that are not formatted correctly.
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

    invalid_keys_by_format = []
    for k in filtered_key_file_dict:
        if not is_valid_key(k):
            invalid_keys_by_format.append(k)

    return invalid_keys_by_format


# MARK: Error Outputs


def invalid_key_formats_check(
    invalid_keys_by_format: List[str],
    all_checks_enabled: bool = False,
) -> bool:
    """
    Report invalid i18n keys based on their formatting conventions.

    Parameters
    ----------
    invalid_keys_by_format : List[str]
        A list of i18n keys that are not formatted correctly.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if there are invalid keys by format.
    """
    invalid_keys_by_format_string = ", ".join(invalid_keys_by_format)
    format_to_be = "are" if len(invalid_keys_by_format) > 1 else "is"
    format_key_to_be = (
        "keys that are" if len(invalid_keys_by_format) > 1 else "key that is"
    )
    format_key_or_keys = "keys" if len(invalid_keys_by_format) > 1 else "key"

    invalid_keys_by_format_error = f"""❌ key_formatting error: There {format_to_be} {len(invalid_keys_by_format)} i18n {format_key_to_be} not formatted correctly. Please reformat the following {format_key_or_keys}:\n\n{invalid_keys_by_format_string}"""

    if not invalid_keys_by_format:
        rprint(
            "[green]✅ key_formatting success: All i18n keys are formatted correctly in the i18n-src file.[/green]"
        )

    else:
        error_string = "\n[red]"
        error_string += invalid_keys_by_format_error
        error_string += "[/red]"
        rprint(error_string)

        if all_checks_enabled:
            raise ValueError("The key formatting i18n check has failed.")

        else:
            sys.exit(1)

    return True


# MARK: Variables

invalid_keys_by_format = audit_invalid_i18n_key_formats(
    key_file_dict=invalid_keys_key_file_dict,
    keys_to_ignore_regex=config_invalid_key_regexes_to_ignore,
)
