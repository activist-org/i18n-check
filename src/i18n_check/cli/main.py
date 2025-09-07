# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the i18n-check command line interface.
"""

import argparse
import sys

from rich import print as rprint

from i18n_check.check.alt_texts import check_alt_texts
from i18n_check.check.aria_labels import check_aria_labels
from i18n_check.check.invalid_keys import (
    invalid_keys_by_format,
    invalid_keys_by_name,
    report_and_correct_keys,
)
from i18n_check.check.missing_keys import check_missing_keys_with_fix
from i18n_check.check.sorted_keys import check_all_files_sorted
from i18n_check.cli.generate_config_file import generate_config_file
from i18n_check.cli.generate_test_frontends import generate_test_frontends
from i18n_check.cli.upgrade import upgrade_cli
from i18n_check.cli.version import get_version_message
from i18n_check.utils import run_check


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
    - --non-existent-keys (-nek): Check i18n key usage and formatting
    - --unused-keys (-uk): Check for unused i18n keys
    - --non-source-keys (-nsk): Check for keys in translations not in source
    - --repeat-keys (-rk): Check for duplicate keys in JSON files
    - --repeat-values (-rv): Check for repeated values in source file
    - --sorted-keys (-sk): Check if all i18n JSON files have keys sorted alphabetically
    - --nested-keys (-nk): Check for nested i18n keys
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
        "-nek",
        "--non-existent-keys",
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
        "-nk",
        "--nested-keys",
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
        run_check("all_checks")
        return

    if args.invalid_keys:
        if args.fix:
            report_and_correct_keys(
                invalid_keys_by_format=invalid_keys_by_format,
                invalid_keys_by_name=invalid_keys_by_name,
                fix=True,
            )

        else:
            run_check("invalid_keys")

        return

    if args.non_existent_keys:
        run_check("non_existent_keys")
        return

    if args.unused_keys:
        run_check("unused_keys")
        return

    if args.non_source_keys:
        run_check("non_source_keys")
        return

    if args.repeat_keys:
        run_check("repeat_keys")
        return

    if args.repeat_values:
        run_check("repeat_values")
        return

    if args.sorted_keys:
        if args.fix:
            check_all_files_sorted(fix=True)

        else:
            run_check("sorted_keys")

        return

    if args.nested_keys:
        run_check("nested_keys")
        return

    if args.missing_keys:
        if args.fix and args.locale:
            check_missing_keys_with_fix(fix_locale=args.locale)

        elif args.fix and not args.locale:
            rprint(
                "[red]❌ Error: --locale (-l) is required when using --fix (-f) with --missing-keys (-mk)[/red]"
            )
            rprint("[yellow]💡 Example: i18n-check -mk -f -l de[/yellow]")
            sys.exit(1)

        else:
            run_check("missing_keys")

        return

    if args.aria_labels:
        if args.fix:
            check_aria_labels(fix=True)

        else:
            run_check("aria_labels")

        return

    if args.alt_texts:
        if args.fix:
            check_alt_texts(fix=True)

        else:
            run_check("alt_texts")

        return

    parser.print_help()


if __name__ == "__main__":
    main()
