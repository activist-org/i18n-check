# SPDX-License-Identifier: GPL-3.0-or-later
"""
Integration tests for .yml config file support.
"""

import tempfile
from pathlib import Path

import pytest


def test_yml_config_file_is_recognized():
    """
    Integration test: Verify that a .yml config file is recognized and used.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a .i18n-check.yml file.
        yml_config = tmp_path / ".i18n-check.yml"
        yml_config.write_text(
            """# Test configuration
            src-dir: frontend
            i18n-dir: frontend/i18n
            i18n-src: frontend/i18n/en.json

            file-types-to-check: [.ts, .js]

            checks:
            global:
                active: true
            """,
            encoding="utf-8",
        )

        # Mock CWD_PATH to use tmp_path.
        import unittest.mock

        with unittest.mock.patch("i18n_check.utils.CWD_PATH", tmp_path):
            from i18n_check.utils import get_config_file_path

            result = get_config_file_path()
            assert result.name == ".i18n-check.yml"
            assert result.is_file()
            assert result == yml_config


def test_yaml_preferred_over_yml():
    """
    Integration test: Verify that .yaml is preferred when both exist.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create both .yaml and .yml files.
        yaml_config = tmp_path / ".i18n-check.yaml"
        yml_config = tmp_path / ".i18n-check.yml"

        yaml_config.write_text("# YAML config", encoding="utf-8")
        yml_config.write_text("# YML config", encoding="utf-8")

        # Mock CWD_PATH to use tmp_path.
        import unittest.mock

        with unittest.mock.patch("i18n_check.utils.CWD_PATH", tmp_path):
            from i18n_check.utils import get_config_file_path

            result = get_config_file_path()
            assert result.name == ".i18n-check.yaml"
            assert result == yaml_config


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
