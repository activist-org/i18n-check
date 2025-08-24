# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the i18n-check command line interface.
"""

import argparse

from i18n_check.check.invalid_keys import (
    invalid_keys_by_format,
    invalid_keys_by_name,
    report_and_correct_keys,
)
from i18n_check.check.ordered_keys import check_ordered_keys
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
    """

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
        help="(with --invalid-keys or --ordered-keys) Automatically fix key naming or ordering issues.",
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
        "-nk",
        "--nested-keys",
        action="store_true",
        help="Check for nested i18n source and translation keys.",
    )

    parser.add_argument(
        "-ok",
        "--ordered-keys",
        action="store_true",
        help="Check that JSON keys are ordered alphabetically.",
    )

    args = parser.parse_args()

    # Process flags with early returns to avoid running multiple commands in one call
    if args.upgrade:
        upgrade_cli()
        return

    if args.generate_config_file:
        generate_config_file()
        return

    if args.generate_test_frontends:
        generate_test_frontends()
        return

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

    if args.nested_keys:
        run_check("nested_keys")
        return

    if args.ordered_keys:
        check_ordered_keys(fix=args.fix)
        return

    # If no recognized flags, print help
    parser.print_help()


if __name__ == "__main__":
    main()
