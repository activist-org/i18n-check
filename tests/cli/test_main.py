# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI main functionality.
"""

import unittest
from io import StringIO
from unittest.mock import patch

from i18n_check.cli.main import main
from i18n_check.utils import read_json_file, replace_text_in_file

from ..test_utils import (
    fail_checks_src_json_path,
    fail_checks_sub_dir_first_file_path,
    fail_checks_sub_dir_second_file_path,
    fail_checks_test_file_path,
)


class TestCliMain(unittest.TestCase):
    """
    Test suite for the main CLI entry point of i18n-check.
    """

    # Patch the print_help method within the correct module.
    @patch("i18n_check.cli.main.argparse.ArgumentParser.print_help")
    def test_main_no_args(self, mock_print_help):
        """
        Test that `print_help` is called when no arguments are provided.
        """
        with patch("sys.argv", ["i18n-check"]):
            main()

        mock_print_help.assert_called_once()

    @patch("i18n_check.cli.main.upgrade_cli")
    def test_main_upgrade(self, mock_upgrade_cli):
        """
        Test that `upgrade_cli` is called with the --upgrade flag.
        """
        with patch("sys.argv", ["i18n-check", "--upgrade"]):
            main()

        mock_upgrade_cli.assert_called_once()

    @patch("i18n_check.cli.main.generate_config_file")
    def test_main_generate_config_file(self, mock_generate_config_file):
        """
        Test that `generate_config_file` is called with the --generate-config-file flag.
        """
        with patch("sys.argv", ["i18n-check", "--generate-config-file"]):
            main()

        mock_generate_config_file.assert_called_once()

    @patch("i18n_check.cli.main.generate_test_frontends")
    def test_main_generate_test_frontends(self, mock_generate_test_frontends):
        """
        Test that `generate_test_frontends` is called with the --generate-test-frontends flag.
        """
        with patch("sys.argv", ["i18n-check", "--generate-test-frontends"]):
            main()

        mock_generate_test_frontends.assert_called_once()

    @patch("i18n_check.check.all_checks.run_all_checks")
    @patch("sys.exit")
    def test_main_all_checks(self, mock_all_checks, mock_sys_exit):
        """
        Test that `run_all_checks` is called for the --all flag.
        """
        with patch("sys.argv", ["i18n-check", "--all-checks"]):
            main()

        mock_all_checks.assert_called_once()

    @patch("i18n_check.check.key_formatting.invalid_key_formats_check_and_fix")
    @patch("sys.exit")
    def test_main_key_formatting(self, mock_invalid_key_formats_check, mock_sys_exit):
        """
        Test that `invalid_key_formats_check_and_fix` is called for the --key-formatting flag.
        """
        with patch("sys.argv", ["i18n-check", "--key-formatting"]):
            main()

        mock_invalid_key_formats_check.assert_called_once()

    @patch("i18n_check.check.key_naming.invalid_key_names_check_and_fix")
    @patch("sys.exit")
    def test_main_key_naming_with_fix(
        self, mock_invalid_key_names_check_and_fix, mock_sys_exit
    ):
        """
        Test that `invalid_key_names_check_and_fix` is called with fix=True for --key-naming and --fix.
        """
        with patch("sys.argv", ["i18n-check", "--key-naming", "--fix"]):
            main()

        mock_invalid_key_names_check_and_fix.assert_called_once()

        fail_checks_src_json = read_json_file(file_path=fail_checks_src_json_path)

        assert fail_checks_src_json.get("i18n.test_file.content_reference")
        assert fail_checks_src_json.get("i18n.test_file.repeat_value_single_file")
        assert fail_checks_src_json.get(
            "i18n.sub_dir._global.repeat_value_multiple_files"
        )

        # Return to old state before string replacement in tests:
        replace_text_in_file(
            path=fail_checks_src_json_path,
            old="i18n.test_file.content_reference",
            new="i18n.wrong_identifier_path.content_reference",
        )
        replace_text_in_file(
            path=fail_checks_test_file_path,
            old="i18n.test_file.content_reference",
            new="i18n.wrong_identifier_path.content_reference",
        )

        # Repeat value keys as well:
        replace_text_in_file(
            path=fail_checks_src_json_path,
            old="i18n.sub_dir._global.repeat_value_multiple_files",
            new="i18n.repeat_value_multiple_files",
        )
        replace_text_in_file(
            path=fail_checks_src_json_path,
            old="i18n.test_file.repeat_value_single_file",
            new="i18n.repeat_value_single_file",
        )

        replace_text_in_file(
            path=fail_checks_test_file_path,
            old="i18n.sub_dir._global.repeat_value_multiple_files",
            new="i18n.repeat_value_multiple_files",
        )
        replace_text_in_file(
            path=fail_checks_sub_dir_first_file_path,
            old="i18n.sub_dir._global.repeat_value_multiple_files",
            new="i18n.repeat_value_multiple_files",
        )
        replace_text_in_file(
            path=fail_checks_sub_dir_second_file_path,
            old="i18n.sub_dir._global.repeat_value_multiple_files",
            new="i18n.repeat_value_multiple_files",
        )

        replace_text_in_file(
            path=fail_checks_test_file_path,
            old="i18n.test_file.repeat_value_single_file",
            new="i18n.repeat_value_single_file",
        )

    @patch("i18n_check.check.nonexistent_keys.nonexistent_keys_check_and_fix")
    @patch("sys.exit")
    def test_main_nonexistent_keys(
        self, mock_nonexistent_keys_check_and_fix, mock_sys_exit
    ):
        """
        Test that `nonexistent_keys_check_and_fix` is called for the --nonexistent-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--nonexistent-keys"]):
            main()

        mock_nonexistent_keys_check_and_fix.assert_called_once()

    @patch("i18n_check.check.unused_keys.unused_keys_check")
    @patch("sys.exit")
    def test_main_unused_keys(self, mock_unused_keys_check, mock_sys_exit):
        """
        Test that `unused_keys_check` is called for the --unused-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--unused-keys"]):
            main()

        mock_unused_keys_check.assert_called_once()

    @patch("i18n_check.check.non_source_keys.non_source_keys_check")
    @patch("sys.exit")
    def test_main_non_source_keys(self, mock_non_source_keys_check, mock_sys_exit):
        """
        Test that `non_source_keys_check` is called for the --non-source-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--non-source-keys"]):
            main()

        mock_non_source_keys_check.assert_called_once()

    @patch("i18n_check.check.repeat_keys.repeat_keys_check")
    @patch("sys.exit")
    def test_main_repeat_keys(self, mock_repeat_keys_check, mock_sys_exit):
        """
        Test that `repeat_keys_check` is called for the --repeat-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--repeat-keys"]):
            main()

        mock_repeat_keys_check.assert_called_once()

    @patch("i18n_check.check.repeat_values.repeat_values_check")
    @patch("sys.exit")
    def test_main_repeat_values(self, mock_repeat_values_check, mock_sys_exit):
        """
        Test that `repeat_values_check` is called for the --repeat-values flag.
        """
        with patch("sys.argv", ["i18n-check", "--repeat-values"]):
            main()

        mock_repeat_values_check.assert_called_once()

    @patch("i18n_check.cli.main.nested_files_check")
    def test_main_nested_files(self, mock_nested_files_check):
        """
        Test that `nested_files_check` is called for the --nested-files flag.
        """
        with patch("sys.argv", ["i18n-check", "--nested-files"]):
            main()

        mock_nested_files_check.assert_called_once()

    @patch(
        "i18n_check.cli.main.get_version_message",
        return_value="i18n-check version 1.0.0",
    )
    def test_main_version(self, mock_get_version):
        """
        Test that the version message is printed with the --version flag.
        """
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            with self.assertRaises(SystemExit):
                with patch("sys.argv", ["i18n-check", "--version"]):
                    main()

            self.assertIn("i18n-check version 1.0.0", mock_stdout.getvalue())

        mock_get_version.assert_called_once()


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
