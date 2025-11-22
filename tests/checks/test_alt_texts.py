# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for alt_texts.py check functionality.
"""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from i18n_check.check.alt_texts import (
    find_alt_text_punctuation_issues,
    report_and_fix_alt_texts,
)

from ..test_utils import checks_fail_json_dir, checks_pass_json_dir


class TestAltTexts(unittest.TestCase):
    def test_find_alt_text_punctuation_issues_with_problems(self):
        """
        Test finding alt text punctuation issues.
        """
        alt_text_issues = find_alt_text_punctuation_issues(
            i18n_directory=checks_fail_json_dir
        )

        expected_issues = {
            "i18n.test_file.fox_image_alt_text": {
                str(checks_fail_json_dir / "test_i18n_src.json"): {
                    "correct_value": "The quick brown fox jumps over the lazy dog.",
                    "current_value": "The quick brown fox jumps over the lazy dog",
                },
                str(checks_fail_json_dir / "test_i18n_locale.json"): {
                    "correct_value": ".الثعلب البني السريع يقفز فوق الكلب الكسول",
                    "current_value": "الثعلب البني السريع يقفز فوق الكلب الكسول",
                },
            },
        }

        self.maxDiff = None

        self.assertEqual(alt_text_issues, expected_issues)

    @patch("i18n_check.check.alt_texts.rprint")
    @patch("sys.exit")
    def test_report_issues_without_fix(self, mock_exit, mock_rprint):
        """
        Test reporting issues without fixing them.
        """
        alt_text_issues = find_alt_text_punctuation_issues(
            i18n_directory=checks_fail_json_dir
        )

        report_and_fix_alt_texts(alt_text_issues, fix=False)

        # Check that appropriate error messages were printed.
        self.assertEqual(mock_rprint.call_count, 2)
        mock_exit.assert_called_once_with(1)

    def test_find_alt_text_punctuation_issues_without_problems(self):
        """
        Test finding alt text punctuation issues when there are none.
        """
        alt_text_issues = find_alt_text_punctuation_issues(
            i18n_directory=checks_pass_json_dir
        )
        self.assertEqual(alt_text_issues, {})

    @patch("i18n_check.check.alt_texts.read_json_file")
    @patch("i18n_check.check.alt_texts.rprint")
    def test_report_no_issues(self, mock_rprint, mock_read_json):
        """
        Test reporting when there are no issues.
        """
        report_and_fix_alt_texts({}, fix=False)

        mock_rprint.assert_called_once_with(
            "[green]✅ alt-texts: All alt text keys have appropriate punctuation.[/green]"
        )


if __name__ == "__main__":
    unittest.main()
