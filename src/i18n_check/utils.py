# SPDX-License-Identifier: GPL-3.0-or-later
"""
Utility functions for i18-check.
"""

import glob
import json
import os
import re
import string
from pathlib import Path
from typing import Dict

import yaml

# MARK: YAML Reading

# Define the path to the YAML configuration file.
config_path = Path(__file__).parent.parent.parent / ".i18n-check.yaml"

with open(config_path, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# MARK: Define Globals

src_directory = Path(config["src-dir"]).resolve()
i18n_directory = Path(config["i18n-dir"]).resolve()
i18n_src_file = Path(config["i18n-src"]).resolve()

file_types_to_check = config["file-types-to-check"]
directories_to_skip = config["directories-to-skip"]
files_to_skip = config["files-to-skip"]
warn_on_nested_i18n_src = config["warn-on-nested-i18n-src"]

# Check for Windows and derive directory path separator.
path_separator = "\\" if os.name == "nt" else "/"

# MARK: File Reading


def read_json_file(file_path: str) -> Dict[str, str]:
    """
    Reads a JSON file and returns its content.

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
    directory: str,
    file_types: list[str],
    directories_to_skip: list[str],
    files_to_skip: list[str],
) -> list:
    """
    Collects all files with a given extension from a directory and its subdirectories.

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
    files_to_check : list
        A list of file paths that match the given extension.
    """
    files_to_check = []
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
    Checks that a i18n key is only lowercase letters, number, periods or underscores.

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
    Converts a path to a valid key with period separators and all words being snake case.

    Parameters
    ----------
    p : str
        The string of the directory path of a file that has a key.

    Returns
    -------
    valid_key : str
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
    Filters out parts from potential_key_parts based on specific conditions.

    A key part is excluded if:
    - It appears as a prefix (with an underscore) in the last element of the list.
    - It is a suffix of the last element but is not equal to the full last element.

    Parameters
    ----------
    potential_key_parts : list[str]
        The list of potential key parts to be filtered.

    Returns
    -------
    valid_key_parts : list[str]
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


def get_all_json_files(directory: str, path_separator: str) -> list:
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
    Converts the input text to lowercase and removes punctuation.

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
    Reads multiple files and stores their content in a dictionary.

    Parameters
    ----------
    file_paths : list[str]
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
