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
from typing import Any, Dict, List, Match, Union

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

# MARK: Invalid Keys

config_invalid_keys_active = config_global_active
config_invalid_keys_directories_to_skip = config_global_directories_to_skip.copy()
config_invalid_keys_files_to_skip = config_global_files_to_skip.copy()
config_invalid_key_regexes_to_ignore = []

if "invalid-keys" in config["checks"]:
    if "active" in config["checks"]["invalid-keys"]:
        config_invalid_keys_active = config["checks"]["invalid-keys"]["active"]

    if "directories-to-skip" in config["checks"]["invalid-keys"]:
        config_invalid_keys_directories_to_skip += [
            CWD_PATH
            / Path(d.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for d in config["checks"]["invalid-keys"]["directories-to-skip"]
        ]

    if "files-to-skip" in config["checks"]["invalid-keys"]:
        config_invalid_keys_files_to_skip += [
            CWD_PATH
            / Path(f.replace("/", PATH_SEPARATOR).replace("\\", PATH_SEPARATOR))
            for f in config["checks"]["invalid-keys"]["files-to-skip"]
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


def sort_keys(file_path: Path) -> bool:
    """
    Sort keys in files alphabetically.

    Parameters
    ----------
    file_path : Path
        Path to the file to sort (JSON or TypeScript).

    Returns
    -------
    bool
        True if the file was modified, False otherwise.
    """
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    if ext == ".json":
        _sort_json_file(file_path)
        return True
    elif ext in {".ts", ".tsx"}:
        return _sort_typescript_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _sort_json_file(file_path: Path) -> None:
    """
    Sort keys in a JSON file.

    Parameters
    ----------
    file_path : Path
        Path to the JSON file to be sorted.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return

    # Find the opening and closing braces of the main object.
    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        if "{" in line and start_idx is None:
            start_idx = i
        if "}" in line:
            end_idx = i

    if start_idx is None or end_idx is None:
        return

    # Extract entries between braces.
    entries = []
    i = start_idx + 1

    while i < end_idx:
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines.
        if not stripped:
            i += 1
            continue

        # Match key at the start of a key-value pair.
        match = re.match(r'^"([^"]+)"\s*:\s*', stripped)
        if match:
            key = match.group(1)
            value_lines = [line]

            # Check if value is a nested object.
            if "{" in stripped and "}" not in stripped:
                # Multi-line nested object - collect all lines until closing brace.
                i += 1
                brace_count = 1
                while i < end_idx and brace_count > 0:
                    next_line = lines[i]
                    value_lines.append(next_line)
                    brace_count += next_line.count("{") - next_line.count("}")
                    i += 1
                i -= 1  # Adjust because outer loop will increment.

            entries.append((key, value_lines))

        i += 1

    # Sort entries by key.
    sorted_entries = sorted(entries, key=lambda x: x[0])

    # Rebuild the file.
    output_lines = []

    # Add lines before entries.
    output_lines.extend(lines[: start_idx + 1])

    # Add sorted entries.
    for idx, (key, value_lines) in enumerate(sorted_entries):
        # Process the entry.
        for line_idx, vline in enumerate(value_lines):
            if line_idx == len(value_lines) - 1:
                # Last line of this entry - handle comma.
                clean_line = vline.rstrip().rstrip(",")

                # Add comma to all but last entry.
                if idx < len(sorted_entries) - 1:
                    output_lines.append(clean_line + ",\n")
                else:
                    output_lines.append(clean_line + "\n")
            else:
                # Middle lines - keep as is.
                output_lines.append(vline)

    # Add closing brace and any content after.
    output_lines.extend(lines[end_idx:])

    # Write back to file.
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)


def _sort_typescript_file(file_path: Path) -> bool:
    """
    Sort i18n comment blocks in a TypeScript file.

    Parameters
    ----------
    file_path : Path
        Path to the TypeScript file to process.

    Returns
    -------
    bool
        True if the file was modified, False otherwise.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] Could not read file {file_path}: {e}")
        return False

    # 1. Define the regex patterns.
    # Matches the whole block (Header + Key lines).
    block_pattern = re.compile(
        r"(//\s*This file contains the following i18n keys:[^\n]*\n)"  # Header.
        r"((?:[ \t]*//(?:[^\n]*\n?))+)",  # Key lines block.
        re.MULTILINE,
    )
    # Matches a single key line and extracts parts.
    key_line_pattern = re.compile(
        r"^([ \t]*//[ \t]*-[ \t]*)"  # Group 1: Prefix (indent, //, -).
        r'(?:([\'"`]?)(i18n\.[a-zA-Z0-9._-]+)\2)'  # Groups 2&3: Quote and Key.
        r"([^\n]*)"  # Group 4: Suffix.
        r"\n?$"
    )

    def replacer(match: Match[str]) -> str:
        """
        Compute the matched keys block and return the sorted block.

        Parameters
        ----------
        match : Match[str]
            The regex match object containing the keys block.

        Returns
        -------
        str
            The sorted keys block with original formatting preserved.
        """
        groups = match.groups()
        if len(groups) < 2:
            return match.group(0)

        header = groups[0]
        keys_block = groups[1]
        lines = keys_block.splitlines(keepends=True)

        key_entries: List[Dict[str, Any]] = []
        original_order: List[Union[str, int]] = []

        for i, line in enumerate(lines):
            m = key_line_pattern.match(line)
            if m:
                prefix, quote, key, suffix = m.groups()
                key_entries.append(
                    {
                        "sort_key": key.lower(),
                        "prefix": prefix,
                        "quote": quote,
                        "key": key,
                        "suffix": suffix,
                    }
                )
                original_order.append(f"KEY_ENTRY_{len(key_entries) - 1}")
            else:
                # Add non-key lines to maintain their order.
                original_order.append(line)

        if not key_entries:
            return match.group(0)  # Return original block if no keys found.

        # Sort the key entries.
        key_entries.sort(key=lambda x: x["sort_key"])

        # Rebuild the new lines block.
        reconstructed_lines = []
        key_idx = 0
        for item in original_order:
            if isinstance(item, str) and item.startswith("KEY_ENTRY_"):
                entry = key_entries[key_idx]
                quoted_key = (
                    f"{entry['quote']}{entry['key']}{entry['quote']}"
                    if entry["quote"]
                    else entry["key"]
                )
                reconstructed_lines.append(
                    f"{entry['prefix']}{quoted_key}{entry['suffix']}\n"
                )
                key_idx += 1
            elif isinstance(item, str):
                reconstructed_lines.append(item)  # Add non-key line back.

        return header + "".join(reconstructed_lines)

    # 2. Use re.sub with a function to process and replace the block.
    new_content = block_pattern.sub(replacer, content, count=1)

    # 3. Write only if modified.
    if new_content != content:
        try:
            file_path.write_text(new_content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"[ERROR] Could not write to file {file_path}: {e}")

    return False


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
