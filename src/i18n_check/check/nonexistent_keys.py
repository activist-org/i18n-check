# SPDX-License-Identifier: GPL-3.0-or-later
"""
Checks the i18n keys used in the project and makes sure that each of them appears in the i18n-src file.

If there are nonexistent keys, alert the user to their presence.

Examples
--------
Run the following script in terminal:

>>> i18n-check -nk
>>> i18n-check -nk -f  # interactive mode to add nonexistent keys
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from rich import print as rprint
from rich.prompt import Prompt

from i18n_check.check.key_naming import map_keys_to_files
from i18n_check.check.repeat_keys import check_file_keys_repeated
from i18n_check.utils import (
    PATH_SEPARATOR,
    collect_files_to_check,
    config_file_types_to_check,
    config_i18n_src_file,
    config_nonexistent_keys_directories_to_skip,
    config_nonexistent_keys_files_to_skip,
    config_repeat_keys_active,
    config_sorted_keys_active,
    config_src_directory,
    read_json_file,
)

# MARK: Paths / Files

i18n_src_dict = read_json_file(file_path=config_i18n_src_file)


# MARK: Key Comparisons


def get_used_i18n_keys(
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    src_directory: Path = config_src_directory,
) -> Set[str]:
    """
    Get all i18n keys that are used in the project.

    Parameters
    ----------
    i18n_src_dict : Dict[str, str]
        The dictionary containing i18n source keys and their associated values.

    src_directory : Path
        The source directory where the files are located.

    Returns
    -------
    Set[str]
        A set of all i18n keys that are used in the project.
    """

    i18n_key_pattern_quote = r"\'i18n\.[_\S\.]+?\'"
    i18n_key_pattern_double_quote = r"\"i18n\.[_\S\.]+?\""
    i18n_key_pattern_back_tick = r"\`i18n\.[_\S\.]+?\`"
    all_i18n_key_patterns = [
        i18n_key_pattern_quote,
        i18n_key_pattern_double_quote,
        i18n_key_pattern_back_tick,
    ]

    files_to_check = collect_files_to_check(
        directory=src_directory,
        file_types_to_check=config_file_types_to_check,
        directories_to_skip=config_nonexistent_keys_directories_to_skip,
        files_to_skip=config_nonexistent_keys_files_to_skip,
    )
    files_to_check_contents = {}
    for frontend_file in files_to_check:
        with open(frontend_file, "r", encoding="utf-8") as f:
            files_to_check_contents[frontend_file] = f.read()

    all_used_i18n_keys: Set[Any] = set()
    for v in files_to_check_contents.values():
        all_file_i18n_keys: List[Any] = []
        all_file_i18n_keys.extend(
            re.findall(i18n_kp, v) for i18n_kp in all_i18n_key_patterns
        )
        # Remove the first and last characters that are the quotes or back ticks.
        all_file_i18n_keys = [k[1:-1] for ks in all_file_i18n_keys for k in ks]

        all_used_i18n_keys.update(all_file_i18n_keys)

    return set(all_used_i18n_keys)


# MARK: Error Outputs


def nonexistent_keys_check(
    all_used_i18n_keys: Set[str],
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    all_checks_enabled: bool = False,
) -> bool:
    """
    Validate that all used i18n keys are present in the i18n source file.

    Parameters
    ----------
    all_used_i18n_keys : Set[str]
        A set of all i18n keys that are used in the project.

    i18n_src_dict : Dict[str, str], default=i18n_src_dict
        The dictionary containing i18n source keys and their associated values.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    Returns
    -------
    bool
        True if the check is successful.

    Raises
    ------
    ValueError, sys.exit(1)
        An error is raised and the system prints error details if there are any i18n keys that are used in the project but not defined in the source file.
    """
    all_keys = i18n_src_dict.keys()
    if nonexistent_keys := list(all_used_i18n_keys - all_keys):
        to_be = "are" if len(nonexistent_keys) > 1 else "is"
        key_to_be = "keys that are" if len(nonexistent_keys) > 1 else "key that is"
        key_or_keys = "keys" if len(nonexistent_keys) > 1 else "key"

        error_message = f"[red]❌ nonexistent-keys error: There {to_be} {len(nonexistent_keys)} i18n {key_to_be} not in the i18n source file. Please check the validity of the following {key_or_keys}:"
        error_message += "\n\n"
        error_message += "\n".join(sorted(nonexistent_keys))
        error_message += "[/red]"

        rprint(error_message)

        rprint(
            "\n[yellow]💡 Tip: You can interactively add nonexistent keys by running the --nonexistent-keys (-nk) check with the --fix (-f) flag.[/yellow]\n"
        )

        if all_checks_enabled:
            raise ValueError("The nonexistent keys i18n check has failed.")

        else:
            sys.exit(1)

    else:
        rprint(
            "[green]✅ nonexistent-keys success: All i18n keys that are used in the project are in the i18n source file.[/green]"
        )

    return True


# MARK: Interactive Fix


def add_nonexistent_keys_interactively(
    all_used_i18n_keys: Set[str],
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    i18n_src_file: Path = config_i18n_src_file,
    src_directory: Path = config_src_directory,
) -> None:
    """
    Interactively add nonexistent keys to the i18n source file.

    Parameters
    ----------
    all_used_i18n_keys : Set[str]
        A set of all i18n keys that are used in the project.

    i18n_src_dict : Dict[str, str], default=i18n_src_dict
        The dictionary containing i18n source keys and their associated values.

    i18n_src_file : Path, default=config_i18n_src_file
        Path to the i18n source file.

    src_directory : Path, default=config_src_directory
        The source directory where the files are located.

    Raises
    ------
    sys.exit(0)
        If the user cancels the operation with Ctrl+C.
    """
    nonexistent_keys = list(all_used_i18n_keys - i18n_src_dict.keys())

    if not nonexistent_keys:
        rprint(
            "[green]✅ nonexistent-keys success: All i18n keys that are used in the project are in the i18n source file.[/green]"
        )
        return

    rprint(
        "\n[yellow]Interactive mode to add values for nonexistent keys to the i18n source file[/yellow]"
    )
    rprint(f"[yellow]Nonexistent keys: {len(nonexistent_keys)}[/yellow]")
    rprint(
        "[yellow]Note: Press Enter to skip any key if you don't know what its value should be[/yellow]"
    )
    rprint("[yellow]Note: Press Ctrl+C at any time to cancel[/yellow]\n")

    try:
        i18n_src_dict_updated = i18n_src_dict.copy()

        # Sort nonexistent keys alphabetically for consistent presentation.
        sorted_nonexistent_keys = sorted(nonexistent_keys)

        nonexistent_keys_dict_for_mapping = {key: "" for key in sorted_nonexistent_keys}
        nonexistent_keys_to_files_dict = map_keys_to_files(
            i18n_src_dict=nonexistent_keys_dict_for_mapping,
            src_directory=src_directory,
        )

        for key in sorted_nonexistent_keys:
            nonexistent_key_files = nonexistent_keys_to_files_dict.get(key, [])

            rprint(f"[cyan]Key:[/cyan] {key}")

            # Show file names where the key is used.
            nonexistent_key_file_names = [
                f.split(PATH_SEPARATOR)[-1] for f in nonexistent_key_files
            ]
            rprint(f"[cyan]Used in:[/cyan] {', '.join(nonexistent_key_file_names)}")

            if value := Prompt.ask(
                f"[green]Enter value for '{key}'[/green]",
                default="",
                show_default=False,
            ):
                # Add the key-value pair to the dictionary.
                i18n_src_dict_updated[key] = value

                # Sort the file if the sorted-keys and repeat-keys checks are activated.
                if config_sorted_keys_active:
                    if (
                        config_repeat_keys_active
                        and not check_file_keys_repeated(str(i18n_src_file))[1]
                    ):
                        i18n_src_dict_updated = dict(
                            sorted(i18n_src_dict_updated.items())
                        )

                    else:
                        rprint(
                            "\n[yellow]⚠️  Note: JSON key sorting skipped as there are repeat keys (i18n-check -rk)[/yellow]"
                        )

                # Write to file.
                with open(i18n_src_file, "w", encoding="utf-8") as f:
                    json.dump(i18n_src_dict_updated, f, indent=2, ensure_ascii=False)
                    f.write("\n")

                rprint(f"[green]✅ Added '{key}': '{value}'[/green]\n")

            else:
                rprint(f"⏭️ Skipped '{key}' (empty value)\n")

    except KeyboardInterrupt:
        rprint("\n[yellow]Cancelled by user[/yellow]")
        sys.exit(0)

    # Show final status.
    if remaining_nonexistent := all_used_i18n_keys - set(
        read_json_file(file_path=i18n_src_file).keys()
    ):
        remaining_count = len(remaining_nonexistent)
        key_or_keys = "key" if remaining_count == 1 else "keys"
        rprint(
            f"[yellow]⚠️ {remaining_count} {key_or_keys} still missing in the i18n source file[/yellow]"
        )

    else:
        rprint("[green]✅ All keys have been added to the i18n source file![/green]")


# MARK: Check with Fix


def nonexistent_keys_check_and_fix(
    all_used_i18n_keys: Set[str],
    i18n_src_dict: Dict[str, str] = i18n_src_dict,
    i18n_src_file: Path = config_i18n_src_file,
    src_directory: Path = config_src_directory,
    all_checks_enabled: bool = False,
    fix: bool = False,
) -> bool:
    """
    Validate that all used i18n keys are present in the i18n source file and optionally enter interactive mode to add nonexistent keys.

    Parameters
    ----------
    all_used_i18n_keys : Set[str]
        A set of all i18n keys that are used in the project.

    i18n_src_dict : Dict[str, str], default=i18n_src_dict
        The dictionary containing i18n source keys and their associated values.

    i18n_src_file : Path, default=config_i18n_src_file
        Path to the i18n source file.

    src_directory : Path, default=config_src_directory
        The source directory where the files are located.

    all_checks_enabled : bool, optional, default=False
        Whether all checks are being ran by the CLI.

    fix : bool, optional, default=False
        If True, enter interactive mode to add nonexistent keys to the i18n source file.

    Returns
    -------
    bool
        True if the check is successful.
    """
    if not fix:
        return nonexistent_keys_check(
            all_used_i18n_keys=all_used_i18n_keys,
            i18n_src_dict=i18n_src_dict,
            all_checks_enabled=all_checks_enabled,
        )

    add_nonexistent_keys_interactively(
        all_used_i18n_keys=all_used_i18n_keys,
        i18n_src_dict=i18n_src_dict,
        i18n_src_file=i18n_src_file,
        src_directory=src_directory,
    )
    return True


# MARK: Variables

all_used_i18n_keys = get_used_i18n_keys(
    i18n_src_dict=i18n_src_dict, src_directory=config_src_directory
)
