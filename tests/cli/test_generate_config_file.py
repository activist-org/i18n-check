# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI config file generation functionality.
"""

import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from i18n_check.cli.generate_config_file import (
    generate_config_file,
    receive_data,
    write_to_file,
)


class TestGenerateConfigFile(unittest.TestCase):
    """Test cases for the generate_config_file script."""

    @patch("builtins.open", new_callable=mock_open)
    @patch(
        "i18n_check.cli.generate_config_file.YAML_FILE_PATH",
        Path("/fake/path/.i18n-check.yaml"),
    )
    def test_write_to_file_all_options(self, mock_open_func):
        """
        Tests the write_to_file function to ensure it formats the output string correctly
        when all parameters are provided.
        """
        src_dir = "my_app/src"
        i18n_dir = "my_app/i18n"
        i18n_src_file = "my_app/i18n/en.json"
        checks = {"global": True, "invalid_keys": False}
        file_types = [".js", ".ts"]
        dirs_to_skip = ["node_modules"]
        files_to_skip = ["test.js"]

        write_to_file(
            src_dir,
            i18n_dir,
            i18n_src_file,
            checks,
            file_types,
            dirs_to_skip,
            files_to_skip,
        )

        # Check that the file was opened in write mode.
        mock_open_func.assert_called_once_with(Path("/fake/path/.i18n-check.yaml"), "w")

        # Get the file handle from the mock.
        file_handle = mock_open_func()

        # Get all the writes that were made to the file.
        all_writes = "".join(call.args[0] for call in file_handle.write.call_args_list)
        # Check that the content written is what we expect.
        self.assertIn("src-dir: my_app/src", all_writes)
        self.assertIn("i18n-dir: my_app/i18n", all_writes)
        self.assertIn("i18n-src: my_app/i18n/en.json", all_writes)
        self.assertIn("global:\n    active: True", all_writes)
        self.assertIn("invalid_keys:\n    active: False", all_writes)
        self.assertIn("file-types-to-check: [.js, .ts]", all_writes)
        self.assertIn("directories-to-skip: [node_modules]", all_writes)
        self.assertIn("files-to-skip: [['test.js']]", all_writes)

    @patch("i18n_check.cli.generate_config_file.write_to_file")
    @patch("builtins.input")
    def test_receive_data(self, mock_input, mock_write_to_file):
        """
        Tests the receive_data function simulating a user who selects specific checks.
        """
        mock_input.side_effect = [
            "",  # Default src_dir
            "",  # Default i18n_dir
            "",  # Default i18n_src_file
            "",  # Default file_types
            "",  # Default dirs_to_skip
            "",  # Default files_to_skip
            "n",  # All checks
            "y",  # invalid_keys
            "n",  # key_identifiers
            "y",  # nested_keys
            "n",  # non_source_keys
            "y",  # repeat_keys
            "n",  # repeat_values
            "y",  # unused_keys
        ]

        receive_data()

        mock_write_to_file.assert_called_once()
        args, kwargs = mock_write_to_file.call_args

        expected_checks = {
            "global": False,
            "invalid_keys": True,
            "key_identifiers": False,
            "nested_keys": True,
            "non_source_keys": False,
            "repeat_keys": True,
            "repeat_values": False,
            "unused_keys": True,
        }
        self.assertEqual(kwargs["checks"], expected_checks)

    @patch("i18n_check.cli.generate_config_file.receive_data")
    @patch("pathlib.Path.is_file", return_value=False)
    @patch("builtins.input", return_value="y")
    @patch("i18n_check.cli.generate_config_file.generate_test_frontends")
    @patch("pathlib.Path.is_dir", return_value=False)
    def test_generate_config_file_does_not_exist(
        self,
        mock_is_dir,
        mock_gen_frontends,
        mock_input,
        mock_is_file,
        mock_receive_data,
    ):
        """
        Tests that if the config file does NOT exist, the receive_data function is called.
        """
        generate_config_file()
        mock_is_file.assert_called_once()
        mock_receive_data.assert_called_once()

    @patch("pathlib.Path.is_file", return_value=True)
    @patch("builtins.input", return_value="y")
    @patch("i18n_check.cli.generate_config_file.receive_data")
    @patch("i18n_check.cli.generate_config_file.generate_test_frontends")
    def test_generate_config_file_exists_reconfigure(
        self, mock_generate_test_frontends, mock_receive_data, mock_input, mock_is_file
    ):
        """Test generate_config_file when the config file exists and user wants to reconfigure."""
        generate_config_file()
        mock_receive_data.assert_called_once()
        mock_generate_test_frontends.assert_called_once()

    @patch("pathlib.Path.is_file", return_value=True)
    @patch("builtins.input", return_value="n")
    @patch("i18n_check.cli.generate_config_file.receive_data")
    def test_generate_config_file_exists_no_reconfigure(
        self, mock_receive_data, mock_input, mock_is_file
    ):
        """Test generate_config_file when the config file exists and user does not want to reconfigure."""
        generate_config_file()
        mock_receive_data.assert_not_called()


if __name__ == "__main__":
    unittest.main()
