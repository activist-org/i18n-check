# SPDX-License-Identifier: GPL-3.0-or-later
"""
Runs all i18n checks for the project.

Examples
--------
Run the following script in terminal:

>>> i18n-check -a
"""

import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

from rich import print as rprint

from i18n_check.utils import (
    config_alt_texts_active,
    config_aria_labels_active,
    config_invalid_keys_active,
    config_missing_keys_active,
    config_nested_keys_active,
    config_non_existent_keys_active,
    config_non_source_keys_active,
    config_repeat_keys_active,
    config_repeat_values_active,
    config_sorted_keys_active,
    config_unused_keys_active,
    run_check,
)

# MARK: Run All


def run_all_checks() -> None:
    """
    Run all internationalization (i18n) checks for the project.

    This function executes a series of checks to validate the project's
    internationalization setup, including key validation, usage checks
    and duplicate detection.

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
    if config_invalid_keys_active:
        checks.append("invalid_keys")

    if config_non_existent_keys_active:
        checks.append("non_existent_keys")

    if config_unused_keys_active:
        checks.append("unused_keys")

    if config_non_source_keys_active:
        checks.append("non_source_keys")

    if config_repeat_keys_active:
        checks.append("repeat_keys")

    if config_repeat_values_active:
        checks.append("repeat_values")

    if config_sorted_keys_active:
        checks.append("sorted_keys")

    if config_nested_keys_active:
        checks.append("nested_keys")

    if config_missing_keys_active:
        checks.append("missing_keys")

    if config_aria_labels_active:
        checks.append("aria_labels")

    if config_alt_texts_active:
        checks.append("alt_texts")

    if not (
        config_invalid_keys_active
        and config_non_existent_keys_active
        and config_unused_keys_active
        and config_non_source_keys_active
        and config_repeat_keys_active
        and config_repeat_values_active
        and config_sorted_keys_active
        and config_nested_keys_active
        and config_missing_keys_active
        and config_aria_labels_active
        and config_alt_texts_active
    ):
        print(
            "Note: Some checks are not enabled in the .i18n-check.yaml configuration file and will be skipped."
        )

    check_results: list[bool] = []
    with ProcessPoolExecutor() as executor:
        # Create a future for each check.
        futures = {executor.submit(run_check, c, True): c for c in checks}

        for future in as_completed(futures):
            check_name = futures[future]
            try:
                result = future.result()
                check_results.append(result)

            except Exception as exc:
                print(f"{check_name} generated an exception: {exc}")
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


# MARK: Main

if __name__ == "__main__":
    run_all_checks()
