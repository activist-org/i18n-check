# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to copy the test frontend files from the package to the present working directory.
"""

import os
import shutil
from pathlib import Path

# Note: Repeat from utils to avoid circular import.
PATH_SEPARATOR = "\\" if os.name == "nt" else "/"
INTERNAL_TEST_FRONTENDS_DIR_PATH = Path(__file__).parent.parent / "test_frontends"


def get_test_frontend_config_file_text() -> str:
    """
    Return the text for the configuration file for the i18n-check test frontends.

    Returns
    -------
    str
        The text for the configuration file for the i18n-check test frontends.
    """
    return r"""# Configuration file for i18n-check validation.
# See https://github.com/activist-org/i18n-check for details.

src-dir: i18n_check_test_frontends/test_frontends/all_checks_fail
i18n-dir: i18n_check_test_frontends/test_frontends/all_checks_fail/test_i18n
i18n-src: i18n_check_test_frontends/test_frontends/all_checks_fail/test_i18n/test_i18n_src.json

# Note: Comment out the above lines and uncomment these to check functionality with a passing frontend.
# Note: You also need to remove the 'search-dirs' argument for 'nonexistent-keys' for all checks to pass.
# src-dir: i18n_check_test_frontends/test_frontends/all_checks_pass
# i18n-dir: i18n_check_test_frontends/test_frontends/all_checks_pass/test_i18n
# i18n-src: i18n_check_test_frontends/test_frontends/all_checks_pass/test_i18n/test_i18n_src.json

file-types-to-check: [.ts]

checks:
  # Global configurations are applied to all checks.
  global:
    active: true
    directories-to-skip: [i18n_check_test_frontends/test_frontends/all_checks_fail/skip_dir]
    files-to-skip: []
  nonexistent-keys:
    search-dirs: [i18n_check_test_frontends/test_frontends/search_dir]
  unused-keys:
    keys-to-ignore: [i18n\.unused_keys\.ignore.*]
"""


def write_test_frontends_config_file(config_file_name: str) -> None:
    """
    Write a YAML configuration file for the i18n-check test frontends.

    Parameters
    ----------
    config_file_name : str
        The name for the i18n-check configuration file.

    Returns
    -------
    None
        The contents of a configuration file are written to match the test frontends.
    """
    test_project_config_text = get_test_frontend_config_file_text()
    with open(config_file_name, "w") as file:
        file.write(test_project_config_text)


def generate_test_frontends() -> None:
    """
    Copy the i18n_check/test_frontends directory to the present working directory.
    """
    if not Path("./i18n_check_test_frontends/").is_dir():
        print(
            f"Generating testing frontends for i18n-check in .{PATH_SEPARATOR}i18n_check_test_frontends{PATH_SEPARATOR} ..."
        )

        shutil.copytree(
            INTERNAL_TEST_FRONTENDS_DIR_PATH,
            Path("./i18n_check_test_frontends/"),
            dirs_exist_ok=True,
        )

        print("The frontends have been successfully generated.")
        print("One passes all checks and one fails all checks.")
        if (
            not Path(".i18n-check.yaml").is_file()
            and not Path(".i18n-check.yml").is_file()
        ):
            print("No .i18n-check.yaml configuration file found.")

            generate_test_project_config_answer = None
            while generate_test_project_config_answer not in ["y", "n", ""]:
                generate_test_project_config_answer = (
                    input(
                        "Would you like to generate a configuration file for the test frontends? ([y]/n): "
                    )
                    .strip()
                    .lower()
                )

            if generate_test_project_config_answer in ["y", ""]:
                write_test_frontends_config_file(config_file_name=".i18n-check.yaml")
                print(
                    "A .i18n-check.yaml configuration file has been written to match the test frontends."
                )

        else:
            config_file_name = (
                ".i18n-check.yaml"
                if Path(".i18n-check.yaml").is_file()
                else ".i18n-check.yml"
            )
            generate_test_project_config_answer = None
            while generate_test_project_config_answer not in ["y", "n", ""]:
                generate_test_project_config_answer = (
                    input(
                        f"Would you like to overwrite the {config_file_name} configuration file for the test frontends? ([y]/n): "
                    )
                    .strip()
                    .lower()
                )

            if generate_test_project_config_answer in ["y", ""]:
                write_test_frontends_config_file(config_file_name=config_file_name)
                print(
                    f"The {config_file_name} configuration file has been overwritten to match the test frontends."
                )

            else:
                print(f"You can set which one to test in the {config_file_name} file.")

    else:
        print(
            f"Test frontends for i18n-check already exist in .{PATH_SEPARATOR}i18n_check_test_frontends{PATH_SEPARATOR} and will not be regenerated."
        )
