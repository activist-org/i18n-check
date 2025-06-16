# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functions to update the i18n-check CLI based on install method.
"""

import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import requests

from i18n_check.cli.version import get_latest_version, get_local_version


def upgrade_cli() -> None:
    """
    Upgrade the CLI tool to the latest version available on GitHub.

    This function checks the current version of the i18n-check CLI tool
    and compares it with the latest version available on GitHub. If a
    newer version is available, it downloads the latest version, extracts
    the files, updates the local files, and installs the updated version
    locally.

    Raises
    ------
    subprocess.CalledProcessError
        If the installation of the updated version fails.
    """
    local_version = get_local_version()
    latest_version_message = get_latest_version()
    latest_version = latest_version_message.split("v")[-1]

    if latest_version_message == "Unknown (Unable to fetch version)":
        print(
            "Unable to fetch the latest version from GitHub. Please check the GitHub repository or your internet connection."
        )
        return

    if local_version == latest_version:
        print("You already have the latest version of i18n-check.")

    if local_version < latest_version:
        print(f"Current version: {local_version}")
        print(f"Latest version: {latest_version}")

    print("Updating i18n-check...")

    url = f"https://github.com/activist-org/i18n-check/archive/refs/tags/{latest_version}.tar.gz"
    print(f"Downloading i18n-check v{latest_version}...")
    response = requests.get(url)

    if response.status_code == 200:
        with open(f"i18n-check-{latest_version}.tar.gz", "wb") as f:
            f.write(response.content)
        print(f"Download complete: i18n-check-{latest_version}.tar.gz")

        print("Extracting files...")
        temp_dir = Path(f"temp_i18n-check-{latest_version}")
        with tarfile.open(f"i18n-check-{latest_version}.tar.gz", "r:gz") as tar:
            tar.extractall(path=temp_dir)

        print("Extraction complete.")

        print("Updating local files...")
        extracted_dir = temp_dir / f"i18n-check-{latest_version}"
        for item in extracted_dir.iterdir():
            if item.is_dir():
                if (Path.cwd() / item.name).exists():
                    shutil.rmtree(Path.cwd() / item.name)

                shutil.copytree(item, Path.cwd() / item.name)

            else:
                shutil.copy2(item, Path.cwd())

        print("Local files updated successfully.")

        print("Cleaning up temporary files...")
        shutil.rmtree(temp_dir)
        os.remove(f"i18n-check-{latest_version}.tar.gz")
        print("Cleanup complete.")

        print("Installing the updated version of i18n-check locally...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])

        except subprocess.CalledProcessError as e:
            print(
                f"Failed to install the local version of i18n-check with error {e}. Please try manually running 'pip install -e .'"
            )

    else:
        print(f"Failed to download the update. Status code: {response.status_code}")


if __name__ == "__main__":
    upgrade_cli()
