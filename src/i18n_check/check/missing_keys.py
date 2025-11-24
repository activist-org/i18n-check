# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks if target locale files are missing keys that exist in the source file.

A key is considered missing if it's not present or if its value is an empty string.

Examples
--------
Run the following script in terminal:

>>> i18n-check -mk
>>> i18n-check -mk -f -l ENTER_ISO_2_CODE  # interactive mode to add missing keys
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich import print as rprint
from rich.prompt import Prompt

from i18n_check.check.key_naming import map_keys_to_files
from i18n_check.check.repeat_keys import check_file_keys_repeated
from i18n_check.utils import (
    PATH_SEPARATOR,
    config_i18n_directory,
    config_i18n_src_file,
    config_missing_keys_locales_to_check,
    config_repeat_keys_active,
    config_sorted_keys_active,
    config_src_directory,
    get_all_json_files,
    read_json_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)

# MARK: Missing Keys


def get_missing_keys_by_locale(
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    i18n_directory: Path = config_i18n_directory,
    locales_to_check: List[str] = config_missing_keys_locales_to_check,
) -> Dict[str, Tuple[List[str], float]]:
    """
    Get missing keys for each locale file compared to the source dictionary.

    Parameters
    ----------
    i18n_src_dict : dict
        The dictionary containing i18n source keys and their associated values.

    i18n_directory : Path
        The directory containing the i18n JSON files.

    locales_to_check : list
        List of locale files to check. If empty, all locale files are checked.

    Returns
    -------
    dict
        A dictionary where keys are locale filenames and values are tuples containing:
        - A list of missing keys (including keys with empty string values)
        - The percentage of missing keys (0-100)
    """
    all_src_keys = set(i18n_src_dict.keys())
    missing_keys_by_locale = {}

    for json_file in get_all_json_files(directory=i18n_directory):
        # Get just the filename without the extension.
        filename = json_file.split(PATH_SEPARATOR)[-1].split(".")[0]

        # Skip the source file itself.
        if filename == str(config_i18n_src_file).split(PATH_SEPARATOR)[-1]:
            continue

        # Skip if locales_to_check is specified and this file isn't in the list.
        if locales_to_check and filename not in locales_to_check:
            continue

        locale_dict = read_json_file(file_path=json_file)
        locale_keys = set(locale_dict.keys())

        # Find keys that are missing or have empty string values.
        missing_keys = [
            key
            for key in all_src_keys
            if key not in locale_keys or locale_dict.get(key) == ""
        ]

        # Calculate the percentage of missing keys.
        if all_src_keys:
            missing_percentage = (len(missing_keys) / len(all_src_keys)) * 100

        else:
            missing_percentage = 0.0

        if missing_keys:
            missing_keys_by_locale[filename] = (
                sorted(missing_keys),
                missing_percentage,
            )

    return missing_keys_by_locale


# MARK: Error Outputs


def report_missing_keys(
    missing_keys_by_locale: Dict[str, Tuple[List[str], float]],
    all_checks_enabled: bool = False,
) -> None:
    """
    Report missing keys found in locale files.

    Parameters
    ----------
    missing_keys_by_locale : dict
        A dictionary with locale filenames as keys and tuples of (missing keys, percentage) as values.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if any locale files have missing keys.
    """
    if missing_keys_by_locale:
        error_message = (
            "\n[red]❌ missing-keys error: There are locale files with missing keys. "
            "Keys are considered missing if they don't exist or have empty string values.\n\n"
        )

        # Report missing keys for each locale.
        for locale_file, (missing_keys, percentage) in missing_keys_by_locale.items():
            error_message += f"Missing keys in {locale_file} ({len(missing_keys)} keys, {percentage:.1f}% missing):\n"
            for key in missing_keys:
                error_message += f"  - {key}\n"

            error_message += "\n"

        error_message += "Summary of missing keys by locale:\n"
        for locale_file, (missing_keys, percentage) in missing_keys_by_locale.items():
            error_message += f"  {locale_file}: {percentage:.1f}% missing\n"

        error_message += "[/red]"
        rprint(error_message)

        if all_checks_enabled:
            raise ValueError("The missing keys i18n check has failed.")

        else:
            sys.exit(1)

    else:
        rprint(
            "[green]✅ missing-keys success: All checked locale files have all required keys with non-empty values.[/green]"
        )


# MARK: Interactive Fix


def add_missing_keys_interactively(
    locale: str,
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    i18n_directory: Path = config_i18n_directory,
) -> None:
    """
    Interactively add missing keys for a specific locale.

    Parameters
    ----------
    locale : str
        The locale to add missing keys for (e.g., 'de', 'fr', 'es').

    i18n_src_dict : dict
        The dictionary containing i18n source keys and their associated values.

    i18n_directory : Path
        The directory containing the i18n JSON files.

    Raises
    ------
    sys.exit(1)
        If the locale file doesn't exist or can't be processed.
    """
    locale_file_path = None
    for json_file in get_all_json_files(directory=i18n_directory):
        filename = json_file.split(PATH_SEPARATOR)[-1].split(".")[0]
        if filename == locale:
            locale_file_path = json_file
            break

    if not locale_file_path:
        rprint(
            f"[red]❌ Error: Locale file '{locale}.json' not found in {i18n_directory}[/red]"
        )
        sys.exit(1)

    # Get missing keys for this locale.
    missing_keys_by_locale = get_missing_keys_by_locale(
        i18n_src_dict=i18n_src_dict,
        i18n_directory=i18n_directory,
        locales_to_check=[locale],
    )

    if locale not in missing_keys_by_locale:
        rprint(f"[green]✅ All keys are present in {locale}.json[/green]")
        return

    missing_keys, percentage = missing_keys_by_locale[locale]

    rprint(f"\n[yellow]Interactive localization mode for locale: {locale}[/yellow]")
    rprint(
        f"[yellow]Missing keys: {len(missing_keys)} ({percentage:.1f}% missing)[/yellow]"
    )
    rprint("[yellow]Note: Press Ctrl+C at any time to cancel[/yellow]\n")

    locale_dict = read_json_file(locale_file_path)

    try:

        def get_source_value_length(key: str) -> int:
            """
            Get the length of missing key value so that they can be sorted by length (shortest first).

            Parameters
            ----------
            key : str
                The key in the i18n_src_dict to get the length of the value for.

            Returns
            -------
            int
                The length of the value of the given key.
            """
            return len(i18n_src_dict.get(key, ""))

        sorted_missing_keys = sorted(missing_keys, key=get_source_value_length)

        missing_keys_dict_for_mapping = {}
        for key in sorted_missing_keys:
            source_value = i18n_src_dict.get(key, "")
            # Skip if the result is a nested key.
            if not isinstance(source_value, dict):
                missing_keys_dict_for_mapping[key] = source_value

        missing_keys_to_files_dict = map_keys_to_files(
            i18n_src_dict=missing_keys_dict_for_mapping,
            src_directory=config_src_directory,
        )

        for key in sorted_missing_keys:
            source_value = i18n_src_dict.get(key, "")

            # Skip if the result is a nested key.
            if not isinstance(source_value, dict):
                missing_key_files = missing_keys_to_files_dict.get(key, [])

                # Skip if the key isn't used in any file.
                if missing_key_files:
                    rprint(f"[cyan]Key:[/cyan] {key}")
                    rprint(f"[cyan]Source value:[/cyan] '{source_value}'")

                    missing_key_file_names = [
                        f.split(PATH_SEPARATOR)[-1] for f in missing_key_files
                    ]
                    rprint(f"[cyan]Used in:[/cyan] {', '.join(missing_key_file_names)}")

                    # Get translation from user.
                    translation = Prompt.ask(
                        f"[green]Enter translation for '{key}'[/green]",
                        default="",
                        show_default=False,
                    )

                    if translation:
                        # Add the translation to the locale dictionary.
                        locale_dict[key] = translation

                        # Sort the file if the sorted-keys and repeat-keys checks are activated.
                        if config_sorted_keys_active:
                            if (
                                config_repeat_keys_active
                                and not check_file_keys_repeated(locale_file_path)[1]
                            ):
                                locale_dict = dict(sorted(locale_dict.items()))

                        else:
                            rprint(
                                "\n[yellow]⚠️  Note: JSON key sorting skipped as there are repeat keys (i18n-check -rk)[/yellow]"
                            )

                        with open(locale_file_path, "w", encoding="utf-8") as f:
                            json.dump(locale_dict, f, indent=2, ensure_ascii=False)
                            f.write("\n")

                        rprint(
                            f"[green]✅ Added translation for '{key}': '{translation}'[/green]\n"
                        )

                    else:
                        rprint(f"⏭️ Skipped '{key}' (empty translation)\n")

    except KeyboardInterrupt:
        rprint("\n[yellow]Cancelled by user[/yellow]")
        sys.exit(0)

    # Show final status.
    remaining_missing = get_missing_keys_by_locale(
        i18n_src_dict=i18n_src_dict,
        i18n_directory=i18n_directory,
        locales_to_check=[locale],
    )

    if locale not in remaining_missing:
        rprint(f"[green]✅ All keys have been added to {locale}.json![/green]")

    else:
        remaining_count = len(remaining_missing[locale][0])
        key_or_keys = "key" if remaining_count == 1 else "keys"
        rprint(
            f"[yellow]⚠️ {remaining_count} {key_or_keys} still missing in {locale}.json[/yellow]"
        )


# MARK: Check with Fix


def missing_keys_check_and_fix(
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    i18n_directory: Path = config_i18n_directory,
    locales_to_check: List[str] = config_missing_keys_locales_to_check,
    all_checks_enabled: bool = False,
    fix_locale: Optional[str] = None,
) -> bool:
    """
    Check missing keys and optionally enter interactive mode to fix them.

    Parameters
    ----------
    i18n_src_dict : dict
        The dictionary containing i18n source keys and their associated values.

    i18n_directory : Path
        The directory containing the i18n JSON files.

    locales_to_check : list
        List of locale files to check. If empty, all locale files are checked.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    fix_locale : str, optional
        If provided, enter interactive mode to add missing keys for this locale.

    Returns
    -------
    bool
        True if the check is successful.
    """
    if fix_locale:
        add_missing_keys_interactively(
            locale=fix_locale,
            i18n_src_dict=i18n_src_dict,
            i18n_directory=i18n_directory,
        )

    else:
        missing_keys_by_locale = get_missing_keys_by_locale(
            i18n_src_dict=i18n_src_dict,
            i18n_directory=i18n_directory,
            locales_to_check=locales_to_check,
        )
        report_missing_keys(
            missing_keys_by_locale=missing_keys_by_locale,
            all_checks_enabled=all_checks_enabled,
        )

    return True
