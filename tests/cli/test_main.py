# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI main functionality.
"""

import unittest
from io import StringIO
from unittest.mock import patch

from i18n_check.cli.main import main


class TestMainCli(unittest.TestCase):
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

    @patch("i18n_check.cli.main.run_check")
    def test_main_all_checks(self, mock_run_check):
        """
        Test that `run_check` is called for the --all-checks flag.
        """
        with patch("sys.argv", ["i18n-check", "--all-checks"]):
            main()
        mock_run_check.assert_called_once_with("all_checks")

    @patch("i18n_check.cli.main.run_check")
    def test_main_invalid_keys(self, mock_run_check):
        """
        Test that `run_check` is called for the --invalid-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--invalid-keys"]):
            main()
        mock_run_check.assert_called_once_with("invalid_keys")

    @patch("i18n_check.cli.main.invalid_keys_check_and_fix")
    def test_main_invalid_keys_with_fix(self, mock_invalid_keys_check_and_fix):
        """
        Test that `invalid_keys_check_and_fix` is called with fix=True for --invalid-keys and --fix.
        """
        with patch("sys.argv", ["i18n-check", "--invalid-keys", "--fix"]):
            main()
        mock_invalid_keys_check_and_fix.assert_called_once()
        args, kwargs = mock_invalid_keys_check_and_fix.call_args
        assert kwargs.get("fix") is True

    @patch("i18n_check.cli.main.run_check")
    def test_main_nonexistent_keys(self, mock_run_check):
        """
        Test that `run_check` is called for the --nonexistent-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--nonexistent-keys"]):
            main()
        mock_run_check.assert_called_once_with("nonexistent_keys")

    @patch("i18n_check.cli.main.run_check")
    def test_main_unused_keys(self, mock_run_check):
        """
        Test that `run_check` is called for the --unused-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--unused-keys"]):
            main()
        mock_run_check.assert_called_once_with("unused_keys")

    @patch("i18n_check.cli.main.run_check")
    def test_main_non_source_keys(self, mock_run_check):
        """
        Test that `run_check` is called for the --non-source-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--non-source-keys"]):
            main()
        mock_run_check.assert_called_once_with("non_source_keys")

    @patch("i18n_check.cli.main.run_check")
    def test_main_repeat_keys(self, mock_run_check):
        """
        Test that `run_check` is called for the --repeat-keys flag.
        """
        with patch("sys.argv", ["i18n-check", "--repeat-keys"]):
            main()
        mock_run_check.assert_called_once_with("repeat_keys")

    @patch("i18n_check.cli.main.run_check")
    def test_main_repeat_values(self, mock_run_check):
        """
        Test that `run_check` is called for the --repeat-values flag.
        """
        with patch("sys.argv", ["i18n-check", "--repeat-values"]):
            main()
        mock_run_check.assert_called_once_with("repeat_values")

    @patch("i18n_check.cli.main.run_check")
    def test_main_nested_files(self, mock_run_check):
        """
        Test that `run_check` is called for the --nested-files flag.
        """
        with patch("sys.argv", ["i18n-check", "--nested-files"]):
            main()
        mock_run_check.assert_called_once_with("nested_files")

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
