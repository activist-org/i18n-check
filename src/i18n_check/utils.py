# SPDX-License-Identifier: GPL-3.0-or-later
"""
Utility functions for i18n-check.
"""

import glob
import json
import os
import re
import string
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

import yaml
from rich import print as rprint

# Check for Windows and derive directory path separator.
PATH_SEPARATOR = "\\" if os.name == "nt" else "/"

# MARK: Base Paths

CWD_PATH = Path.cwd()


def get_config_file_path() -> Path:
    """
    Get the path to the i18n-check configuration file.

    Checks for both .yaml and .yml extensions, preferring .yaml if both exist.

    Returns
    -------
    Path
        The path to the configuration file (.yaml or .yml).
    """
    yaml_path = CWD_PATH / ".i18n-check.yaml"
    yml_path = CWD_PATH / ".i18n-check.yml"

    # Prefer .yaml if it exists, otherwise check for .yml.
    if yaml_path.is_file():
        return yaml_path
    elif yml_path.is_file():
        return yml_path
    else:
        # Default to .yaml for new files.
        return yaml_path


# Import after defining get_config_file_path to avoid circular import.
from i18n_check.cli.generate_config_file import generate_config_file  # noqa: E402

YAML_CONFIG_FILE_PATH = get_config_file_path()
INTERNAL_TEST_FRONTENDS_DIR_PATH = Path(__file__).parent / "test_frontends"

# MARK: YAML Reading

if not Path(YAML_CONFIG_FILE_PATH).is_file():
    generate_config_file()

if not Path(YAML_CONFIG_FILE_PATH).is_file():
    print(
        "No configuration file. Please generate a configuration file (.i18n-check.yaml or .i18n-check.yml) with i18n-check -gcf."
    )
    exit(1)

with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# MARK: Paths

config_src_directory = (
    CWD_PATH
    / Path(config["src-dir"].replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
).resolve()
config_i18n_directory = (
    CWD_PATH
    / Path(
        config["i18n-dir"].replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR)
    )
).resolve()
config_i18n_src_file = (
    CWD_PATH
    / Path(
        config["i18n-src"].replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR)
    )
).resolve()

# MARK: File Types

config_file_types_to_check = config["file-types-to-check"]

# MARK: Global

# Note: We initialize per-check active states with global defaults.
config_global_active = False
config_global_directories_to_skip = []
config_global_files_to_skip = []

if "global" in config["checks"]:
    if "active" in config["checks"]["global"]:
        config_global_active = config["checks"]["global"]["active"]

    if "directories-to-skip" in config["checks"]["global"]:
        config_global_directories_to_skip = [
            CWD_PATH
            / Path(d.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for d in config["checks"]["global"]["directories-to-skip"]
        ]

    if "files-to-skip" in config["checks"]["global"]:
        config_global_files_to_skip = [
            CWD_PATH
            / Path(f.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for f in config["checks"]["global"]["files-to-skip"]
        ]

# MARK: Key Formatting

# Note: We don't have skipped files or directories for non-source-keys.
config_key_formatting_active = config_global_active
config_key_formatting_regexes_to_ignore = []

if "key-formatting" in config["checks"]:
    if "active" in config["checks"]["key-formatting"]:
        config_key_formatting_active = config["checks"]["key-formatting"]["active"]

    if "keys-to-ignore" in config["checks"]["key-formatting"]:
        _keys_to_ignore = config["checks"]["key-formatting"]["keys-to-ignore"]

        if isinstance(_keys_to_ignore, str):
            config_key_formatting_regexes_to_ignore = (
                [_keys_to_ignore] if _keys_to_ignore else []
            )

        elif isinstance(_keys_to_ignore, list):
            config_key_formatting_regexes_to_ignore = _keys_to_ignore

        else:
            config_key_formatting_regexes_to_ignore = []

# MARK: Key Naming

config_key_naming_active = config_global_active

config_key_naming_directories_to_skip = config_global_directories_to_skip.copy()
config_key_naming_files_to_skip = config_global_files_to_skip.copy()
config_key_naming_regexes_to_ignore = []

if "key-naming" in config["checks"]:
    if "active" in config["checks"]["key-naming"]:
        config_key_naming_active = config["checks"]["key-naming"]["active"]

    if "directories-to-skip" in config["checks"]["key-naming"]:
        config_key_naming_directories_to_skip += [
            CWD_PATH
            / Path(d.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for d in config["checks"]["key-naming"]["directories-to-skip"]
        ]

    if "files-to-skip" in config["checks"]["key-naming"]:
        config_key_naming_files_to_skip += [
            CWD_PATH
            / Path(f.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for f in config["checks"]["global"]["files-to-skip"]
        ]

    if "keys-to-ignore" in config["checks"]["key-naming"]:
        _keys_to_ignore = config["checks"]["key-naming"]["keys-to-ignore"]

        if isinstance(_keys_to_ignore, str):
            config_key_naming_regexes_to_ignore = (
                [_keys_to_ignore] if _keys_to_ignore else []
            )

        elif isinstance(_keys_to_ignore, list):
            config_key_naming_regexes_to_ignore = _keys_to_ignore

        else:
            config_key_naming_regexes_to_ignore = []

# MARK: Nonexistent Keys

config_nonexistent_keys_active = config_global_active
config_nonexistent_keys_directories_to_skip = config_global_directories_to_skip.copy()
config_nonexistent_keys_files_to_skip = config_global_files_to_skip.copy()

if "nonexistent-keys" in config["checks"]:
    if "active" in config["checks"]["nonexistent-keys"]:
        config_nonexistent_keys_active = config["checks"]["nonexistent-keys"]["active"]

    if "directories-to-skip" in config["checks"]["nonexistent-keys"]:
        config_nonexistent_keys_directories_to_skip += [
            CWD_PATH
            / Path(d.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for d in config["checks"]["nonexistent-keys"]["directories-to-skip"]
        ]

    if "files-to-skip" in config["checks"]["nonexistent-keys"]:
        config_nonexistent_keys_files_to_skip += [
            CWD_PATH
            / Path(f.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for f in config["checks"]["global"]["files-to-skip"]
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
        config_unused_keys_directories_to_skip += [
            CWD_PATH
            / Path(d.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for d in config["checks"]["unused-keys"]["directories-to-skip"]
        ]

    if "files-to-skip" in config["checks"]["unused-keys"]:
        config_unused_keys_files_to_skip += [
            CWD_PATH
            / Path(f.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for f in config["checks"]["unused-keys"]["files-to-skip"]
        ]

# MARK: Sorted Keys

# Note: We don't have skipped files or directories for sorted-keys.
config_sorted_keys_active = config_global_active

if "sorted-keys" in config["checks"] and "active" in config["checks"]["sorted-keys"]:
    config_sorted_keys_active = config["checks"]["sorted-keys"]["active"]

# MARK: Nested Keys

# Note: We don't have skipped files or directories for nested-files.
config_nested_files_active = config_global_active

if "nested-files" in config["checks"] and "active" in config["checks"]["nested-files"]:
    config_nested_files_active = config["checks"]["nested-files"]["active"]

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


@lru_cache(maxsize=128)
def _collect_files_to_check_cached(
    directory: str,
    file_types_to_check: tuple[str, ...],
    directories_to_skip: tuple[str, ...],
    files_to_skip: tuple[str, ...],
) -> tuple[str, ...]:
    """
    Cached implementation of collect_files_to_check.

    This internal function uses hashable types (tuples and strings) to enable caching.

    Parameters
    ----------
    directory : str
        The resolved directory path to search in.

    file_types_to_check : tuple[str, ...]
        Tuple of file extensions to search for.

    directories_to_skip : tuple[str, ...]
        Tuple of resolved directory paths to skip.

    files_to_skip : tuple[str, ...]
        Tuple of resolved file paths to skip.

    Returns
    -------
    tuple[str, ...]
        Tuple of file paths that match the given extensions.
    """
    directory_path = Path(directory).resolve()
    skip_dirs_resolved = [Path(d).resolve() for d in directories_to_skip]
    skip_files_resolved = [Path(f).resolve() for f in files_to_skip]
    files_to_check: List[str] = []

    for root, dirs, files in os.walk(directory_path):
        root_path = Path(root).resolve()

        # Skip directories in directories_to_skip and later files in files_to_skip.
        if any(
            root_path == skip_dir or root_path.is_relative_to(skip_dir)
            for skip_dir in skip_dirs_resolved
        ):
            continue

        for file in files:
            file_path = (root_path / file).resolve()
            if (
                any(
                    file_path.suffix == f".{ftype.lstrip('.')}"
                    for ftype in file_types_to_check
                )
                and file_path not in skip_files_resolved
            ):
                files_to_check.append(str(file_path))

    return tuple(files_to_check)


def collect_files_to_check(
    directory: str | Path,
    file_types_to_check: list[str],
    directories_to_skip: list[Path],
    files_to_skip: list[Path],
) -> List[str]:
    """
    Collect all files with a given extension from a directory and its subdirectories.

    This function is cached, so repeated calls with the same parameters will return
    the cached result without re-scanning the filesystem.

    Parameters
    ----------
    directory : str
        The directory to search in.

    file_types_to_check : list[str]
        The file extensions to search in.

    directories_to_skip : list[Path]
        Paths to directories to not include in the search.

    files_to_skip : list[Path]
        Paths to files to not include in the check.

    Returns
    -------
    list
        A list of file paths that match the given extension.
    """
    # Convert to hashable types and call cached implementation.
    directory_str = str(Path(directory).resolve())
    file_types_tuple = tuple(file_types_to_check)
    directories_tuple = tuple(str(Path(d).resolve()) for d in directories_to_skip)
    files_tuple = tuple(str(Path(f).resolve()) for f in files_to_skip)

    result = _collect_files_to_check_cached(
        directory_str,
        file_types_tuple,
        directories_tuple,
        files_tuple,
    )

    # Convert back to list for backward compatibility.
    return list(result)


# MARK: Valid Keys


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
    p = p.replace(PATH_SEPARATOR, ".")

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


@lru_cache(maxsize=32)
def _get_all_json_files_cached(directory: str) -> tuple[str, ...]:
    """
    Cached implementation of get_all_json_files.

    This internal function uses hashable types (strings and tuples) to enable caching.

    Parameters
    ----------
    directory : str
        The resolved directory path to search in.

    Returns
    -------
    tuple[str, ...]
        Tuple of JSON file paths.
    """
    json_files = glob.glob(f"{directory}{PATH_SEPARATOR}*.json")
    return tuple(json_files)


def get_all_json_files(directory: str | Path) -> List[str]:
    """
    Get all JSON files in the specified directory.

    This function is cached to avoid repeated filesystem scans.

    Parameters
    ----------
    directory : str
        The directory in which to search for JSON files.

    Returns
    -------
    list
        A list of paths to all JSON files in the specified directory.
    """
    directory_str = str(Path(directory).resolve())
    result = _get_all_json_files_cached(directory_str)
    return list(result)


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
