# SPDX-License-Identifier: GPL-3.0-or-later
"""
Runs all i18n checks for the project.

Examples
--------
Run the following script in terminal:

>>> i18n-check -a
"""

import argparse
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from pathlib import Path

from rich import print as rprint

from i18n_check.check.alt_texts import alt_texts_check_and_fix
from i18n_check.check.aria_labels import aria_labels_check_and_fix
from i18n_check.check.key_formatting import (
    invalid_key_formats_check_and_fix,
    invalid_keys_by_format,
)
from i18n_check.check.key_naming import (
    invalid_key_names_check_and_fix,
    invalid_keys_by_name,
)
from i18n_check.check.missing_keys import missing_keys_check_and_fix
from i18n_check.check.nested_files import nested_files_check
from i18n_check.check.non_source_keys import non_source_keys_check, non_source_keys_dict
from i18n_check.check.nonexistent_keys import (
    all_used_i18n_keys,
    nonexistent_keys_check_and_fix,
)
from i18n_check.check.repeat_keys import repeat_keys_check
from i18n_check.check.repeat_values import (
    json_repeat_value_counts,
    repeat_value_error_report,
    repeat_values_check,
)
from i18n_check.check.sorted_keys import sorted_keys_check_and_fix
from i18n_check.check.unused_keys import unused_keys, unused_keys_check
from i18n_check.utils import (
    config_alt_texts_active,
    config_aria_labels_active,
    config_key_formatting_active,
    config_key_naming_active,
    config_missing_keys_active,
    config_nested_files_active,
    config_non_source_keys_active,
    config_nonexistent_keys_active,
    config_repeat_keys_active,
    config_repeat_values_active,
    config_sorted_keys_active,
    config_unused_keys_active,
)

# MARK: Run All


def fill_partial_checks(
    pre_configured_checks: dict[str, tuple[bool, list[partial[bool]], str]],
) -> tuple[list[bool], list[partial[bool]], list[str]]:
    """
    Populate necessary values into specific Arrays.

    Parameters
    ----------
    pre_configured_checks : dict[str,tuple[bool,list[partial[bool]],str]]
        Necessary values are passed as a dict to unpack and process.

    Returns
    -------
    tuple[list[bool],list[partial[bool]],list[str]]
        A tuple containing a list of checked boolean values, a list of partial[boolean]
        and finally all the checked names as list of str.
    """
    checks: list[partial[bool]] = []
    check_names: list[str] = []
    all_true: list[bool] = []
    for enabled, partial_func, check_name in pre_configured_checks.values():
        all_true.append(enabled)
        if enabled:
            checks.extend(partial_func)
            check_names.append(check_name)
    return (all_true, checks, check_names)


def run_all_checks(args: argparse.Namespace) -> None:
    """
    Run all internationalization (i18n) checks for the project.

    This function executes a series of checks to validate the project's
    internationalization setup, including key validation, usage checks
    and duplicate detection.

    Parameters
    ----------
    args : argparse.Namespace
        The arguments that have been passed to the CLI.

    Raises
    ------
    AssertionError
        If any of the i18n checks fail, an assertion error is raised with
        a message indicating that some checks didn't pass.

    Notes
    -----
    The checks performed include:
    - Invalid key detection
    - Non-existent key validation
    - Unused key detection
    - Non-source key detection
    - Repeated key detection
    - Repeated value detection
    - Sorted keys validation
    - Nested key detection
    - Missing key detection
    - Aria label punctuation validation
    - Alt text punctuation validation
    """

    pre_configured_checks: dict[str, tuple[bool, list[partial[bool]], str]] = {
        "config_key_formatting_active": (
            config_key_formatting_active,
            [
                partial(
                    invalid_key_formats_check_and_fix,
                    invalid_keys_by_format=invalid_keys_by_format,
                    all_checks_enabled=True,
                )
            ],
            "key-formatting",
        ),
        "config_key_naming_active": (
            config_key_naming_active,
            [
                partial(
                    invalid_key_names_check_and_fix,
                    invalid_keys_by_name=invalid_keys_by_name,
                    all_checks_enabled=True,
                    fix=args.fix,
                )
            ],
            "key-naming",
        ),
        "config_nonexistent_keys_active": (
            config_nonexistent_keys_active,
            [
                partial(
                    nonexistent_keys_check_and_fix,
                    all_used_i18n_keys=all_used_i18n_keys,
                    all_checks_enabled=True,
                )
            ],
            "nonexistent-keys",
        ),
        "config_unused_keys_active": (
            config_unused_keys_active,
            [
                partial(
                    unused_keys_check, unused_keys=unused_keys, all_checks_enabled=True
                )
            ],
            "unused-keys",
        ),
        "config_non_source_keys_active": (
            config_non_source_keys_active,
            [
                partial(
                    non_source_keys_check,
                    non_source_keys_dict=non_source_keys_dict,
                    all_checks_enabled=True,
                )
            ],
            "non-source-keys",
        ),
        "config_repeat_keys_active": (
            config_repeat_keys_active,
            [partial(repeat_keys_check, all_checks_enabled=True)],
            "repeat-keys",
        ),
        "config_repeat_values_active": (
            config_repeat_values_active,
            [
                partial(
                    repeat_values_check,
                    json_repeat_value_counts=json_repeat_value_counts,
                    repeat_value_error_report=repeat_value_error_report,
                    all_checks_enabled=True,
                )
            ],
            "repeat-values",
        ),
        "config_sorted_keys_active": (
            config_sorted_keys_active,
            [partial(sorted_keys_check_and_fix, all_checks_enabled=True, fix=args.fix)],
            "sorted-keys",
        ),
        "config_nested_files_active": (
            config_nested_files_active,
            [(partial(nested_files_check))],
            "nested-files",
        ),  # Note: This check warns the user and doesn't raise an error, so no need for all_checks_enabled.
        "config_missing_keys_active": (
            config_missing_keys_active,
            [partial(missing_keys_check_and_fix, all_checks_enabled=True)],
            "missing-keys",
        ),  # We don't allow fix in all checks mode.
        "config_aria_labels_active": (
            config_aria_labels_active,
            [partial(aria_labels_check_and_fix, all_checks_enabled=True, fix=args.fix)],
            "aria-labels",
        ),
        "config_alt_texts_active": (
            config_alt_texts_active,
            [partial(alt_texts_check_and_fix, all_checks_enabled=True, fix=args.fix)],
            "alt-texts",
        ),
    }
    all_true, checks, check_names = fill_partial_checks(pre_configured_checks)

    if Path(".i18n-check.yaml").is_file():
        config_file_name = ".i18n-check.yaml"

    else:
        config_file_name = ".i18n-check.yml"

    if not all(all_true):
        rprint(
            f"[yellow]⚠️  Note: Some checks are not enabled in the {config_file_name} configuration file and will be skipped.[/yellow]"
        )

    check_results: list[bool] = []
    with ProcessPoolExecutor() as executor:
        # Create a future for each check.
        futures = {
            executor.submit(checks[i]): check_names[i] for i in range(len(checks))
        }

        for future in as_completed(futures):
            try:
                result = future.result()
                check_results.append(result)

            except ValueError:
                check_results.append(False)

    if not all(check_results):
        rprint(
            "\n[red]❌ i18n-check error: Some i18n checks did not pass. Please see the error messages above.[/red]"
        )
        rprint(
            "[yellow]💡 Tip: You can bypass these checks within Git commit hooks by adding `--no-verify` to your commit command.[/yellow]"
        )
        sys.exit(1)

    rprint("\n[green]✅ Success: All i18n checks have passed![/green]")
