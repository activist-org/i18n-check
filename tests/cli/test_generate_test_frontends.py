# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the generate_test_frontends.py script.
"""

import unittest
from pathlib import Path
from unittest.mock import call, patch

from i18n_check.cli.generate_test_frontends import generate_test_frontends
from i18n_check.utils import INTERNAL_TEST_FRONTENDS_DIR_PATH, PATH_SEPARATOR


class TestGenerateTestFrontends(unittest.TestCase):
    """
    Test cases for the generate_test_frontends function.
    """

    @patch("pathlib.Path.is_dir", return_value=False)
    @patch("shutil.copytree")
    @patch("builtins.print")
    @patch("pathlib.Path.is_file", return_value=False)
    def test_generate_when_directory_does_not_exist(
        self, mock_is_file, mock_print, mock_copytree, mock_is_dir
    ):
        """
        Tests that the test frontends are generated when the destination directory does not exist.
        """
        generate_test_frontends()

        mock_is_dir.assert_called_with()
        mock_copytree.assert_called_once_with(
            INTERNAL_TEST_FRONTENDS_DIR_PATH,
            Path("./i18n_check_test_frontends/"),
            dirs_exist_ok=True,
        )
        self.assertIn(
            call(
                f"Generating testing frontends for i18n-check in .{PATH_SEPARATOR}i18n_check_test_frontends{PATH_SEPARATOR} ..."
            ),
            mock_print.call_args_list,
        )
        self.assertIn(
            call("The frontends have been successfully generated."),
            mock_print.call_args_list,
        )
        self.assertIn(
            call(
                "Please generate one with the 'i18n-check --generate-config-file' command."
            ),
            mock_print.call_args_list,
        )

    @patch("pathlib.Path.is_dir", return_value=True)
    @patch("shutil.copytree")
    @patch("builtins.print")
    def test_generate_when_directory_exists(
        self, mock_print, mock_copytree, mock_is_dir
    ):
        """
        Tests that the test frontends are not generated when the destination directory already exists.
        """
        generate_test_frontends()

        mock_is_dir.assert_called_with()
        mock_copytree.assert_not_called()
        mock_print.assert_called_once_with(
            f"Test frontends for i18n-check already exist in .{PATH_SEPARATOR}i18n_check_test_frontends{PATH_SEPARATOR} and will not be regenerated."
        )

    @patch("pathlib.Path.is_dir", return_value=False)
    @patch("shutil.copytree")
    @patch("builtins.print")
    @patch("pathlib.Path.is_file", side_effect=[True, True])
    def test_prints_correct_message_when_yaml_exists(
        self, mock_is_file, mock_print, mock_copytree, mock_is_dir
    ):
        """
        Tests the output message when a .i18n-check.yaml file exists.
        """
        generate_test_frontends()
        mock_print.assert_any_call(
            "You can set which one to test in the .i18n-check.yaml file."
        )

    @patch("pathlib.Path.is_dir", return_value=False)
    @patch("shutil.copytree")
    @patch("builtins.print")
    @patch("pathlib.Path.is_file", side_effect=[False, True, False, True])
    def test_prints_correct_message_when_yml_exists(
        self, mock_is_file, mock_print, mock_copytree, mock_is_dir
    ):
        """
        Tests the output message when a .i18n-check.yml file exists.
        """
        generate_test_frontends()
        mock_print.assert_any_call(
            "You can set which one to test in the .i18n-check.yml file."
        )


if __name__ == "__main__":
    unittest.main()
