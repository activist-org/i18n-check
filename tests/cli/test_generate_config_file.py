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
    """
    Test cases for the generate_config_file script.
    """

    @patch("builtins.open", new_callable=mock_open)
    @patch(
        "i18n_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH",
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
        checks = {
            "global": {
                "active": True,
                "directories-to-skip": ["node_modules", "dist"],
                "files-to-skip": ["test.js", "setup.py"],
            },
            "non_existent_keys": {"active": False},
        }
        file_types = [".js", ".ts"]

        # FIX 2: Call write_to_file with the correct 7 arguments in the correct order.
        write_to_file(
            src_dir=src_dir,
            i18n_dir=i18n_dir,
            i18n_src_file=i18n_src_file,
            file_types_to_check=file_types,
            checks=checks,
        )

        mock_open_func.assert_called_with(Path("/fake/path/.i18n-check.yaml"), "w")
        handle = mock_open_func()
        written_content = handle.write.call_args[0][0]
        self.assertIn("src-dir: my_app/src", written_content)
        self.assertIn("i18n-dir: my_app/i18n", written_content)
        self.assertIn("i18n-src: my_app/i18n/en.json", written_content)
        self.assertIn("file-types-to-check: [.js, .ts]", written_content)
        self.assertIn("global:\n    active: True", written_content)
        self.assertIn("non_existent_keys:\n    active: False", written_content)
        self.assertIn("directories-to-skip: [node_modules, dist]", written_content)
        self.assertIn("files-to-skip: [test.js, setup.py]", written_content)

    @patch("i18n_check.cli.generate_config_file.write_to_file")
    @patch("builtins.input")
    def test_receive_data(self, mock_input, mock_write_to_file):
        """
        Tests the receive_data function simulating a user who selects specific checks.
        """
        self.maxDiff = None
        mock_input.side_effect = [
            "",  # default src_dir
            "",  # default i18n_dir
            "",  # default i18n_src_file
            "",  # default file_types
            "n",  # all checks
            "",  # global directories_to_skip
            "",  # global files_to_skip
            "y",  # invalid_keys
            "",  # invalid_keys directories_to_skip
            "",  # invalid_keys files_to_skip
            "",  # invalid_keys keys_to_ignore
            "n",  # non_existent_keys
            "",  # non_existent_keys directories_to_skip
            "",  # non_existent_keys files_to_skip
            "y",  # unused_keys
            "",  # unused_keys directories_to_skip
            "",  # unused_keys files_to_skip
            "n",  # non_source_keys
            "y",  # repeat_keys
            "n",  # repeat_values
            "y",  # nested_keys
            "y",  # missing_keys
            "",  # locales-to-check
        ]

        receive_data()

        mock_write_to_file.assert_called_once()
        # The call in receive_data() uses keyword arguments, so they appear in 'kwargs'.
        _args, kwargs = mock_write_to_file.call_args

        expected_checks = {
            "global": {
                "title": "all checks",
                "active": False,
                "directories-to-skip": ["frontend/node_modules"],
                "files-to-skip": [],
            },
            "invalid_keys": {
                "title": "invalid keys",
                "active": True,
                "directories-to-skip": [],
                "files-to-skip": [],
                "keys-to-ignore": [],
            },
            "non_existent_keys": {
                "title": "non existent keys",
                "active": False,
                "directories-to-skip": [],
                "files-to-skip": [],
            },
            "unused_keys": {
                "title": "unused keys",
                "active": True,
                "directories-to-skip": [],
                "files-to-skip": [],
            },
            "non_source_keys": {"title": "non source keys", "active": False},
            "repeat_keys": {"title": "repeat keys", "active": True},
            "repeat_values": {"title": "repeat values", "active": False},
            "nested_keys": {"title": "nested keys", "active": True},
            "missing_keys": {
                "title": "missing keys",
                "active": True,
                "locales-to-check": [],
            },
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
        """
        Test generate_config_file when the config file exists and user wants to reconfigure.
        """
        generate_config_file()
        mock_receive_data.assert_called_once()
        mock_generate_test_frontends.assert_called_once()

    @patch("pathlib.Path.is_file", return_value=True)
    @patch("builtins.input", return_value="n")
    @patch("i18n_check.cli.generate_config_file.receive_data")
    def test_generate_config_file_exists_no_reconfigure(
        self, mock_receive_data, mock_input, mock_is_file
    ):
        """
        Test generate_config_file when the config file exists and user does not want to reconfigure.
        """
        generate_config_file()
        mock_receive_data.assert_not_called()


if __name__ == "__main__":
    unittest.main()
