# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functions for checking current version of the i18n-check CLI.
"""

import importlib.metadata
from typing import Any, Dict

import requests

UNKNOWN_VERSION = "Unknown i18n-check version"
UNKNOWN_VERSION_NOT_PIP = f"{UNKNOWN_VERSION} (Not installed via pip)"
UNKNOWN_VERSION_NOT_FETCHED = f"{UNKNOWN_VERSION} (Unable to fetch version)"


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
        return UNKNOWN_VERSION_NOT_PIP


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
        return UNKNOWN_VERSION_NOT_FETCHED


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

    if local_version == UNKNOWN_VERSION_NOT_PIP:
        return UNKNOWN_VERSION_NOT_PIP

    elif latest_version == UNKNOWN_VERSION_NOT_FETCHED:
        return UNKNOWN_VERSION_NOT_FETCHED

    local_version_clean = local_version.strip()
    latest_version_clean = latest_version.replace("i18n-check", "").strip()

    if local_version_clean == latest_version_clean:
        return f"i18n-check v{local_version_clean}"

    elif local_version_clean > latest_version_clean:
        return f"i18n-check v{local_version_clean} is higher than the currently released version i18n-check v{latest_version_clean}. Hopefully this is a development build, and if so, thanks for your work on i18n-check! If not, please report this to the team at https://github.com/activist-org/i18n-check/issues."

    else:
        return f"i18n-check v{local_version_clean} (Upgrade available: i18n-check v{latest_version_clean}). To upgrade: i18n-check -u"
