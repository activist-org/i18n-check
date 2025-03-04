# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the i18n-check command line interface.
"""

import argparse

from i18n_check.cli.upgrade import upgrade_cli
from i18n_check.cli.version import get_version_message

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
    subparsers = parser.add_subparsers(dest="command")  # noqa: F841
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

    # MARK: Setup CLI

    args = parser.parse_args()

    if args.upgrade:
        upgrade_cli()
        return

    if not args.command:
        parser.print_help()
        return


if __name__ == "__main__":
    main()
