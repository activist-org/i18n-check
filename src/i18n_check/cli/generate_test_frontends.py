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
            print("You can set which one to test in an i18n-check configuration file.")
            print(
                "Please generate one with the 'i18n-check --generate-config-file' command."
            )

        elif Path(".i18n-check.yaml").is_file():
            print("You can set which one to test in the .i18n-check.yaml file.")

        elif Path(".i18n-check.yml").is_file():
            print("You can set which one to test in the .i18n-check.yml file.")

    else:
        print(
            f"Test frontends for i18n-check already exist in .{PATH_SEPARATOR}i18n_check_test_frontends{PATH_SEPARATOR} and will not be regenerated."
        )
