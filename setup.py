import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

package_directory = os.path.abspath(os.path.dirname(__file__))
with open(
    os.path.join(package_directory, "requirements.txt"), encoding="utf-8"
) as req_file:
    requirements = req_file.readlines()

on_rtd = os.environ.get("READTHEDOCS") == "True"
if on_rtd:
    requirements = []

setup(
    name="",
    version="0.1.0",
    package_dir={"": "src"},
    author="Andrew Tavis McAllister",
    author_email="andrew.t.mcallister@gmail.com",
    description="Check i18n/L10n keys and values",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/activist-org/i18n-check",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 1 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)

if __name__ == "__main__":
    setup(**setup_args)