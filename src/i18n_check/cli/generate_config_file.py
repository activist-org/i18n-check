# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to generate a configuration file for i18n-check.
"""

from pathlib import Path
from typing import Dict

from i18n_check.cli.generate_test_frontends import generate_test_frontends

YAML_CONFIG_FILE_PATH = Path.cwd() / ".i18n-check.yaml"
TEST_FRONTENDS_PATH = Path(__file__).parent.parent.parent / "i18n_check_test_frontends/"


def write_to_file(
    src_dir: str,
    i18n_dir: str,
    i18n_src_file: str,
    file_types_to_check: list[str] | None,
    checks: Dict[str, dict],  # type: ignore [type-arg]
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

    file_types_to_check : list[str]
        Input file extensions for checks.

    checks : dict
        The boolean values for checks being enabled or not.
    """
    with open(YAML_CONFIG_FILE_PATH, "w") as file:
        checks_str = ""
        for c in checks:
            checks_str += f"  {c}:\n    active: {checks[c]['active']}\n"

            if "directories-to-skip" in checks[c]:
                checks_str += f"    directories-to-skip: [{', '.join(checks[c]['directories-to-skip'])}]\n"

            if "files-to-skip" in checks[c]:
                checks_str += (
                    f"    files-to-skip: [{', '.join(checks[c]['files-to-skip'])}]\n"
                )

        file_types_to_check_str = (
            ", ".join(file_types_to_check) if file_types_to_check else ""
        )

        config_string = f"""# Configuration file for i18n-check validation.
# See https://github.com/activist-org/i18n-check for details.

src-dir: {src_dir}
i18n-dir: {i18n_dir}
i18n-src: {i18n_src_file}

file-types-to-check: [{file_types_to_check_str}]

checks:
  # Global configurations are applied to all checks.
{checks_str}
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
        "Enter the file extension types to check [.ts, .js]: "
    ).split() or [".ts", ".js"]

    print("Answer using y or n to select your required checks.")

    checks = {
        "global": {
            "title": "all checks",
            "active": False,
            "directories-to-skip": [],
            "files-to-skip": [],
        },
        "invalid_keys": {
            "title": "invalid keys",
            "active": False,
            "directories-to-skip": [],
            "files-to-skip": [],
        },
        "key_identifiers": {
            "title": "key Identifiers",
            "active": False,
            "directories-to-skip": [],
            "files-to-skip": [],
        },
        "unused_keys": {
            "title": "unused keys",
            "active": False,
            "directories-to-skip": [],
            "files-to-skip": [],
        },
        "non_source_keys": {"title": "non source keys", "active": False},
        "repeat_keys": {"title": "repeat keys", "active": False},
        "repeat_values": {"title": "repeat values", "active": False},
        "nested_keys": {"title": "nested keys", "active": False},
    }

    for c, v in checks.items():
        if not checks["global"]["active"]:
            check_prompt = input(
                f"{checks[c]['title'].capitalize()} check [y]: "  # type: ignore [attr-defined]
            ).lower()

        if checks["global"]["active"] or check_prompt in ["y", ""]:
            checks[c]["active"] = True

        if "directories-to-skip" in v:
            if c == "global":
                directories_to_skip = input(
                    f"Directories to skip for {checks[c]['title']} [frontend/node_modules]: "
                ).lower()
                checks[c]["directories-to-skip"] = (
                    directories_to_skip
                    if directories_to_skip != ""
                    else ["frontend/node_modules"]
                )

            else:
                directories_to_skip = input(
                    f"Directories to skip for {checks[c]['title']} [None]: "
                ).lower()
                checks[c]["directories-to-skip"] = (
                    directories_to_skip if directories_to_skip != "" else []
                )

        if "files-to-skip" in checks[c]:
            files_to_skip = input(
                f"Files to skip for {checks[c]['title']} [None]: "
            ).lower()
            checks[c]["files-to-skip"] = files_to_skip if files_to_skip != "" else []

    write_to_file(
        src_dir=src_dir,
        i18n_dir=i18n_dir,
        i18n_src_file=i18n_src_file,
        file_types_to_check=file_types_to_check,
        checks=checks,
    )


def generate_config_file() -> None:
    """
    Generate a configuration file for i18n-check based on user inputs.
    """
    if Path(YAML_CONFIG_FILE_PATH).is_file():
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
