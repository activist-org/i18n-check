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


class TestAriaLabels(unittest.TestCase):
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.test_data_with_issues = {
            "i18n.test.form_button_aria_label": "Click here.",
            "i18n.test.link_aria_label": "Navigate to page!",
            "i18n.test.input_aria_label": "Enter your name?",
            "i18n.test.normal_key": "This is not an aria label.",
            "i18n.test.another_aria_label": "Submit form",  # no punctuation - correct
            "i18n.test.rtl_aria_label": "انقر هنا؟",  # Arabic with question mark
        }

        self.test_data_without_issues = {
            "i18n.test.form_button_aria_label": "Click here",
            "i18n.test.link_aria_label": "Navigate to page",
            "i18n.test.input_aria_label": "Enter your name",
            "i18n.test.normal_key": "This is not an aria label.",
            "i18n.test.another_aria_label": "Submit form",
        }

    def test_find_aria_label_punctuation_issues_with_problems(self):
        """
        Test finding aria label punctuation issues.
        """
        issues = find_aria_label_punctuation_issues(self.test_data_with_issues)

        expected_issues = {
            "i18n.test.form_button_aria_label": "Click here",
            "i18n.test.link_aria_label": "Navigate to page",
            "i18n.test.input_aria_label": "Enter your name",
            "i18n.test.rtl_aria_label": "انقر هنا",
        }

        self.assertEqual(issues, expected_issues)

    def test_find_aria_label_punctuation_issues_without_problems(self):
        """
        Test finding aria label punctuation issues when there are none.
        """
        issues = find_aria_label_punctuation_issues(self.test_data_without_issues)
        self.assertEqual(issues, {})

    def test_non_aria_label_keys_ignored(self):
        """
        Test that non-aria label keys are ignored.
        """
        test_data = {
            "i18n.test.normal_key": "This has a period.",
            "i18n.test.another_key": "This has an exclamation!",
        }

        issues = find_aria_label_punctuation_issues(test_data)
        self.assertEqual(issues, {})

    def test_empty_values_handled(self):
        """
        Test that empty values are handled gracefully.
        """
        test_data = {
            "i18n.test.empty_aria_label": "",
            "i18n.test.none_aria_label": None,
        }

        issues = find_aria_label_punctuation_issues(test_data)
        self.assertEqual(issues, {})

    @patch("i18n_check.check.aria_labels.read_json_file")
    @patch("i18n_check.check.aria_labels.rprint")
    def test_report_no_issues(self, mock_rprint, mock_read_json):
        """
        Test reporting when there are no issues.
        """
        report_and_fix_aria_labels({}, fix=False)

        mock_rprint.assert_called_once_with(
            "\n[green]✅ aria_labels: All aria label keys have appropriate punctuation.[/green]\n"
        )

    @patch("i18n_check.check.aria_labels.read_json_file")
    @patch("i18n_check.check.aria_labels.rprint")
    @patch("sys.exit")
    def test_report_with_issues_no_fix(self, mock_exit, mock_rprint, mock_read_json):
        """
        Test reporting when there are issues but not fixing.
        """
        mock_read_json.return_value = self.test_data_with_issues

        issues = {"i18n.test.form_button_aria_label": "Click here"}

        report_and_fix_aria_labels(issues, fix=False)

        # Should call rprint twice - once for errors, once for tip.
        self.assertEqual(mock_rprint.call_count, 2)
        mock_exit.assert_called_once_with(1)

    def test_rtl_punctuation_detection(self):
        """
        Test that RTL punctuation is correctly detected and removed.
        """
        test_data = {
            "i18n.test.arabic_aria_label": "انقر هنا؟",  # Arabic question mark
            "i18n.test.hebrew_aria_label": "לחץ כאן?",  # Hebrew with Latin question mark
        }

        issues = find_aria_label_punctuation_issues(test_data)

        expected = {
            "i18n.test.arabic_aria_label": "انقر هنا",
            "i18n.test.hebrew_aria_label": "לחץ כאן",
        }

        self.assertEqual(issues, expected)


if __name__ == "__main__":
    unittest.main()
