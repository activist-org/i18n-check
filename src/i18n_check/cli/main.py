# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the i18n-check command line interface.
"""

import argparse

from i18n_check.cli.generate_config_file import generate_config_file
from i18n_check.cli.generate_test_frontends import generate_test_frontends
from i18n_check.cli.upgrade import upgrade_cli
from i18n_check.cli.version import get_version_message
from i18n_check.utils import run_check

CLI_EPILOG = (
    "Visit the codebase at https://github.com/activist-org/i18n-check to learn more!"
)


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
    - --key-identifiers (-ki): Check i18n key usage and formatting
    - --invalid-keys (-ik): Check for invalid i18n keys in codebase
    - --unused-keys (-uk): Check for unused i18n keys
    - --non-source-keys (-nsk): Check for keys in translations not in source
    - --repeat-keys (-rk): Check for duplicate keys in JSON files
    - --repeat-values (-rv): Check for repeated values in source file
    - --nested-keys (-nk): Check for nested i18n keys

    Examples
    --------
    >>> i18n-check --generate-config-file  # -gcf
    >>> i18n-check --key-identifiers  # -ki
    >>> i18n-check --all-checks  # -a
    """
    # MARK: CLI Base

    parser = argparse.ArgumentParser(
        description="i18n-check is a CLI tool for checking i18n/L10n keys and values.",
        epilog=CLI_EPILOG,
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
        "-ki",
        "--key-identifiers",
        action="store_true",
        help="Check for usage and formatting of i18n keys in the i18n-src file.",
    )

    parser.add_argument(
        "-ik",
        "--invalid-keys",
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

    if args.key_identifiers:
        run_check("key_identifiers")
        return

    if args.invalid_keys:
        run_check("invalid_keys")
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

    parser.print_help()


if __name__ == "__main__":
    main()
