# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functions to update the i18n-check CLI based on install method.
"""

import subprocess
import sys

from packaging import version
from packaging.version import InvalidVersion

from i18n_check.cli.version import (
    UNKNOWN_VERSION_NOT_FETCHED,
    get_latest_version,
    get_local_version,
)


def upgrade_cli() -> None:
    """
    Upgrade the CLI tool to the latest available version on PyPI.

    Raises
    ------
    subprocess.CalledProcessError
        If the installation of the latest version fails.
    """
    local_version = get_local_version()
    latest_version_message = get_latest_version()

    if latest_version_message == UNKNOWN_VERSION_NOT_FETCHED:
        print(
            "Unable to fetch the latest version from GitHub. Please check the GitHub repository or your internet connection."
        )
        return

    latest_version = latest_version_message.split("v")[-1]
    local_version_clean = local_version.strip()
    latest_version_clean = latest_version.replace("i18n-check", "").strip()

    # Handle empty or invalid version strings.
    try:
        local_ver = (
            version.parse(local_version_clean)
            if local_version_clean
            else version.parse("0.0.0")
        )

    except InvalidVersion:
        # If local version is invalid, treat it as 0.0.0 to force upgrade.
        local_ver = version.parse("0.0.0")

    try:
        latest_ver = version.parse(latest_version_clean)

    except InvalidVersion:
        print("Unable to parse the latest version. Please check the GitHub repository.")
        return

    if local_ver == latest_ver:
        print("You already have the latest version of i18n-check.")

    elif local_ver > latest_ver:
        print(
            f"i18n-check v{local_version_clean} is higher than the currently released version i18n-check v{latest_version_clean}. Hopefully this is a development build, and if so, thanks for your work on i18n-check! If not, please report this to the team at https://github.com/activist-org/i18n-check/issues."
        )

    else:
        print(f"Current version: {local_version}")
        print(f"Latest version: {latest_version}")
        print("Updating i18n-check with pip...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "i18n-check"]
            )

        except subprocess.CalledProcessError as e:
            print(
                f"Failed to install the latest version of i18n-check with error {e}. Please check the error message and report any issues to the team at https://github.com/activist-org/i18n-check/issues."
            )


if __name__ == "__main__":
    upgrade_cli()
