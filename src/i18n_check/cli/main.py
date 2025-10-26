# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the i18n-check command line interface.
"""

import argparse
import sys

from rich import print as rprint

from i18n_check.check.all_checks import run_all_checks
from i18n_check.check.alt_texts import alt_texts_check_and_fix
from i18n_check.check.aria_labels import aria_labels_check_and_fix
from i18n_check.check.invalid_keys import (
    invalid_keys_by_format,
    invalid_keys_by_name,
    invalid_keys_check_and_fix,
)
from i18n_check.check.missing_keys import missing_keys_check_and_fix
from i18n_check.check.nested_files import nested_files_check
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
from i18n_check.cli.generate_config_file import generate_config_file
from i18n_check.cli.generate_test_frontends import generate_test_frontends
from i18n_check.cli.upgrade import upgrade_cli
from i18n_check.cli.version import get_version_message


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
    - --version (-v): Show the version of the i18n-check CLI
    - --upgrade (-u): Upgrade the i18n-check CLI to the latest version
    - --generate-config-file (-gcf): Generate a configuration file for i18n-check
    - --generate-test-frontends (-gtf): Generate frontends to test i18n-check functionalities
    - --all-checks (-a): Run all available checks
    - --invalid-keys (-ik): Check for invalid i18n keys in codebase
    - --nonexistent-keys (-nk): Check i18n key usage and formatting
    - --unused-keys (-uk): Check for unused i18n keys
    - --non-source-keys (-nsk): Check for keys in translations not in source
    - --repeat-keys (-rk): Check for duplicate keys in JSON files
    - --repeat-values (-rv): Check for repeated values in source file
    - --sorted-keys (-sk): Check if all i18n JSON files have keys sorted alphabetically
    - --nested-files (-nf): Check for nested i18n keys
    - --missing-keys (-mk): Check for missing keys in locale files
    - --locale (-l): Specify locale for interactive key addition
    - --aria-labels (-al): Check for appropriate punctuation in aria label keys
    - --alt-texts (-at): Check for appropriate punctuation in alt text keys

    Examples
    --------
    >>> i18n-check --generate-config-file  # -gcf
    >>> i18n-check --invalid-keys  # -ik
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
        "-ik",
        "--invalid-keys",
        action="store_true",
        help="Check for usage and formatting of i18n keys in the i18n-src file.",
    )

    parser.add_argument(
        "-f",
        "--fix",
        action="store_true",
        help="(with --invalid-keys) Automatically fix key naming issues.",
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
        "-l",
        "--locale",
        type=str,
        help="(with --missing-keys --fix) Specify the locale to interactively add missing keys to.",
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

    # MARK: Setup CLI

    args = parser.parse_args()

    if args.upgrade:
        upgrade_cli()
        return

    if args.generate_config_file:
        generate_config_file()
        return

    if args.generate_test_frontends:
        generate_test_frontends()
        return

    # MARK: Run Checks

    if args.all_checks:
        run_all_checks(args=args)
        return

    if args.invalid_keys:
        invalid_keys_check_and_fix(
            invalid_keys_by_format=invalid_keys_by_format,
            invalid_keys_by_name=invalid_keys_by_name,
            fix=args.fix,
        )

        return

    if args.nonexistent_keys:
        nonexistent_keys_check_and_fix(
            all_used_i18n_keys=all_used_i18n_keys,
            fix=args.fix,
        )
        return

    if args.unused_keys:
        unused_keys_check(unused_keys=unused_keys)
        return

    if args.non_source_keys:
        non_source_keys_check(non_source_keys_dict=non_source_keys_dict)
        return

    if args.repeat_keys:
        repeat_keys_check()
        return

    if args.repeat_values:
        repeat_values_check(
            json_repeat_value_counts=json_repeat_value_counts,
            repeat_value_error_report=repeat_value_error_report,
        )
        return

    if args.sorted_keys:
        sorted_keys_check_and_fix(fix=args.fix)

        return

    if args.nested_files:
        nested_files_check()
        return

    if args.missing_keys:
        if args.fix and args.locale:
            missing_keys_check_and_fix(fix_locale=args.locale)

        elif args.fix:
            rprint(
                "[red]❌ Error: --locale (-l) is required when using --fix (-f) with --missing-keys (-mk)[/red]"
            )
            rprint("[yellow]💡 Example: i18n-check -mk -f -l ENTER_ISO_2_CODE[/yellow]")
            sys.exit(1)

        else:
            missing_keys_check_and_fix()

        return

    if args.aria_labels:
        aria_labels_check_and_fix(fix=args.fix)

        return

    if args.alt_texts:
        alt_texts_check_and_fix(fix=args.fix)

        return

    parser.print_help()
