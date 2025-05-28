# SPDX-License-Identifier: GPL-3.0-or-later
"""
Runs all i18n checks for the project.

Examples
--------
Run the following script in terminal:

>>> python3 src/i18n_check/checks/run_i18n_checks.py
"""

from i18n_check.utils import run_check

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
    - Key identifier validation
    - Non-source key detection
    - Unused key detection
    - Repeated key detection
    - Repeated value detection
    - Nested key detection
    """
    checks = [
        "invalid_keys.py",
        "key_identifiers.py",
        "non_source_keys.py",
        "unused_keys.py",
        "repeat_keys.py",
        "repeat_values.py",
        "nested_keys.py",
    ]

    check_results: list[bool] = []
    check_results.extend(run_check(check) for check in checks)

    assert all(check_results), (
        "\nError: Some i18n checks did not pass. Please see the error messages above."
    )

    print("\nSuccess: All i18n checks have passed!")


# MARK: Main

if __name__ == "__main__":
    run_all_checks()
