# SPDX-License-Identifier: GPL-3.0-or-later
"""
Utility functions for i18n-check.
"""

import glob
import json
import os
import re
import string
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml
from rich import print as rprint

from i18n_check.cli.generate_config_file import (
    YAML_CONFIG_FILE_PATH,
    generate_config_file,
)

# Check for Windows and derive directory path separator.
path_separator = "\\" if os.name == "nt" else "/"

# MARK: YAML Reading

i18n_check_root_path = Path.cwd()

if not Path(YAML_CONFIG_FILE_PATH).is_file():
    generate_config_file()

if not Path(YAML_CONFIG_FILE_PATH).is_file():
    print(
        "No configuration file. Please generate an .i18n-check.yaml file with i18n-check -gcf."
    )
    exit(1)

with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# MARK: Paths

config_src_directory = (i18n_check_root_path / Path(config["src-dir"])).resolve()
config_i18n_directory = (i18n_check_root_path / Path(config["i18n-dir"])).resolve()
config_i18n_src_file = (i18n_check_root_path / Path(config["i18n-src"])).resolve()

# MARK: File Types

config_file_types_to_check = config["file-types-to-check"]

# MARK: Global

config_global_active = False
config_global_directories_to_skip = []
config_global_files_to_skip = []

if "global" in config["checks"]:
    if "active" in config["checks"]["global"]:
        config_global_active = config["checks"]["global"]["active"]

    if "directories-to-skip" in config["checks"]["global"]:
        config_global_directories_to_skip = config["checks"]["global"][
            "directories-to-skip"
        ]

    if "files-to-skip" in config["checks"]["global"]:
        config_global_files_to_skip = config["checks"]["global"]["files-to-skip"]

# MARK: Invalid Keys

config_invalid_keys_active = config_global_active
config_invalid_keys_directories_to_skip = config_global_directories_to_skip.copy()
config_invalid_keys_files_to_skip = config_global_files_to_skip.copy()
config_invalid_key_regexes_to_ignore = []

if "invalid-keys" in config["checks"]:
    if "active" in config["checks"]["invalid-keys"]:
        config_invalid_keys_active = config["checks"]["invalid-keys"]["active"]

    if "directories-to-skip" in config["checks"]["invalid-keys"]:
        config_invalid_keys_directories_to_skip += config["checks"]["invalid-keys"][
            "directories-to-skip"
        ]

    if "files-to-skip" in config["checks"]["invalid-keys"]:
        config_invalid_keys_files_to_skip += config["checks"]["invalid-keys"][
            "files-to-skip"
        ]

    if "keys-to-ignore" in config["checks"]["invalid-keys"]:
        keys_to_ignore = config["checks"]["invalid-keys"]["keys-to-ignore"]

        if isinstance(keys_to_ignore, str):
            config_invalid_key_regexes_to_ignore = (
                [keys_to_ignore] if keys_to_ignore else []
            )

        elif isinstance(keys_to_ignore, list):
            config_invalid_key_regexes_to_ignore = keys_to_ignore

        else:
            config_invalid_key_regexes_to_ignore = []

# MARK: Non-Existent Keys

config_non_existent_keys_active = config_global_active
config_non_existent_keys_directories_to_skip = config_global_directories_to_skip.copy()
config_non_existent_keys_files_to_skip = config_global_files_to_skip.copy()

if "non-existent-keys" in config["checks"]:
    if "active" in config["checks"]["non-existent-keys"]:
        config_non_existent_keys_active = config["checks"]["non-existent-keys"][
            "active"
        ]

    if "directories-to-skip" in config["checks"]["non-existent-keys"]:
        config_non_existent_keys_directories_to_skip += config["checks"][
            "non-existent-keys"
        ]["directories-to-skip"]

    if "files-to-skip" in config["checks"]["non-existent-keys"]:
        config_non_existent_keys_files_to_skip += config["checks"]["global"][
            "files-to-skip"
        ]

# MARK: Non-Source Keys

# Note: We don't have skipped files or directories for non-source-keys.
config_non_source_keys_active = config_global_active

if (
    "non-source-keys" in config["checks"]
    and "active" in config["checks"]["non-source-keys"]
):
    config_non_source_keys_active = config["checks"]["non-source-keys"]["active"]

# MARK: Repeat Keys

# Note: We don't have skipped files or directories for repeat-keys.
config_repeat_keys_active = config_global_active

if "repeat-keys" in config["checks"] and "active" in config["checks"]["repeat-keys"]:
    config_repeat_keys_active = config["checks"]["repeat-keys"]["active"]

# MARK: Repeat Values

# Note: We don't have skipped files or directories for repeat-values.
config_repeat_values_active = config_global_active

if (
    "repeat-values" in config["checks"]
    and "active" in config["checks"]["repeat-values"]
):
    config_repeat_values_active = config["checks"]["repeat-values"]["active"]

# MARK: Unused Keys

config_unused_keys_active = config_global_active
config_unused_keys_directories_to_skip = config_global_directories_to_skip.copy()
config_unused_keys_files_to_skip = config_global_files_to_skip.copy()

if "unused-keys" in config["checks"]:
    if "active" in config["checks"]["unused-keys"]:
        config_unused_keys_active = config["checks"]["unused-keys"]["active"]

    if "directories-to-skip" in config["checks"]["unused-keys"]:
        config_unused_keys_directories_to_skip += config["checks"]["unused-keys"][
            "directories-to-skip"
        ]

    if "files-to-skip" in config["checks"]["unused-keys"]:
        config_unused_keys_files_to_skip += config["checks"]["unused-keys"][
            "files-to-skip"
        ]

# MARK: Sorted Keys

# Note: We don't have skipped files or directories for sorted-keys.
config_sorted_keys_active = config_global_active

if "sorted-keys" in config["checks"] and "active" in config["checks"]["sorted-keys"]:
    config_sorted_keys_active = config["checks"]["sorted-keys"]["active"]

# MARK: Nested Keys

# Note: We don't have skipped files or directories for nested-keys.
config_nested_keys_active = config_global_active

if "nested-keys" in config["checks"] and "active" in config["checks"]["nested-keys"]:
    config_nested_keys_active = config["checks"]["nested-keys"]["active"]

# MARK: Missing Keys

config_missing_keys_active = config_global_active
config_missing_keys_locales_to_check = []

if "missing-keys" in config["checks"]:
    if "active" in config["checks"]["missing-keys"]:
        config_missing_keys_active = config["checks"]["missing-keys"]["active"]

    if "locales-to-check" in config["checks"]["missing-keys"]:
        config_missing_keys_locales_to_check = config["checks"]["missing-keys"][
            "locales-to-check"
        ]

# MARK: Aria Labels

# Note: We don't have skipped files or directories for aria-labels.
config_aria_labels_active = config_global_active

if "aria-labels" in config["checks"] and "active" in config["checks"]["aria-labels"]:
    config_aria_labels_active = config["checks"]["aria-labels"]["active"]

# MARK: Alt Texts

# Note: We don't have skipped files or directories for alt-texts.
config_alt_texts_active = config_global_active

if "alt-texts" in config["checks"] and "active" in config["checks"]["alt-texts"]:
    config_alt_texts_active = config["checks"]["alt-texts"]["active"]

# MARK: File Reading


def read_json_file(file_path: str | Path) -> Any:
    """
    Read JSON file and return its content as a Python object.

    Parameters
    ----------
    file_path : str
        The path to the JSON file.

    Returns
    -------
    dict
        The content of the JSON file.
    """
    with open(file_path, encoding="utf-8") as f:
        return json.loads(f.read())


# MARK: Collect Files


def collect_files_to_check(
    directory: str | Path,
    file_types: list[str],
    directories_to_skip: list[str],
    files_to_skip: list[str],
) -> List[str]:
    """
    Collect all files with a given extension from a directory and its subdirectories.

    Parameters
    ----------
    directory : str
        The directory to search in.

    file_types : list[str]
        The file extensions to search in.

    directories_to_skip : list[str]
        Directories to not include in the search.

    files_to_skip : list[str]
        Files to not include in the check.

    Returns
    -------
    list
        A list of file paths that match the given extension.
    """
    files_to_check: List[str] = []
    for root, dirs, files in os.walk(directory):
        # Skip directories in directories_to_skip.
        if all(skip_dir not in root for skip_dir in directories_to_skip):
            # Collect files that match the file_types and are not in files_to_skip.
            files_to_check.extend(
                os.path.join(root, file)
                for file in files
                if not any(root.startswith(d) for d in directories_to_skip)
                and any(file.endswith(file_type) for file_type in file_types)
                and file not in files_to_skip
            )

    return files_to_check


# MARK: Invalid Keys


def is_valid_key(k: str) -> bool:
    """
    Check that an i18n key is only lowercase letters, number, periods or underscores.

    Parameters
    ----------
    k : str
        The key to check.

    Returns
    -------
    bool
        Whether the given key matches the specified style.
    """
    pattern = r"^[a-z0-9._]+$"

    return bool(re.match(pattern, k))


# MARK: Renaming Keys


def path_to_valid_key(p: str) -> str:
    """
    Convert a path to a valid key with period separators and all words being snake case.

    Parameters
    ----------
    p : str
        The path to the file where an i18n key is used.

    Returns
    -------
    str
        The valid base key that can be used for i18n keys in this file.

    Notes
    -----
    - Insert underscores between words that are not abbreviations
        - Only if the word is preceded by a lowercase letter and followed by an uppercase letter
    - [str] values are removed in this step as [id] uuid path routes don't add anything to keys
    """
    # Remove path segments like '[id]'.
    p = re.sub(r"\[.*?\]", "", p)
    # Replace path separator with a dot.
    p = p.replace(path_separator, ".")

    # Convert camelCase or PascalCase to snake_case, but preserve acronyms.
    p = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", p)  # ABCxyz -> ABC_xyz
    p = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", p)  # abcXyz -> abc_xyz

    p = p.lower()
    p = p.replace("..", ".").replace("._", ".").replace("-", "_")

    return p.strip(".")


# MARK: Valid Parts


def filter_valid_key_parts(potential_key_parts: list[str]) -> list[str]:
    """
    Filter out parts from potential_key_parts based on specific conditions.

    A key part is excluded if:
    - It appears as a prefix (with an underscore) in the last element of the list.
    - It is a suffix of the last element but is not equal to the full last element.

    Parameters
    ----------
    potential_key_parts : list[str]
        The list of potential key parts to be filtered.

    Returns
    -------
    list[str]
        The filtered list of valid key parts.
    """
    return [
        p
        for p in potential_key_parts
        if f"{p}_" not in potential_key_parts[-1]
        and not (
            p == potential_key_parts[-1][-len(p) :] and p != potential_key_parts[-1]
        )
    ]


# MARK: JSON Files


def get_all_json_files(directory: str | Path, path_separator: str) -> List[str]:
    """
    Get all JSON files in the specified directory.

    Parameters
    ----------
    directory : str
        The directory in which to search for JSON files.

    path_separator : str
        The path separator to be used in the directory path.

    Returns
    -------
    list
        A list of paths to all JSON files in the specified directory.
    """
    return glob.glob(f"{directory}{path_separator}*.json")


# MARK: Lower and Remove Punctuation


def lower_and_remove_punctuation(text: str) -> str:
    """
    Convert the input text to lowercase and remove punctuation.

    Parameters
    ----------
    text : str
        The input text to process.

    Returns
    -------
    str
        The processed text with lowercase letters and no punctuation.
    """
    punctuation_no_exclamation = string.punctuation.replace("!", "")

    if isinstance(text, str):
        return text.lower().translate(str.maketrans("", "", punctuation_no_exclamation))

    else:
        return text


# MARK: Reading to Dicts


def read_files_to_dict(files: list[str]) -> Dict[str, str]:
    """
    Read multiple files and store their content in a dictionary.

    Parameters
    ----------
    files : list[str]
        A list of file paths to read.

    Returns
    -------
    dict
        A dictionary where keys are file paths and values are file contents.
    """
    file_contents = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            file_contents[file] = f.read()

    return file_contents


# MARK: Run Check


def run_check(script_name: str, include_suppress_errors: bool = False) -> bool:
    """
    Run a check script and report the results via the terminal.

    Parameters
    ----------
    script_name : str
        The name for the script to run.

    include_suppress_errors : bool, optional, default=False
        Whether to suppress subprocess error output.

    Returns
    -------
    bool
        Whether the given script passed or not from subprocess.run.check.

    Raises
    -------
    subprocess.CalledProcessError
        An error that the given check script has failed.
    """
    try:
        subprocess.run(
            ["python", "-m", f"i18n_check.check.{script_name}"],
            check=True,
        )
        return True

    except subprocess.CalledProcessError as e:
        if not include_suppress_errors:
            print(f"Error running {script_name}: {e}\n")
            sys.exit(1)

        return False


# MARK: Replace Keys


def replace_text_in_file(path: str | Path, old: str, new: str) -> None:
    """
    Replace all occurrences of a substring with a new string in a file.

    Parameters
    ----------
    path : str or Path
        The path to the file in which to perform the replacement.

    old : str
        The substring to be replaced.

    new : str
        The string to replace the old substring with.
    """
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    if old in content:
        content = content.replace(old, new)
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        rprint(f"[yellow]\n✨ Replaced '{old}' with '{new}' in {path}[/yellow]")
