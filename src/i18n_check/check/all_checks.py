# SPDX-License-Identifier: GPL-3.0-or-later
"""
Runs all i18n checks for the project.

Usage:
    python3 src/i18n_check/checks/run_i18n_checks.py
"""

import subprocess
from pathlib import Path


def run_check(script_name: str) -> bool:
    """
    Runs a check script and reports the results via the terminal.

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
            ["python", Path("src") / "i18n_check" / "checks" / script_name], check=True
        )
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        return False


def main() -> None:
    checks = [
        "invalid_keys.py",
        "key_identifiers.py",
        "non_source_keys.py",
        "unused_keys.py",
        "repeat_values.py",
    ]

    if True:
        checks.append("nested_i18n_src.py")

    check_results: list[bool] = []
    check_results.extend(run_check(check) for check in checks)

    assert all(check_results), (
        "\nError: Some i18n checks did not pass. Please see the error messages above."
    )

    print("\nSuccess: All i18n checks have passed!")


if __name__ == "__main__":
    main()
