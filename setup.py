# SPDX-License-Identifier: GPL-3.0-or-later
import os

try:
    from setuptools import find_packages, setup

except ImportError:
    from distutils.core import setup

package_directory = os.path.abspath(os.path.dirname(__file__))
with open(
    os.path.join(package_directory, "README.md"), encoding="utf-8"
) as readme_file:
    long_description = readme_file.read()

with open(
    os.path.join(package_directory, "requirements.txt"), encoding="utf-8"
) as req_file:
    requirements = req_file.readlines()

on_rtd = os.environ.get("READTHEDOCS") == "True"
if on_rtd:
    requirements = []

setup_args = dict(
    name="i18n-check",
    version="1.15.2",
    package_dir={"": "src"},
    author="i18n-check developers",
    author_email="team@activist.org",
    description="Check i18n/L10n keys and values",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/activist-org/i18n-check",
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "i18n-check=i18n_check.cli.main:main",
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

if __name__ == "__main__":
    setup(**setup_args)
