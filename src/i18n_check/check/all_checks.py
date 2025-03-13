# SPDX-License-Identifier: GPL-3.0-or-later
"""
Runs all i18n checks for the project.

Usage:
    python3 src/i18n_check/checks/run_i18n_checks.py
"""

from i18n_check.utils import run_check


def main() -> None:
    checks = [
        "invalid_keys.py",
        "key_identifiers.py",
        "non_source_keys.py",
        "unused_keys.py",
        "repeat_values.py",
    ]

    if True:
        checks.append("nested_keys.py")

    check_results: list[bool] = []
    check_results.extend(run_check(check) for check in checks)

    assert all(
        check_results
    ), "\nError: Some i18n checks did not pass. Please see the error messages above."

    print("\nSuccess: All i18n checks have passed!")


if __name__ == "__main__":
    main()
