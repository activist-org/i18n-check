# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the i18n-check command line interface.
"""

import argparse

from i18n_check.cli.upgrade import upgrade_cli
from i18n_check.cli.version import get_version_message
from i18n_check.utils import run_check

CLI_EPILOG = (
    "Visit the codebase at https://github.com/activist-org/i18n-check to learn more!"
)


def main() -> None:
    # MARK: CLI Base

    parser = argparse.ArgumentParser(
        description="i18n-check is a CLI tool for checking i18n/L10n keys and values.",
        epilog=CLI_EPILOG,
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=60),
    )
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
        "-uk",
        "--unused-keys",
        action="store_true",
        help="Check for unused i18n keys in the codebase.",
    )

    parser.add_argument(
        "-rv",
        "--repeat-values",
        action="store_true",
        help="Check for values in the i18n-src file have repeat string.",
    )

    parser.add_argument(
        "-nsk",
        "--non-source-keys",
        action="store_true",
        help="Check if i18n translation JSON files have keys that are not in es-US.json.",
    )

    parser.add_argument(
        "-nf",
        "--nested-i18n-src",
        action="store_true",
        help="Check for nested i18n source keys in the i18n-src file.",
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
        help="Check for keys used in the project appear in the i18n-src file.",
    )

    parser.add_argument(
        "-ach",
        "--all-checks",
        action="store_true",
        help="Run all i18n checks for the project.",
    )
    # MARK: Setup CLI

    args = parser.parse_args()

    if args.upgrade:
        upgrade_cli()
        return

    if args.unused_keys:
        run_check("unused_keys.py")
        return

    if args.repeat_values:
        run_check("repeat_values.py")
        return

    if args.non_source_keys:
        run_check("non_source_keys.py")
        return

    if args.nested_i18n_src:
        run_check("nested_i18n_src.py")
        return

    if args.key_identifiers:
        run_check("key_identifiers.py")
        return

    if args.invalid_keys:
        run_check("invalid_keys.py")
        return

    if args.all_checks:
        run_check("all_checks.py")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
