# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the i18n-check command line interface.
"""

import argparse
import sys
from argparse import Namespace
from typing import Callable

from rich import print as rprint

from i18n_check.check.all_checks import run_all_checks
from i18n_check.check.alt_texts import alt_texts_check_and_fix
from i18n_check.check.aria_labels import aria_labels_check_and_fix
from i18n_check.check.key_formatting import (
    invalid_key_formats_check_and_fix,
    invalid_keys_by_format,
)
from i18n_check.check.key_naming import (
    invalid_key_names_check_and_fix,
    invalid_keys_by_name,
)
from i18n_check.check.missing_keys import missing_keys_check_and_fix
from i18n_check.check.nested_files import nested_files_check, nested_files_check_and_fix
from i18n_check.check.non_source_keys import non_source_keys_check, non_source_keys_dict
from i18n_check.check.nonexistent_keys import (
    all_used_i18n_keys,
    nonexistent_keys_check_and_fix,
)
from i18n_check.check.repeat_keys import repeat_keys_check
from i18n_check.check.repeat_values import (
    json_repeat_value_counts,
    repeat_value_error_report,
    repeat_values_check,
)
from i18n_check.check.sorted_keys import sorted_keys_check_and_fix
from i18n_check.check.unused_keys import unused_keys, unused_keys_check
from i18n_check.cli.generate_config_file import (
    config_file_is_valid,
    generate_config_file,
)
from i18n_check.cli.generate_test_frontends import generate_test_frontends
from i18n_check.cli.upgrade import upgrade_cli
from i18n_check.cli.version import get_version_message


def run_all_checks_command(args: Namespace) -> None:
    """
    Helper method to run all i18n-checks.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Runs all the checks in the project.
    """
    run_all_checks(args=args)


def run_key_formatting_command(args: Namespace) -> None:
    """
    Helper method to check proper key formatting of i18n-keys.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks the key formatting and prints the result via terminal.
    """
    invalid_key_formats_check_and_fix(
        invalid_keys_by_format=invalid_keys_by_format,
        all_checks_enabled=False,
        fix=args.fix,
    )


def run_key_naming_command(args: Namespace) -> None:
    """
    Helper method to check proper key naming of i18n-keys.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks the naming of keys and prints the result via terminal.
    """
    invalid_key_names_check_and_fix(
        invalid_keys_by_name=invalid_keys_by_name,
        all_checks_enabled=False,
        fix=args.fix,
    )


def run_nonexistent_keys_command(args: Namespace) -> None:
    """
    Helper method to check non existent keys.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks if there's non existent keys and prints the result via terminal.
    """
    nonexistent_keys_check_and_fix(all_used_i18n_keys=all_used_i18n_keys, fix=args.fix)


def run_unused_keys_command(args: Namespace) -> None:
    """
    Helper method to check for unused i18n keys in the codebase.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks the codebase for unused keys and prints the result via terminal.
    """
    if args.delete:
        from i18n_check.check.unused_keys import (
            unused_keys_check_and_delete,  # needed for tests
        )

        unused_keys_check_and_delete(unused_keys=unused_keys)

    else:
        unused_keys_check(unused_keys=unused_keys)


def run_non_source_keys_command(args: Namespace) -> None:
    """
    Helper method to check if i18n translation JSON files that are not present in the source files.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks the codebase for any non source keys in the JSON files and prints the result via terminal.
    """

    if args.delete:
        from i18n_check.check.non_source_keys import non_source_keys_check_and_delete

        non_source_keys_check_and_delete(non_source_keys_dict=non_source_keys_dict)
    else:
        non_source_keys_check(non_source_keys_dict=non_source_keys_dict)


def run_repeat_keys_command(args: Namespace) -> None:
    """
    Check for duplicate keys in i18n JSON files.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks for duplicate keys and prints the result via terminal.
    """
    repeat_keys_check()


def run_repeat_values_command(args: Namespace) -> None:
    """
    Check if values in the i18n-src file have repeat strings.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks for repeated strings and prints the result via terminal.
    """
    repeat_values_check(
        json_repeat_value_counts=json_repeat_value_counts,
        repeat_value_error_report=repeat_value_error_report,
    )


def run_sorted_keys_command(args: Namespace) -> None:
    """
    Check if all the i8n-check's JSON files are sorted alphabetically.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks if the keys are sorted alphabetically and prints the result via terminal.
    """
    sorted_keys_check_and_fix(fix=args.fix)


def run_nested_files_command(args: Namespace) -> None:
    """
    Check for nested i18n source and translation keys.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks if the files are nested, then fixes it and prints the result via terminal.
    """
    if args.fix:
        nested_files_check_and_fix()
    else:
        nested_files_check()


def _missing_keys_locale_error() -> None:
    """
    Helper function to check for missing keys.

    Returns
    -------
    None
        Prints if there's no required flag and terminates the process.
    """
    rprint(
        "[red]❌ Error: --locale (-l) is required when using --fix (-f) with --missing-keys (-mk)[/red]"
    )
    rprint("[yellow]💡 Example: i18n-check -mk -f -l ENTER_ISO_2_CODE[/yellow]")
    sys.exit(1)


def run_missing_keys_command(args: Namespace) -> None:
    """
    Check for missing keys in locale files compared to the source file.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks for the missing keys, then fixes it and prints the result via terminal.
    """
    if args.fix and args.locale:
        missing_keys_check_and_fix(fix_locale=args.locale)
    elif args.fix:
        _missing_keys_locale_error()
    else:
        missing_keys_check_and_fix()


def run_aria_labels_command(args: Namespace) -> None:
    """
    Check for the appropriate punctuation in the keys end with '_aria_label'.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks for the appropriate punctuations, then fixes it and prints the result via terminal.
    """
    aria_labels_check_and_fix(fix=args.fix)


def run_alt_texts_command(args: Namespace) -> None:
    """
    Check for the appropriate punctuation in the keys end with '_alt_text'.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    None
        Checks for the appropriate punctuations, then fixes it and prints the result via terminal.
    """
    alt_texts_check_and_fix(fix=args.fix)


CHECK_COMMANDS: dict[str, Callable[[Namespace], None]] = {
    "all_checks": run_all_checks_command,
    "key_formatting": run_key_formatting_command,
    "key_naming": run_key_naming_command,
    "nonexistent_keys": run_nonexistent_keys_command,
    "unused_keys": run_unused_keys_command,
    "non_source_keys": run_non_source_keys_command,
    "repeat_keys": run_repeat_keys_command,
    "repeat_values": run_repeat_values_command,
    "sorted_keys": run_sorted_keys_command,
    "nested_files": run_nested_files_command,
    "missing_keys": run_missing_keys_command,
    "aria_labels": run_aria_labels_command,
    "alt_texts": run_alt_texts_command,
}


def dispatch_check_command(args: Namespace) -> bool:
    """
    Check for the arguments and dispatches the right command to execute.

    Parameters
    ----------
    args : Namespace
        Receives CLI args for the specific function.

    Returns
    -------
    bool
        Returns the boolean value of execution status of the commands given.
    """
    for flag_name, handler in CHECK_COMMANDS.items():
        if getattr(args, flag_name):
            handler(args)
            return True
    return False


def main() -> None:
    """
    Execute the i18n-check CLI based on provided arguments.

    This function serves as the entry point for the i18n-check command line interface.
    It parses command line arguments and executes the appropriate checks or actions.

    Returns
    -------
    None
        This function returns nothing; it executes checks and outputs results directly.

    Notes
    -----
    The available command line arguments are:
    - --help (-h): Show this help message and exit.
    - --version (-v): Show the version of the i18n-check CLI.
    - --upgrade (-u): Upgrade the i18n-check CLI to the latest version.
    - --generate-config-file (-gcf): Generate a configuration file for i18n-check.
    - --generate-test-frontends (-gtf): Generate frontends to test i18n-check functionalities.
    - --all-checks (-a): Run all available checks.
    - --key-formatting (-kf): Check for proper formatting of i18n keys in the i18n-src file.
    - --key-naming (-kn): Check for consistent file based naming of i18n keys in the codebase.
    - --nonexistent-keys (-nk): Check if the codebase includes i18n keys that are not within the source file.
    - --unused-keys (-uk): Check for unused i18n keys in the codebase.
    - --non-source-keys (-nsk): Check if i18n translation JSON files have keys that are not in the source file.
    - --repeat-keys (-rk): Check for duplicate keys in i18n JSON files.
    - --repeat-values (-rv): Check if values in the i18n-src file have repeat strings.
    - --sorted-keys (-sk): Check if all i18n JSON files have keys sorted alphabetically.
    - --nested-files (-nf): Check for nested i18n source and translation keys.
    - --missing-keys (-mk): Check for missing keys in locale files.
    - --aria-labels (-al): Check for appropriate punctuation in aria label keys.
    - --alt-texts (-at): Check for appropriate punctuation in alt text keys.
    - --fix (-f): Automatically fix key issues. Can be used with -kf, -kn, -nk, -sk, -mk, -al, -at or -nf.
    - --locale (-l): Specify locale for interactive key addition.
    - --delete (-d): Delete unused keys or non-source keys from JSON files. Can be used with -uk or -nsk.

    Examples
    --------
    >>> i18n-check --generate-config-file  # -gcf
    >>> i18n-check --key-formatting  # -kf
    >>> i18n-check --key-formatting --fix  # -kf -f
    >>> i18n-check --key-naming --fix  # -kn -f
    >>> i18n-check --all-checks  # -a
    >>> i18n-check --missing-keys --fix --locale ENTER_ISO_2_CODE  # interactive mode to add missing keys
    """
    # MARK: CLI Base

    parser = argparse.ArgumentParser(
        prog="i18n-check",
        description="i18n-check is a CLI tool for checking i18n/L10n keys and values.",
        epilog="Visit the codebase at https://github.com/activist-org/i18n-check to learn more!",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=60),
    )

    parser._actions[0].help = "Show this help message and exit."

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{get_version_message()}",
        help="Show the version of the i18n-check CLI.",
    )

    parser.add_argument(
        "-u",
        "--upgrade",
        action="store_true",
        help="Upgrade the i18n-check CLI to the latest version.",
    )

    parser.add_argument(
        "-gcf",
        "--generate-config-file",
        action="store_true",
        help="Generate a configuration file for i18n-check.",
    )

    parser.add_argument(
        "-gtf",
        "--generate-test-frontends",
        action="store_true",
        help="Generate frontends to test i18n-check functionalities.",
    )

    parser.add_argument(
        "-a",
        "--all-checks",
        action="store_true",
        help="Run all i18n checks on the project.",
    )

    parser.add_argument(
        "-kf",
        "--key-formatting",
        action="store_true",
        help="Check for proper formatting of i18n keys in the i18n-src file.",
    )

    parser.add_argument(
        "-kn",
        "--key-naming",
        action="store_true",
        help="Check for consistent file based naming of i18n keys in the codebase.",
    )

    parser.add_argument(
        "-nk",
        "--nonexistent-keys",
        action="store_true",
        help="Check if the codebase includes i18n keys that are not within the source file.",
    )

    parser.add_argument(
        "-uk",
        "--unused-keys",
        action="store_true",
        help="Check for unused i18n keys in the codebase.",
    )

    parser.add_argument(
        "-nsk",
        "--non-source-keys",
        action="store_true",
        help="Check if i18n translation JSON files have keys that are not in the source file.",
    )

    parser.add_argument(
        "-rk",
        "--repeat-keys",
        action="store_true",
        help="Check for duplicate keys in i18n JSON files.",
    )

    parser.add_argument(
        "-rv",
        "--repeat-values",
        action="store_true",
        help="Check if values in the i18n-src file have repeat strings.",
    )

    parser.add_argument(
        "-sk",
        "--sorted-keys",
        action="store_true",
        help="Check if all i18n JSON files have keys sorted alphabetically.",
    )

    parser.add_argument(
        "-nf",
        "--nested-files",
        action="store_true",
        help="Check for nested i18n source and translation keys.",
    )

    parser.add_argument(
        "-mk",
        "--missing-keys",
        action="store_true",
        help="Check for missing keys in locale files compared to the source file.",
    )

    parser.add_argument(
        "-al",
        "--aria-labels",
        action="store_true",
        help="Check for appropriate punctuation in keys that end with '_aria_label'.",
    )

    parser.add_argument(
        "-at",
        "--alt-texts",
        action="store_true",
        help="Check for appropriate punctuation in keys that end with '_alt_text'.",
    )

    parser.add_argument(
        "-f",
        "--fix",
        action="store_true",
        help="Automatically fix key issues. Can be used with -kf, -kn, -nk, -sk, -mk, -al, -at or -nf.",
    )

    parser.add_argument(
        "-l",
        "--locale",
        type=str,
        help="When using -mk -f, specify the locale to interactively add missing keys to.",
    )

    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="Delete unused keys or non-source keys from JSON files. Can be used with -uk or -nsk.",
    )

    # MARK: Setup CLI

    args = parser.parse_args()

    if args.generate_test_frontends:
        generate_test_frontends()
        return

    if args.upgrade:
        upgrade_cli()
        return

    if args.generate_config_file:
        generate_config_file()
        return

    if not config_file_is_valid():
        sys.exit(1)
    if not dispatch_check_command(args):
        parser.print_help()
