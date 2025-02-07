"""
Utility functions for the i18 check keys.
"""

import json
import os 
import re
from pathlib import Path
import yaml
from collections.abc import MutableMapping
import glob
import string



# MARK: YAML Reading

# Define the path to the YAML configuration file
config_path = Path(__file__).parent.parent.parent / ".i18n-check.yaml"

with open(config_path, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Define Globals


i18n_check_dir = str(Path(config["i18n-dir"]).resolve())
json_file_directory = Path(config["i18n-dir"]).resolve()
frontend_directory = Path(config["src-dir"]).resolve()
en_us_json_file = Path(config["i18n-src"]).resolve()
i18n_map_file = Path(config["i18n-map"]).resolve()
frontend_types_dir = Path(config["types_dir"]).resolve()


SPDX_LICENSE_IDENTIFIER = "AGPL-3.0-or-later"

# Check for Windows and derive directory path separator.
path_separator = "\\" if os.name == "nt" else "/"


file_types_to_check = [".vue", ".ts", ".js"]
directories_to_skip = [
    i18n_check_dir,
    str((frontend_directory / ".nuxt").resolve()),
    str((frontend_directory / ".output").resolve()),
    str((frontend_directory / "node_modules").resolve()),
]


# MARK: File Reading

def read_json_file(file_path):
    """
    Reads a JSON file and returns its content.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file.   
    """
    with open(file_path, encoding="utf-8") as f:
        return json.loads(f.read())

# MARK: collecting File

def collect_files(directory, file_types, directories_to_skip, files_to_skip):
    """
    Collects all files with a given extension from a directory and its subdirectories.

    Parameters:
        directory (str): The directory to search in.
        extension (str): The file extension to look for.

    Returns:
        list: A list of file paths that match the given extension.
    """
    files_to_check = []
    for root, dirs, files in os.walk(directory):
        files_to_check.extend(
            os.path.join(root, file)
            for file in files
            if all(root[: len(d)] != d for d in directories_to_skip)
            and any(file[-len(t) :] == t for t in file_types)
            and file not in files_to_skip
        )
    return files_to_check

# MARK: Invalid Keys

def is_valid_key(s):
    """
    Checks that a i18n key is only lowercase letters, number, periods or underscores.
    """
    pattern = r"^[a-z0-9._]+$"
    return bool(re.match(pattern, s))


# MARK: Renaming Keys


def path_to_valid_key(p: str):
    """
    Converts a path to a valid key with period separators and all words being snake case.

    Note: [id] and [group_id] are removed in this step as it doesn't add anything to keys.

    Parameters
    ----------
    p : list str
        The string of the directory path of a file that has a key.

    Returns
    -------
    valid_key : str
        The correct i18n key that would match the directory structure passed.
    """

    # Insert underscores between words, but only if the word is preceded by a lowercase letter and followed by an uppercase letter (i.e. except for abbreviations).
    valid_key = ""
    for i, c in enumerate(p):
        if c.isupper():
            if i == 0:
                valid_key += c.lower()

            elif p[i - 1].isupper() and (i == len(p) - 1 or p[i + 1].isupper()):
                # Middle or end of an abbreviation: append lowercase without underscore
                valid_key += c.lower()

            else:
                valid_key += f"_{c.lower()}"

        else:
            valid_key += c

    return (
        valid_key.replace(path_separator, ".")
        .replace("._", ".")
        .replace("-", "_")
        .replace(".[id]", "")
        .replace(".[group_id]", "")
    )

# MARK: Valid Parts

def filter_valid_key_parts(potential_key_parts):
    """
    Filters out parts from potential_key_parts based on specific conditions.
    
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

# MARK: Flattening Dicts

def flatten_nested_dict(
    dictionary: MutableMapping, parent_key: str = "", sep: str = "."
) -> MutableMapping:
    """
    Flattens a nested dictionary.

    Parameters
    ----------
    d : MutableMapping
        The nested dictionary to flatten.

    parent_key : str
        The key of the current value being flattened.

    sep : str
        The separator to be used to join the nested keys.

    Returns
    -------
    MutableMapping
        The flattened version of the given nested dictionary.
    """
    items = []
    for k, v in dictionary.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_nested_dict(v, new_key, sep=sep).items())

        else:
            items.append((new_key, v))

    return dict(items)

# MARK: JSON Files

def get_all_json_files(directory, path_separator):
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

def lower_and_remove_punctuation(value):
    """
    Converts the input text to lowercase and removes punctuation.

    Parameters:
        text (str): The input text to process.

    Returns:
        str: The processed text with lowercase letters and no punctuation.
    """
    punctuation_no_exclamation = string.punctuation.replace("!", "")
    return value.lower().translate(str.maketrans("", "", punctuation_no_exclamation))

# MARK: Reading to Dicts
def read_files_to_dict(files):
    """
    Reads multiple files and stores their content in a dictionary.

    Parameters:
        file_paths (list): A list of file paths to read.

    Returns:
        dict: A dictionary where keys are file paths and values are file contents.
    """
    file_contents = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            file_contents[file] = f.read()
    return file_contents

