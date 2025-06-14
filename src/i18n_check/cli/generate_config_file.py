# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to generate a configuration file for i18n-check.
"""

from pathlib import Path

from i18n_check.cli.generate_test_frontends import generate_test_frontends

YAML_FILE_PATH = Path(__file__).parent.parent.parent.parent / ".i18n-check.yaml"
TEST_FRONTENDS_PATH = Path(__file__).parent.parent.parent / "i18n_check_test_frontends/"


checks = {
    "global": False,
    "invalid_keys": False,
    "key_identifiers": False,
    "nested_keys": False,
    "non_source_keys": False,
    "repeat_keys": False,
    "repeat_values": False,
    "unused_keys": False,
}


def write_to_file(
    src_dir: str,
    i18n_dir: str,
    i18n_src_file: str,
    checks: dict,
    file_types_to_check: list[str],
    dirs_to_skip: list[str],
    files_to_skip: list[str],
) -> None:
    """
    Writing to file .i18n-check.yaml file.

    Parameters
    ----------
    src_dir : str
        Input src dir directory.

    i18n_dir : str
        Input i18n-dir directory.

    i18n_src_file : str
        Input i18n-dir-src directory.

    checks : dict
        The boolean values for checks being enabled or not.

    file_types_to_check : list[str]
        Input file extensions for checks.

    dirs_to_skip : list[src]
        Input directory to skip. Default: frontend/node_modules.

    files_to_skip : list[src]
        Input files to skip checking.
    """
    with open(YAML_FILE_PATH, "w") as file:
        checks_str = "".join(f"  {k}:\n    active: {v}\n" for k, v in checks.items())
        file_types_to_check_str = ", ".join(file_types_to_check)
        dirs_to_skip_str = ", ".join(dirs_to_skip)
        files_to_skip_str = files_to_skip or ""

        config_string = f"""# Configuration file for i18n-check validation.
# See https://github.com/activist-org/i18n-check for details.

src-dir: {src_dir}
i18n-dir: {i18n_dir}
i18n-src: {i18n_src_file}

checks:
{checks_str}
file-types-to-check: [{file_types_to_check_str}]
directories-to-skip: [{dirs_to_skip_str}]
files-to-skip: [{files_to_skip_str}]
"""

        file.write(config_string)


def receive_data() -> None:
    """
    Interact with user to configure a .yml file.
    """
    src_dir = input("Enter src dir [frontend]: ").strip() or "frontend"
    i18n_dir = input("Enter i18n-dir [frontend/i18n]: ").strip() or "frontend/i18n"
    i18n_src_file = (
        input("Enter i18n-src file [frontend/i18n/en.json]: ").strip()
        or "frontend/i18n/en.json"
    )
    file_types_to_check = input(
        "Enter the file extension type to check [.ts, .js]: "
    ).split() or [".ts", ".js"]
    dirs_to_skip = input(
        "Enter directories to skip [frontend/node_modules]: "
    ).split() or ["frontend/node_modules"]
    files_to_skip = input("Enter files to skip [None]: ").split() or None

    print("Answer using y or n to select your required checks.")
    all_check_choice = input("All checks [y]: ").lower()
    if all_check_choice in ["y", ""]:
        checks = {"global": True}

    else:
        invalid_key = input("Invalid key check: ")
        checks["invalid_keys"] = invalid_key.lower() == "y"

        key_identifiers = input("Key Identifiers check: ")
        checks["key_identifiers"] = key_identifiers.lower() == "y"

        nested_key = input("Nested keys: ")
        checks["nested_keys"] = nested_key.lower() == "y"

        non_source_keys = input("Non source keys: ")
        checks["non_source_keys"] = bool(non_source_keys.lower() == "y")

        repeat_keys = input("Repeat keys: ")
        checks["repeat_keys"] = bool(repeat_keys.lower() == "y")

        repeat_values = input("Repeat values: ")
        checks["repeat_values"] = bool(repeat_values.lower() == "y")

        unused_keys = input("Unused keys: ")
        checks["unused_keys"] = bool(unused_keys.lower() == "y")

    write_to_file(
        src_dir=src_dir,
        i18n_dir=i18n_dir,
        i18n_src_file=i18n_src_file,
        checks=checks,
        file_types_to_check=file_types_to_check,
        dirs_to_skip=dirs_to_skip,
        files_to_skip=files_to_skip,
    )


def generate_config_file() -> None:
    """
    Generate a configuration file for i18n-check based on user inputs.
    """
    if Path(YAML_FILE_PATH).is_file():
        print(
            "An i18n-check configuration file already exists. Would you like to re-configure your .i18n-check.yaml file?"
        )
        reconfigure_choice = input("Press y or n to continue [y]: ").lower()
        if reconfigure_choice in ["y", ""]:
            print("Configuring...")
            receive_data()
            print("Your .i18n-check.yaml file has been generated successfully.")
            if not Path(TEST_FRONTENDS_PATH).is_dir():
                test_frontend_choice = input(
                    "\nWould you like to generate test pseudocode frontends to experiment with i18n-check?"
                    "\nPress y to generate an i18n_check_test_frontends directory [y]: "
                ).lower()
                if test_frontend_choice in ["y", ""]:
                    generate_test_frontends()

                else:
                    print("Exiting.")

        else:
            print("Exiting.")

    else:
        print(
            "You do not have an i18n-check configuration file. Follow the commands below to generate .i18n-check.yaml..."
        )
        receive_data()
        print("Your .i18n-check.yaml file has been generated successfully.")


if __name__ == "__main__":
    generate_config_file()
