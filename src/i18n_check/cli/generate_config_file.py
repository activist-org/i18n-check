# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to generate a configuration file for i18n-check.
"""

from pathlib import Path

import yaml
from generate_test_frontends import generate_test_frontends

YAML_FILE_PATH = Path(__file__).parent.parent.parent.parent / ".i18n-check.yaml"
TEST_FRONTENDS_PATH = Path(__file__).parent.parent.parent / "i18n_check_test_frontends/"


checks = [
    {"all": False},
    {"invalid_keys": False},
    {"key_identifiers": False},
    {"nested_keys": False},
    {"non_source_keys": False},
    {"repeat_keys": False},
    {"repeat_values": False},
    {"unused_keys": False},
]


def write_to_file(
    src_dir, i18n_dir, i18n_dir_src, check_file_types, dirs_to_skip, files_to_skip
):
    """
    Writing to file .i18n-check.yaml file.
    """
    with open(YAML_FILE_PATH, "w") as file:
        data = {
            "src-dir": src_dir,
            "i18n-dir": i18n_dir,
            "i18n-src": i18n_dir_src,
            "checks": checks,
            "file-types-to-check": check_file_types,
            "directories-to-skip": dirs_to_skip,
            "files-to-skip": files_to_skip,
        }
        yaml.dump(data=data, stream=file)


def receive_data():
    """
    Interacting with user to configure .yml file.
    """
    src_dir = input("Enter src dir: ").strip() or "src/i18n_check/test_frontends"
    i18n_dir = (
        input("Enter i18n-dir: ").strip()
        or "src/i18n_check/test_frontends/all_checks_fail/test_i18n"
    )
    i18n_src_dir = (
        input("Enter i18n-src dir: ").strip()
        or "src/i18n_check/test_frontends/all_checks_fail/test_i18n"
    )
    check_file_types = input("Enter the file extension type to check: ").split() or [
        ".ts",
        ".js",
        ".vue",
    ]
    dirs_to_skip = input("Enter directories to skip: ").split() or [
        "frontend/node_modules"
    ]
    files_to_skip = input("Enter files to skip: ").split() or [
        "app.py"
    ]  # using app.py as an example. Default value needs to be changed.

    print("Answer using y or n to select your required checks.")
    all_check_choice = input("All checks: ").lower()
    if all_check_choice == "y":
        checks[0]["all"] = True
    else:
        invalid_key = input("Invalid key check: ")
        checks[1]["invalid_keys"] = True if invalid_key.lower() == "y" else False
        key_identifiers = input("Key Identifiers check: ")
        checks[2]["key_identifiers"] = True if key_identifiers.lower() == "y" else False
        nested_key = input("Nested keys: ")
        checks[3]["nested_keys"] = True if nested_key.lower() == "y" else False
        non_source_keys = input("Non source keys: ")
        checks[4]["non_source_keys"] = True if non_source_keys.lower() == "y" else False
        repeat_keys = input("Repeat keys: ")
        checks[5]["repeat_keys"] = True if repeat_keys.lower() == "y" else False
        repeat_values = input("Repeat values: ")
        checks[6]["repeat_values"] = True if repeat_values.lower() == "y" else False
        unused_keys = input("Unused keys: ")
        checks[7]["unused_keys"] = True if unused_keys.lower() == "y" else False

    write_to_file(
        src_dir=src_dir,
        i18n_dir=i18n_dir,
        i18n_dir_src=i18n_src_dir,
        check_file_types=check_file_types,
        dirs_to_skip=dirs_to_skip,
        files_to_skip=files_to_skip,
    )


def generate_config_file() -> None:
    """
    Interactively generate a configuration file for i18n-check based on user inputs.
    """
    if Path(YAML_FILE_PATH).is_file():
        print(
            "Config file exists. Would you like to re-configure your .i18n-check.yaml file?"
        )
        choice = input("Press Y or N to continue: ").lower()
        if choice == "y":
            print("Configuring....")
            receive_data()
            print("Your .i18n-check.yaml file has been generated.")
            if Path(TEST_FRONTENDS_PATH).is_dir():
                choice2 = input(
                    "checks for test_frontends exist. Would you like to reconfigure these tests?: "
                ).lower()
                if choice2 == "y":
                    generate_test_frontends()
                else:
                    print("Exiting.")
            else:
                print("frontend_checks directory does not exist. Generating tests.....")
                generate_test_frontends()
        else:
            print("Exiting.")
    else:
        print("File does not exist. Configure your .i18n-check.yaml file.....")
        receive_data()
        print("Your .i18n-check.yaml file has been generated.")


if __name__ == "__main__":
    generate_config_file()
