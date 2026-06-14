# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to generate a configuration file for i18n-check.
"""

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from rich import print as rprint
from yaml import safe_load

from i18n_check.cli.generate_test_frontends import generate_test_frontends

EXTERNAL_TEST_FRONTENDS_DIR_PATH = Path.cwd() / "i18n_check_test_frontends"

# Note: Repeat from utils to avoid circular import.
PATH_SEPARATOR = "\\" if os.name == "nt" else "/"


def check_config_and_validate(
    config: dict[str, Any],
    validators: dict[str, Callable[[Any], bool]],
    VALID_CHECK_KEYS: set[str],
) -> bool:
    """
    Check configuration files and validate.

    Parameters
    ----------
    config : dict[str,Any]
        A dictionary representing the configuration file.
    validators : dict[str,Callable[[Any],bool]]
        A dictionary containing necessary paths and it's instance types as Callable functions.
    VALID_CHECK_KEYS : set[str]
        A set of necessary keys to be checked.

    Returns
    -------
    bool
        Returns True if all the check has been passed otherwise False.
    """
    if config is None:
        rprint(
            "[red]The i18n-check configuration file is empty. Please regenerate your config file with i18n-check -gcf.[/red]"
        )
        return False

    for key, validator in validators.items():
        if key == "checks":
            if (
                key not in config
                or not validator(config[key])
                or len(set(config["checks"].keys()) & VALID_CHECK_KEYS) == 0
            ):
                rprint(
                    f"[red]The i18n-check '{key}' argument has not been defined properly. Please check the configuration file and try again.[/red]"
                )
                return False
            continue
        if key not in config or not validator(config[key]):
            rprint(
                f"[red]The i18n-check '{key}' argument has not been defined properly. Please check the configuration file and try again.[/red]"
            )
            return False
    return True


def config_file_is_valid() -> bool:
    """
    Check that the configuration file for i18n-check is not empty and has the necessary keys.

    Returns
    -------
    bool
        True if the i18n-check configuration file is valid. False otherwise.
    """
    from i18n_check.utils import YAML_CONFIG_FILE_PATH

    VALID_CHECK_KEYS = {
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
    }

    VALIDATORS: dict[str, Callable[[Any], bool]] = {
        "src-dir": lambda v: isinstance(v, str),
        "i18n-dir": lambda v: isinstance(v, str),
        "i18n-src": lambda v: isinstance(v, str),
        "file-types-to-check": lambda v: isinstance(v, list),
        "checks": lambda v: isinstance(v, dict),
    }

    with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        config = safe_load(file)
        return check_config_and_validate(config, VALIDATORS, VALID_CHECK_KEYS)


def check_to_str(check_name: str, check_cfg: dict) -> str:
    """
    To check and serialize a single check config to it's YAML string block.

    Parameters
    ----------
    check_name : str
        Names to be checked and passed as a str.
    check_cfg : dict
        Configs for the checks to be skipped.

    Returns
    -------
    str
        A Result of the check returned as a string.
    """
    lines = [f"  {check_name}:\n    active: {check_cfg['active']}"]

    optional_list_fields = [
        "directories-to-skip",
        "files-to-skip",
        "locales-to-check",
        "search-dirs",
    ]
    for field in optional_list_fields:
        if field in check_cfg:
            lines.append(f"    {field}: [{', '.join(check_cfg[field])}]")

    if "keys-to-ignore" in check_cfg:
        val = check_cfg["keys-to-ignore"]
        if isinstance(val, list):
            formatted = ", ".join(f'"{k}"' for k in val)
            lines.append(f"    keys-to-ignore: [{formatted}]")
        else:
            lines.append(f'    keys-to-ignore: "{val}"')

    return "\n".join(lines) + "\n"


def write_to_file(
    src_dir: str,
    i18n_dir: str,
    i18n_src_file: str,
    file_types_to_check: list[str] | None,
    checks: dict[str, dict],
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

    checks_str = "".join(check_to_str(name, cfg) for name, cfg in checks.items())
    file_types_str = ", ".join(file_types_to_check) if file_types_to_check else ""

    config_string = f"""# Configuration file for i18n-check validation.
# See https://github.com/activist-org/i18n-check for details.
src-dir: {src_dir}
i18n-dir: {i18n_dir}
i18n-src: {i18n_src_file}
file-types-to-check: [{file_types_str}]
checks:
  # Global configurations are applied to all checks.
{checks_str}
"""
    config_file_path = get_config_file_path()
    with open(config_file_path, "w", encoding="utf-8") as f:
        f.write(config_string)


def build_checks() -> dict[str, dict[str, Any]]:
    """
    Build a Dictionary of checks to be checked.

    Returns
    -------
    dict[str,dict[str,Any]]
        A dictionary containing necessary keys, directories and information to check.
    """
    return {
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


def prompt(msg: str, default: str = "") -> str:
    """
    Prompt the user for input, returning a default if the response is empty.

    Parameters
    ----------
    msg : str
        The message displayed to the user as the input prompt.
    default : str
        The value to return if the user provides no input. Defaults to "".

    Returns
    -------
    str
        The stripped user input or default value if the response is empty.
    """
    return input(msg).strip() or default


def prompt_list(msg: str, sep: str = ",") -> list[str]:
    """
    Prompt the user for a list of inputs, returning a list of responses.

    Parameters
    ----------
    msg : str
        The message displayed to the user as the input prompt.
    sep : str
        A separator to separate the response.

    Returns
    -------
    list[str]
        A list of responses in string format collected from the user.
    """
    raw = input(msg).strip()
    return [item.strip() for item in raw.split(sep) if item.strip()] if raw else []


def activate_check(checks: dict, key: str) -> None:
    """
    Prompt the user  to activate a check, unless global is already active.

    Parameters
    ----------
    checks : dict
        A dictionary of checks passed to check.
    key : str
        Lookup key passed for accessing the dictionary.

    Returns
    -------
    None
        Looks up the checks with the lookup key if not prompts the users.
    """
    if checks["global"]["active"]:
        checks[key]["active"] = True
        return
    answer = input(f"{str(checks[key]['title']).capitalize()} check [y]: ").lower()
    checks[key]["active"] = answer in ("y", "")


def directories_to_skip(key: str, title: str) -> str | list[str]:
    """
    Prompt the user for directories to skip for a given check.

    Parameters
    ----------
    key : str
        The check identifier used to determine if the global default applies.
    title : str
        The human-readable check name displayed in the prompt.

    Returns
    -------
    str | list[str]
        The user-provided directory string, or a list containing the default path.
    """
    if key == "global":
        default = [f"frontend{PATH_SEPARATOR}node_modules"]
        raw = input(
            f"Directories to skip for {title} [frontend{PATH_SEPARATOR}node_modules]: "
        ).lower()
        return raw if raw else default
    raw = input(f"Directories to skip for {title} [None]: ").lower()
    return raw if raw else []


def fill_optional_fields(checks: dict, key: str) -> None:
    """
    Populate optional configuration fields for a given check by prompting the user.

    Parameters
    ----------
    checks : dict
        The full checks configuration dict containing all check entries.
    key : str
        The lookup key identifying which check entry to populate.

    Returns
    -------
    None
        Prompts the users to skip the required files.
    """
    v = checks[key]

    if "directories-to-skip" in v:
        v["directories-to-skip"] = directories_to_skip(key, v["title"])

    if "files-to-skip" in v:
        raw = input(f"Files to skip for {v['title']} [None]: ").lower()
        v["files-to-skip"] = raw.split() if raw else []

    if "keys-to-ignore" in v:
        v["keys-to-ignore"] = prompt_list(
            f"Keys to ignore for {v['title']} (comma-separated regex) [None]: "
        )

    if "locales-to-check" in v:
        v["locales-to-check"] = prompt_list(
            f"Locales to check for {v['title']} (comma-separated, e.g., fr, de) [All]: "
        )

    if "search-dirs" in v:
        v["search-dirs"] = prompt_list(
            f"Additional search dirs for {v['title']} (comma-separated) [None]: "
        )


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

    checks: dict[str, dict[str, Any]] = build_checks()

    for key in checks:
        activate_check(checks, key)
        fill_optional_fields(checks, key)

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
