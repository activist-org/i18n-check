# # SPDX-License-Identifier: GPL-3.0-or-later
# """
# Tests for the CLI upgrade functionality.
# """

# import subprocess
# import unittest
# from unittest.mock import MagicMock, mock_open, patch

# from i18n_check.cli.upgrade import upgrade_cli


# class TestUpgradeCli(unittest.TestCase):
#     @patch(
#         "i18n_check.cli.upgrade.get_latest_version", return_value="i18n-check v1.1.0"
#     )
#     @patch("i18n_check.cli.upgrade.get_local_version", return_value="1.1.0")
#     @patch("builtins.print")
#     def test_already_up_to_date(
#         self, mock_print, mock_local_version, mock_latest_version
#     ):
#         upgrade_cli()
#         mock_print.assert_any_call("You already have the latest version of i18n-check.")

#     @patch(
#         "i18n_check.cli.upgrade.get_latest_version",
#         return_value="Unknown (Unable to fetch version)",
#     )
#     @patch("i18n_check.cli.upgrade.get_local_version", return_value="1.0.0")
#     @patch("builtins.print")
#     def test_unable_to_fetch_latest_version(self, mock_print, *_):
#         upgrade_cli()
#         mock_print.assert_any_call(
#             "Unable to fetch the latest version from GitHub. Please check the GitHub repository or your internet connection."
#         )

#     # Mocking the entire flow.
#     @patch("i18n_check.cli.upgrade.sys")
#     @patch("i18n_check.cli.upgrade.subprocess.check_call")
#     @patch("i18n_check.cli.upgrade.os.remove")
#     @patch("i18n_check.cli.upgrade.shutil.rmtree")
#     @patch("i18n_check.cli.upgrade.shutil.copy2")
#     @patch("i18n_check.cli.upgrade.shutil.copytree")
#     @patch("i18n_check.cli.upgrade.Path")
#     @patch("i18n_check.cli.upgrade.tarfile.open")
#     @patch("builtins.open", new_callable=mock_open)
#     @patch("i18n_check.cli.upgrade.requests.get")
#     @patch(
#         "i18n_check.cli.upgrade.get_latest_version", return_value="i18n-check v1.1.0"
#     )
#     @patch("i18n_check.cli.upgrade.get_local_version", return_value="1.0.0")
#     @patch("builtins.print")
#     def test_successful_upgrade_flow(
#         self,
#         mock_print,
#         mock_local,
#         mock_latest,
#         mock_requests_get,
#         mock_builtin_open,
#         mock_tarfile_open,
#         mock_path,
#         mock_copytree,
#         mock_copy2,
#         mock_rmtree,
#         mock_os_remove,
#         mock_subprocess,
#         mock_sys,
#     ):
#         """
#         Tests the entire successful upgrade process from start to finish.
#         """
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_response.content = b"dummy_tarball_content"
#         mock_requests_get.return_value = mock_response

#         # 2. Mock tarfile extraction.
#         mock_tar = MagicMock()
#         mock_tarfile_open.return_value.__enter__.return_value = mock_tar

#         # 3. Mock Path and file system iteration.
#         mock_extracted_dir = MagicMock()
#         mock_file_item = MagicMock()
#         mock_file_item.is_dir.return_value = False
#         mock_dir_item = MagicMock()
#         mock_dir_item.is_dir.return_value = True
#         mock_extracted_dir.iterdir.return_value = [mock_file_item, mock_dir_item]

#         path_instance_mock = MagicMock()
#         path_instance_mock.__truediv__.return_value = mock_extracted_dir
#         mock_path.return_value = path_instance_mock

#         mock_sys.executable = "/path/to/python"

#         upgrade_cli()

#         # Assert download was attempted.
#         mock_requests_get.assert_called_once_with(
#             "https://github.com/activist-org/i18n-check/archive/refs/tags/1.1.0.tar.gz"
#         )

#         mock_builtin_open.assert_called_once_with("i18n-check-1.1.0.tar.gz", "wb")
#         mock_tarfile_open.assert_called_once_with("i18n-check-1.1.0.tar.gz", "r:gz")
#         mock_tar.extractall.assert_called_once()

#         mock_copytree.assert_called_once()
#         mock_copy2.assert_called_once()

#         # Assert cleanup.
#         self.assertEqual(
#             mock_rmtree.call_count, 2, "Should remove old dirs and the temp dir"
#         )
#         mock_os_remove.assert_called_once_with("i18n-check-1.1.0.tar.gz")

#         mock_subprocess.assert_called_once_with(
#             ["/path/to/python", "-m", "pip", "install", "-e", "."]
#         )

#     # This test reuses many mocks from the success test but changes the last step.
#     @patch("i18n_check.cli.upgrade.sys")
#     @patch("i18n_check.cli.upgrade.subprocess.check_call")
#     @patch("i18n_check.cli.upgrade.os.remove")
#     @patch("i18n_check.cli.upgrade.shutil.rmtree")
#     @patch("i18n_check.cli.upgrade.shutil.copy2")
#     @patch("i18n_check.cli.upgrade.shutil.copytree")
#     @patch("i18n_check.cli.upgrade.Path")
#     @patch("i18n_check.cli.upgrade.tarfile.open")
#     @patch("builtins.open", new_callable=mock_open)
#     @patch("i18n_check.cli.upgrade.requests.get")
#     @patch(
#         "i18n_check.cli.upgrade.get_latest_version", return_value="i18n-check v1.1.0"
#     )
#     @patch("i18n_check.cli.upgrade.get_local_version", return_value="1.0.0")
#     @patch("builtins.print")
#     def test_pip_install_fails(
#         self,
#         mock_print,
#         mock_local,
#         mock_latest,
#         mock_requests_get,
#         mock_builtin_open,
#         mock_tarfile_open,
#         mock_path,
#         mock_copytree,
#         mock_copy2,
#         mock_rmtree,
#         mock_os_remove,
#         mock_subprocess,
#         mock_sys,
#     ):
#         """
#         Tests the scenario where the final pip install command fails.
#         """
#         # Mock everything to succeed up to the subprocess call.
#         mock_response = MagicMock(status_code=200, content=b"dummy")
#         mock_requests_get.return_value = mock_response
#         mock_tarfile_open.return_value.__enter__.return_value = MagicMock()
#         mock_path.return_value = MagicMock(
#             __truediv__=MagicMock(
#                 return_value=MagicMock(iterdir=MagicMock(return_value=[]))
#             )
#         )
#         mock_sys.executable = "/path/to/python"

#         error = subprocess.CalledProcessError(returncode=1, cmd="pip install -e .")
#         mock_subprocess.side_effect = error

#         upgrade_cli()

#         mock_subprocess.assert_called_once()
#         mock_print.assert_any_call(
#             f"Failed to install the local version of i18n-check with error {error}. Please try manually running 'pip install -e .'"
#         )


# if __name__ == "__main__":
#     unittest.main()
