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
from pathlib import Path
from typing import Any, Dict, List

import yaml

# MARK: YAML Reading

# Define the path to the YAML configuration file.
config_path = Path(__file__).parent.parent.parent / ".i18n-check.yaml"

with open(config_path, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# MARK: Paths

src_directory = Path(config["src-dir"]).resolve()
i18n_directory = Path(config["i18n-dir"]).resolve()
i18n_src_file = Path(config["i18n-src"]).resolve()

# MARK: Active Checks

if "global" in config["checks"] and "active" in config["checks"]["global"]:
    global_active = config["checks"]["global"]["active"]

if global_active:
    invalid_keys_active = global_active
    key_identifiers_active = global_active
    non_source_active = global_active
    repeat_keys_active = global_active
    repeat_values_active = global_active
    unused_keys_active = global_active

else:
    if (
        "invalid-keys" in config["checks"]
        and "active" in config["checks"]["invalid-keys"]
    ):
        invalid_keys_active = config["checks"]["invalid-keys"]["active"]

    else:
        invalid_keys_active = False

    if (
        "key-identifiers" in config["checks"]
        and "active" in config["checks"]["key-identifiers"]
    ):
        key_identifiers_active = config["checks"]["key-identifiers"]["active"]

    else:
        key_identifiers_active = False

    if (
        "non-source-keys" in config["checks"]
        and "active" in config["checks"]["non-source-keys"]
    ):
        non_source_active = config["checks"]["non-source-keys"]["active"]

    else:
        non_source_active = False

    if (
        "repeat-keys" in config["checks"]
        and "active" in config["checks"]["repeat-keys"]
    ):
        repeat_keys_active = config["checks"]["repeat-keys"]["active"]

    else:
        repeat_keys_active = False

    if (
        "repeat-values" in config["checks"]
        and "active" in config["checks"]["repeat-values"]
    ):
        repeat_values_active = config["checks"]["repeat-values"]["active"]

    else:
        repeat_values_active = False

    if (
        "unused-keys" in config["checks"]
        and "active" in config["checks"]["unused-keys"]
    ):
        unused_keys_active = config["checks"]["unused-keys"]["active"]

    else:
        unused_keys_active = False

# MARK: Check Skips

global_skip = []
if "global" in config["checks"] and "skip" in config["checks"]["global"]:
    global_skip = config["checks"]["global"]["skip"]

invalid_keys_skip = global_skip
key_identifiers_skip = global_skip
non_source_skip = global_skip
repeat_keys_skip = global_skip
repeat_values_skip = global_skip
unused_keys_skip = global_skip

if "invalid-keys" in config["checks"] and "skip" in config["checks"]["invalid-keys"]:
    invalid_keys_skip += config["checks"]["invalid-keys"]["skip"]

if (
    "key-identifiers" in config["checks"]
    and "skip" in config["checks"]["key-identifiers"]
):
    invalid_keys_skip += config["checks"]["key-identifiers"]["skip"]

if (
    "non-source-keys" in config["checks"]
    and "skip" in config["checks"]["non-source-keys"]
):
    invalid_keys_skip += config["checks"]["non-source-keys"]["skip"]

if "repeat-keys" in config["checks"] and "skip" in config["checks"]["repeat-keys"]:
    invalid_keys_skip += config["checks"]["repeat-keys"]["skip"]

if "repeat-values" in config["checks"] and "skip" in config["checks"]["repeat-values"]:
    invalid_keys_skip += config["checks"]["repeat-values"]["skip"]

if "unused-keys" in config["checks"] and "skip" in config["checks"]["unused-keys"]:
    invalid_keys_skip += config["checks"]["unused-keys"]["skip"]

file_types_to_check = config["file-types-to-check"]
files_to_skip = config["files-to-skip"]
warn_on_nested_keys = config["warn-on-nested-keys"]

# Check for Windows and derive directory path separator.
path_separator = "\\" if os.name == "nt" else "/"

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
        The string of the directory path of a file that has a key.

    Returns
    -------
    str
        The correct i18n key that would match the directory structure passed.
    """

    # Insert underscores between words that are not abbreviations.
    # Only if the word is preceded by a lowercase letter and followed by an uppercase letter.
    valid_key = ""
    for i, c in enumerate(p):
        if c.isupper():
            if i == 0:
                valid_key += c.lower()

            elif p[i - 1].isupper() or (i == len(p) - 1 or p[i + 1].isupper()):
                # Middle or end of an abbreviation: append lowercase without underscore.
                valid_key += c.lower()

            else:
                valid_key += f"_{c.lower()}"

        else:
            valid_key += c

    # Replace path segments like '[id]' that are not useful information for keys.
    valid_key = re.sub(r"\[.*?\]", "", valid_key)

    return (
        valid_key.replace(path_separator, ".")
        .replace("..", ".")
        .replace("._", ".")
        .replace("-", "_")
    )


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

    return text.lower().translate(str.maketrans("", "", punctuation_no_exclamation))


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


def run_check(script_name: str) -> bool:
    """
    Run a check script and report the results via the terminal.

    Parameters
    ----------
    script_name : str
        The filename for the script to run.

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
            ["python", Path("src") / "i18n_check" / "check" / script_name], check=True
        )
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        return False
