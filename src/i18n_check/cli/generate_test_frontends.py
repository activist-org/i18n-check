# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to copy the test frontend files from the package to the present working directory.
"""

import shutil
from pathlib import Path

TEST_FRONTENDS_DIRECTORY = Path(__file__).parent.parent / "test_frontends"


def generate_test_frontends() -> None:
    """
    Copy the i18n_check/test_frontends directory to the present working directory.
    """
    if not Path("./i18n_check_test_frontends/").is_dir():
        print(
            "Generating testing frontends for i18n-check in ./i18n_check_test_frontends/ ..."
        )

        shutil.copytree(
            TEST_FRONTENDS_DIRECTORY,
            "./i18n_check_test_frontends/",
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
            "Test frontends for i18n-check already exist in ./i18n_check_test_frontends/ and will not be regenerated."
        )


if __name__ == "__main__":
    generate_test_frontends()
