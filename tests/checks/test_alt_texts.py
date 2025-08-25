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


class TestAltTexts(unittest.TestCase):
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.test_data_with_issues = {
            "i18n.test.image_alt_text": "A beautiful sunset over the mountains",
            "i18n.test.fox_image_alt_text": "The quick brown fox jumps over the lazy dog",
            "i18n.test.photo_alt_text": "Team photo from 2024",
            "i18n.test.normal_key": "This is not an alt text.",
            "i18n.test.another_alt_text": "Chart showing sales data.",  # already has period - correct
            "i18n.test.banner_alt_text": "Welcome banner image",
        }

        self.test_data_without_issues = {
            "i18n.test.image_alt_text": "A beautiful sunset over the mountains.",
            "i18n.test.fox_image_alt_text": "The quick brown fox jumps over the lazy dog.",
            "i18n.test.photo_alt_text": "Team photo from 2024.",
            "i18n.test.normal_key": "This is not an alt text.",
            "i18n.test.another_alt_text": "Chart showing sales data.",
        }

    def test_find_alt_text_punctuation_issues_with_problems(self):
        """
        Test finding alt text punctuation issues.
        """
        issues = find_alt_text_punctuation_issues(self.test_data_with_issues)

        expected_issues = {
            "i18n.test.image_alt_text": "A beautiful sunset over the mountains.",
            "i18n.test.fox_image_alt_text": "The quick brown fox jumps over the lazy dog.",
            "i18n.test.photo_alt_text": "Team photo from 2024.",
            "i18n.test.banner_alt_text": "Welcome banner image.",
        }

        self.assertEqual(issues, expected_issues)

    def test_find_alt_text_punctuation_issues_without_problems(self):
        """
        Test finding alt text punctuation issues when there are none.
        """
        issues = find_alt_text_punctuation_issues(self.test_data_without_issues)
        self.assertEqual(issues, {})

    def test_non_alt_text_keys_ignored(self):
        """
        Test that non-alt text keys are ignored.
        """
        test_data = {
            "i18n.test.normal_key": "This has no period",
            "i18n.test.another_key": "This has no punctuation either",
        }

        issues = find_alt_text_punctuation_issues(test_data)
        self.assertEqual(issues, {})

    def test_empty_values_handled(self):
        """
        Test that empty values are handled gracefully.
        """
        test_data = {
            "i18n.test.empty_alt_text": "",
            "i18n.test.none_alt_text": None,
        }

        issues = find_alt_text_punctuation_issues(test_data)
        self.assertEqual(issues, {})

    def test_whitespace_cleanup(self):
        """
        Test that trailing whitespace is cleaned up when adding periods.
        """
        test_data = {
            "i18n.test.spaced_alt_text": "Image description ",
        }

        issues = find_alt_text_punctuation_issues(test_data)
        expected_issues = {
            "i18n.test.spaced_alt_text": "Image description.",
        }

        self.assertEqual(issues, expected_issues)

    def test_various_punctuation_handled(self):
        """
        Test that alt texts with various punctuation are handled correctly.
        """
        test_data = {
            "i18n.test.period_alt_text": "Already has period.",
            "i18n.test.exclamation_alt_text": "Already has exclamation!",
            "i18n.test.question_alt_text": "Already has question?",
            "i18n.test.comma_alt_text": "Already has comma,",
            "i18n.test.semicolon_alt_text": "Already has semicolon;",
            "i18n.test.arabic_question_alt_text": "Arabic question؟",
            "i18n.test.no_punctuation_alt_text": "No punctuation",
        }

        issues = find_alt_text_punctuation_issues(test_data)

        # Only the text without punctuation should be flagged.
        expected_issues = {
            "i18n.test.no_punctuation_alt_text": "No punctuation.",
        }

        self.assertEqual(issues, expected_issues)

    @patch("i18n_check.check.alt_texts.read_json_file")
    @patch("i18n_check.check.alt_texts.rprint")
    def test_report_no_issues(self, mock_rprint, mock_read_json):
        """
        Test reporting when there are no issues.
        """
        report_and_fix_alt_texts({}, fix=False)

        mock_rprint.assert_called_once_with(
            "\n[green]✅ alt_texts: All alt text keys have appropriate punctuation.[/green]\n"
        )

    @patch("i18n_check.check.alt_texts.read_json_file")
    @patch("i18n_check.check.alt_texts.rprint")
    @patch("sys.exit")
    def test_report_issues_without_fix(self, mock_exit, mock_rprint, mock_read_json):
        """
        Test reporting issues without fixing them.
        """
        mock_read_json.return_value = {"i18n.test.image_alt_text": "A beautiful sunset"}

        issues = {"i18n.test.image_alt_text": "A beautiful sunset."}

        report_and_fix_alt_texts(issues, fix=False)

        # Check that appropriate error messages were printed.
        self.assertEqual(mock_rprint.call_count, 2)
        mock_exit.assert_called_once_with(1)

    @patch("i18n_check.check.alt_texts.get_all_json_files")
    @patch("i18n_check.check.alt_texts.read_json_file")
    @patch("i18n_check.check.alt_texts.replace_text_in_file")
    @patch("i18n_check.check.alt_texts.rprint")
    @patch("sys.exit")
    def test_report_and_fix_issues(
        self, mock_exit, mock_rprint, mock_replace, mock_read_json, mock_get_files
    ):
        """
        Test reporting and fixing issues.
        """
        mock_read_json.return_value = {"i18n.test.image_alt_text": "A beautiful sunset"}
        mock_get_files.return_value = ["test_file.json"]

        issues = {"i18n.test.image_alt_text": "A beautiful sunset."}

        report_and_fix_alt_texts(issues, fix=True)

        # Check that the fix was applied.
        mock_replace.assert_called_once_with(
            path="test_file.json",
            old='"i18n.test.image_alt_text": "A beautiful sunset"',
            new='"i18n.test.image_alt_text": "A beautiful sunset."',
        )
        mock_exit.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()
