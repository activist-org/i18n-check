# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to generate a configuration file for i18n-check.
"""

import os
from pathlib import Path
from typing import Dict

from rich import print as rprint
from yaml import safe_load

from i18n_check.cli.generate_test_frontends import generate_test_frontends

EXTERNAL_TEST_FRONTENDS_DIR_PATH = Path.cwd() / "i18n_check_test_frontends"

# Note: Repeat from utils to avoid circular import.
PATH_SEPARATOR = "\\" if os.name == "nt" else "/"


def config_file_is_valid() -> bool:
    """
    Check that the configuration file for i18n-check is not empty and has the necessary keys.

    Returns
    -------
    bool
        True if the i18n-check configuration file is valid. False otherwise.
    """
    from i18n_check.utils import YAML_CONFIG_FILE_PATH

    with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        config = safe_load(file)

        if config is not None:
            config_keys = config.keys()
            if "src-dir" not in config_keys or not isinstance(config["src-dir"], str):
                rprint(
                    "[red]The i18n-check 'src-dir' argument has not been defined properly. Please check the configuration file and try again.[/red]"
                )
                return False

            if "i18n-dir" not in config_keys or not isinstance(config["i18n-dir"], str):
                rprint(
                    "[red]The i18n-check 'i18n-dir' argument has not been defined properly. Please check the configuration file and try again.[/red]"
                )
                return False

            if "i18n-src" not in config_keys or not isinstance(config["i18n-src"], str):
                rprint(
                    "[red]The i18n-check 'i18n-src' argument has not been defined properly. Please check the configuration file and try again.[/red]"
                )
                return False

            if "file-types-to-check" not in config_keys or not isinstance(
                config["file-types-to-check"], list
            ):
                rprint(
                    "[red]The i18n-check 'file-types-to-check' argument has not been defined properly. Please check the configuration file and try again.[/red]"
                )
                return False

            if (
                "checks" not in config_keys
                or not isinstance(config["checks"], dict)
                # No checks including global have been found in the config file.
                or len(
                    set(config["checks"].keys())
                    & set(
                        [
                            "global",
                            "key-formatting",
                            "key-naming",
                            "nonexistent-keys",
                            "unused-keys",
                            "non-source-keys",
                            "repeat-keys",
                            "repeat-values",
                            "sorted-keys",
                            "nested-files",
                            "missing-keys",
                            "aria-labels",
                            "alt-texts",
                        ]
                    )
                )
                == 0
            ):
                rprint(
                    "[red]The i18n-check 'checks' argument has not been defined properly. Please check the configuration file and try again.[/red]"
                )
                return False

            return True

        else:
            rprint(
                "[red]The i18n-check configuration file is empty. Please regenerate your config file with i18n-check -gcf.[/red]"
            )
            return False


def write_to_file(
    src_dir: str,
    i18n_dir: str,
    i18n_src_file: str,
    file_types_to_check: list[str] | None,
    checks: Dict[str, dict],  # type: ignore [type-arg]
) -> None:
    """
    Writing to the i18n source JSON file.

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
    # Import here to avoid circular import.
    from i18n_check.utils import get_config_file_path

    config_file_path = get_config_file_path()
    with open(config_file_path, "w", encoding="utf-8") as file:
        checks_str = ""
        for c in checks:
            checks_str += f"  {c}:\n    active: {checks[c]['active']}\n"

            if "directories-to-skip" in checks[c]:
                checks_str += f"    directories-to-skip: [{', '.join(checks[c]['directories-to-skip'])}]\n"

            if "files-to-skip" in checks[c]:
                checks_str += (
                    f"    files-to-skip: [{', '.join(checks[c]['files-to-skip'])}]\n"
                )

            if "keys-to-ignore" in checks[c]:
                if isinstance(checks[c]["keys-to-ignore"], list):
                    keys_list = ", ".join(
                        f'"{key}"' for key in checks[c]["keys-to-ignore"]
                    )
                    checks_str += f"    keys-to-ignore: [{keys_list}]\n"

                else:
                    checks_str += (
                        f'    keys-to-ignore: "{checks[c]["keys-to-ignore"]}"\n'
                    )

            if "locales-to-check" in checks[c]:
                checks_str += f"    locales-to-check: [{', '.join(checks[c]['locales-to-check'])}]\n"

            if "search-dirs" in checks[c]:
                checks_str += (
                    f"    search-dirs: [{', '.join(checks[c]['search-dirs'])}]\n"
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
    i18n_dir = (
        input(f"Enter i18n-dir [frontend{PATH_SEPARATOR}i18n]: ").strip()
        or f"frontend{PATH_SEPARATOR}i18n"
    )
    i18n_src_file = (
        input(
            f"Enter i18n-src file [frontend{PATH_SEPARATOR}i18n{PATH_SEPARATOR}en.json]: "
        ).strip()
        or f"frontend{PATH_SEPARATOR}i18n{PATH_SEPARATOR}en.json"
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
            "keys-to-ignore": [],
        },
        "nonexistent_keys": {
            "title": "non existent keys",
            "active": False,
            "directories-to-skip": [],
            "files-to-skip": [],
            "search-dirs": [],
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
        "sorted_keys": {"title": "sorted keys", "active": False},
        "nested_files": {"title": "nested keys", "active": False},
        "missing_keys": {
            "title": "missing keys",
            "active": False,
            "locales-to-check": [],
        },
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
                    f"Directories to skip for {checks[c]['title']} [frontend{PATH_SEPARATOR}node_modules]: "
                ).lower()
                checks[c]["directories-to-skip"] = (
                    directories_to_skip
                    if directories_to_skip != ""
                    else [f"frontend{PATH_SEPARATOR}node_modules"]
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

        if "keys-to-ignore" in checks[c]:
            keys_to_ignore_input = input(
                f"Keys to ignore for {checks[c]['title']} (comma-separated regex patterns) [None]: "
            )
            if keys_to_ignore_input.strip():
                patterns = [
                    pattern.strip() for pattern in keys_to_ignore_input.split(",")
                ]
                # Filter out empty patterns.
                checks[c]["keys-to-ignore"] = [p for p in patterns if p]

            else:
                checks[c]["keys-to-ignore"] = []

        if "locales-to-check" in checks[c]:
            locales_to_check = input(
                f"Locales to check for {checks[c]['title']} (comma-separated, e.g., fr, de) [All]: "
            )
            if locales_to_check.strip():
                checks[c]["locales-to-check"] = [
                    locale.strip() for locale in locales_to_check.split(",")
                ]

            else:
                checks[c]["locales-to-check"] = []

        if "search-dirs" in checks[c]:
            search_dirs = input(
                f"Additional search directories for {checks[c]['title']} (comma-separated, e.g., frontend/test, frontend/test-e2e) [None]: "
            )
            if search_dirs.strip():
                checks[c]["search-dirs"] = [
                    dir.strip() for dir in search_dirs.split(",")
                ]

            else:
                checks[c]["search-dirs"] = []

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
    # Import here to avoid circular import.
    from i18n_check.utils import get_config_file_path

    config_path = get_config_file_path()
    if config_path.is_file():
        config_file_name = config_path.name
        print(
            f"An i18n-check configuration file already exists. Would you like to re-configure your {config_file_name} file?"
        )
        reconfigure_choice = input("Press y or n to continue [y]: ").lower()
        if reconfigure_choice in ["y", ""]:
            print("Configuring...")
            receive_data()
            print(f"Your {config_file_name} file has been generated successfully.")
            if not Path(EXTERNAL_TEST_FRONTENDS_DIR_PATH).is_dir():
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
            "You do not have an i18n-check configuration file. Follow the commands below to generate a .i18n-check.yaml configuration file..."
        )
        receive_data()
        config_path = get_config_file_path()
        print(f"Your {config_path.name} file has been generated successfully.")
