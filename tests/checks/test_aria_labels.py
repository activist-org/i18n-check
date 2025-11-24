# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for aria_labels.py check functionality.
"""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from i18n_check.check.aria_labels import (
    find_aria_label_punctuation_issues,
    report_and_fix_aria_labels,
)

from ..test_utils import checks_fail_json_dir, checks_pass_json_dir


class TestAriaLabels(unittest.TestCase):
    def test_find_aria_label_punctuation_issues_with_problems(self):
        """
        Test finding aria label punctuation issues.
        """
        aria_label_issues = find_aria_label_punctuation_issues(
            i18n_directory=checks_fail_json_dir
        )

        expected_issues = {
            "i18n.test_file.form_button_aria_label": {
                str(checks_fail_json_dir / "test_i18n_src.json"): {
                    "correct_value": "Click here to submit the form",
                    "current_value": "Click here to submit the form.",
                },
                str(checks_fail_json_dir / "test_i18n_locale.json"): {
                    "correct_value": "انقر هنا لتقديم النموذج",
                    "current_value": ".انقر هنا لتقديم النموذج",
                },
            },
        }

        self.assertEqual(aria_label_issues, expected_issues)

    @patch("i18n_check.check.aria_labels.rprint")
    @patch("sys.exit")
    def test_report_with_issues_no_fix(self, mock_exit, mock_rprint):
        """
        Test reporting when there are issues but not fixing.
        """
        aria_label_issues = find_aria_label_punctuation_issues(
            i18n_directory=checks_fail_json_dir
        )

        report_and_fix_aria_labels(aria_label_issues, fix=False)

        # Should call rprint twice - once for errors, once for tip.
        self.assertEqual(mock_rprint.call_count, 2)
        mock_exit.assert_called_once_with(1)

    def test_find_aria_label_punctuation_issues_without_problems(self):
        """
        Test finding aria label punctuation issues when there are none.
        """
        aria_label_issues = find_aria_label_punctuation_issues(
            i18n_directory=checks_pass_json_dir
        )
        self.assertEqual(aria_label_issues, {})

    @patch("i18n_check.check.aria_labels.read_json_file")
    @patch("i18n_check.check.aria_labels.rprint")
    def test_report_no_issues(self, mock_rprint, mock_read_json):
        """
        Test reporting when there are no issues.
        """
        aria_label_issues = find_aria_label_punctuation_issues(
            i18n_directory=checks_pass_json_dir
        )
        report_and_fix_aria_labels(aria_label_issues, fix=False)

        mock_rprint.assert_called_once_with(
            "[green]✅ aria-labels: All aria label keys have appropriate punctuation.[/green]"
        )


if __name__ == "__main__":
    unittest.main()
