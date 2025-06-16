# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functions for checking current version of the i18n-check CLI.
"""

import importlib.metadata
from typing import Any, Dict

import requests


def get_local_version() -> str:
    """
    Get the local version of the i18n-check package.

    Returns
    -------
    str
        The version of the installed i18n-check package, or a message indicating
        that the package is not installed via pip.
    """
    try:
        return importlib.metadata.version("i18n-check")

    except importlib.metadata.PackageNotFoundError:
        return "Unknown (Not installed via pip)"


def get_latest_version() -> Any:
    """
    Get the latest version of the i18n-check package from GitHub.

    Returns
    -------
    Any
        The latest version of the i18n-check package, or a message indicating
        that the version could not be fetched.
    """
    try:
        response = requests.get(
            "https://api.github.com/repos/activist-org/i18n-check/releases/latest"
        )
        response_data: Dict[str, Any] = response.json()
        return response_data["name"]

    except Exception:
        return "Unknown (Unable to fetch version)"


def get_version_message() -> str:
    """
    Get a message indicating the local and latest versions of the i18n-check package.

    Returns
    -------
    str
        A message indicating the local version, the latest version, and whether
        an upgrade is available.
    """
    local_version = get_local_version()
    latest_version = get_latest_version()

    if local_version == "Unknown (Not installed via pip)":
        return f"i18n-check {local_version}"
    elif latest_version == "Unknown (Unable to fetch version)":
        return f"i18n-check {latest_version}"

    local_version_clean = local_version.strip()
    latest_version_clean = latest_version.replace("i18n-check", "").strip()

    if local_version_clean == latest_version_clean:
        return f"i18n-check v{local_version_clean}"

    return f"i18n-check v{local_version_clean} (Upgrade available: i18n-check v{latest_version_clean})\nTo update: pip install --upgrade i18n-check"


if __name__ == "__main__":
    print(get_version_message())
