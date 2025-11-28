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
    checks = []
    check_names = []

    if config_key_formatting_active:
        checks.append(
            partial(
                invalid_key_formats_check_and_fix,
                invalid_keys_by_format=invalid_keys_by_format,
                all_checks_enabled=True,
            )
        )
        check_names.append("key-formatting")

    if config_key_naming_active:
        checks.append(
            partial(
                invalid_key_names_check_and_fix,
                invalid_keys_by_name=invalid_keys_by_name,
                all_checks_enabled=True,
                fix=args.fix,
            )
        )
        check_names.append("key-naming")

    if config_nonexistent_keys_active:
        # We don't allow fix in all checks mode.
        checks.append(
            partial(
                nonexistent_keys_check_and_fix,
                all_used_i18n_keys=all_used_i18n_keys,
                all_checks_enabled=True,
            )
        )
        check_names.append("nonexistent-keys")

    if config_unused_keys_active:
        checks.append(
            partial(unused_keys_check, unused_keys=unused_keys, all_checks_enabled=True)
        )
        check_names.append("unused-keys")

    if config_non_source_keys_active:
        checks.append(
            partial(
                non_source_keys_check,
                non_source_keys_dict=non_source_keys_dict,
                all_checks_enabled=True,
            )
        )
        check_names.append("non-source-keys")

    if config_repeat_keys_active:
        checks.append(partial(repeat_keys_check, all_checks_enabled=True))
        check_names.append("repeat-keys")

    if config_repeat_values_active:
        checks.append(
            partial(
                repeat_values_check,
                json_repeat_value_counts=json_repeat_value_counts,
                repeat_value_error_report=repeat_value_error_report,
                all_checks_enabled=True,
            )
        )
        check_names.append("repeat-values")

    if config_sorted_keys_active:
        checks.append(
            partial(sorted_keys_check_and_fix, all_checks_enabled=True, fix=args.fix)
        )
        check_names.append("sorted-keys")

    if config_nested_files_active:
        # Note: This check warns the user and doesn't raise an error, so no need for all_checks_enabled.
        checks.append(partial(nested_files_check))
        check_names.append("nested-files")

    if config_missing_keys_active:
        # We don't allow fix in all checks mode.
        checks.append(partial(missing_keys_check_and_fix, all_checks_enabled=True))
        check_names.append("missing-keys")

    if config_aria_labels_active:
        checks.append(
            partial(aria_labels_check_and_fix, all_checks_enabled=True, fix=args.fix)
        )
        check_names.append("aria-labels")

    if config_alt_texts_active:
        checks.append(
            partial(alt_texts_check_and_fix, all_checks_enabled=True, fix=args.fix)
        )
        check_names.append("alt-texts")

    if Path(".i18n-check.yaml").is_file():
        config_file_name = ".i18n-check.yaml"

    else:
        config_file_name = ".i18n-check.yml"

    if not (
        config_key_formatting_active
        and config_key_naming_active
        and config_nonexistent_keys_active
        and config_unused_keys_active
        and config_non_source_keys_active
        and config_repeat_keys_active
        and config_repeat_values_active
        and config_sorted_keys_active
        and config_nested_files_active
        and config_missing_keys_active
        and config_aria_labels_active
        and config_alt_texts_active
    ):
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
