.. image:: https://raw.githubusercontent.com/activist-org/i18n-check/main/.github/resources/images/i18nCheckGitHubBanner.png
    :width: 100%
    :align: center
    :target: https://github.com/activist-org/i18n-check

|rtd| |pr_ci| |python_package_ci| |issues| |python| |pypi| |pypistatus| |license| |coc| |matrix|

.. |rtd| image:: https://img.shields.io/readthedocs/i18n-check.svg?label=%20&logo=read-the-docs&logoColor=ffffff
    :target: http://i18n-check.readthedocs.io/en/latest/

.. |pr_ci| image:: https://img.shields.io/github/actions/workflow/status/activist-org/i18n-check/pr_ci.yaml?branch=main&label=%20&logo=ruff&logoColor=ffffff
    :target: https://github.com/activist-org/i18n-check/actions/workflows/pr_ci.yaml

.. |python_package_ci| image:: https://img.shields.io/github/actions/workflow/status/activist-org/i18n-check/pr_ci.yaml?branch=main&label=%20&logo=pytest&logoColor=ffffff
    :target: https://github.com/activist-org/i18n-check/actions/workflows/python_package_ci.yaml

.. |issues| image:: https://img.shields.io/github/issues/activist-org/i18n-check?label=%20&logo=github
    :target: https://github.com/activist-org/i18n-check/issues

.. |python| image:: https://img.shields.io/badge/Python%203-306998.svg?logo=python&logoColor=ffffff
    :target: https://github.com/activist-org/i18n-check/blob/main/CONTRIBUTING.md

.. |pypi| image:: https://img.shields.io/pypi/v/i18n-check.svg?label=%20&color=4B8BBE
    :target: https://pypi.org/project/i18n-check/

.. |pypistatus| image:: https://img.shields.io/pypi/status/i18n-check.svg?label=%20
    :target: https://pypi.org/project/i18n-check/

.. |license| image:: https://img.shields.io/github/license/activist-org/i18n-check.svg?label=%20
    :target: https://github.com/activist-org/i18n-check/blob/main/LICENSE.txt

.. |coc| image:: https://img.shields.io/badge/Contributor%20Covenant-ff69b4.svg
    :target: https://github.com/activist-org/i18n-check/blob/main/.github/CODE_OF_CONDUCT.md

.. |matrix| image:: https://img.shields.io/badge/Matrix-000000.svg?logo=matrix&logoColor=ffffff
    :target: https://matrix.to/#/#activist_community:matrix.org

**Check i18n/L10n keys and values**

``i18n-check`` is a Python package to automate the validation of keys and values of your internationalization and localization processes.

Developed by the `activist community <https://github.com/activist-org/>`_, this package is meant to assure that development and i18n/L10n teams are in sync when using JSON based localization processes. The checks can be expanded later to work for other file types as needed.

Conventions
===========

`activist <https://github.com/activist-org/activist/>`_ i18n keys follow the following conventions that are enforced by `i18n-check`:

- All key base paths should be the file path where the key is used prepended with ``i18n.``
    - Starting i18n keys with a common identifier allows them to be found within checks
- If a key is used in more than one file, then the lowest common directory followed by ``_global`` is the base path
- Base paths should be followed by a minimally descriptive content reference
    - Only the formatting of these content references is checked via ``i18n-check``
- Separate base directory paths by periods (``.``)
- Separate all directory and file name components as well as content references by underscores (``_``)
- Repeat words in file paths for sub directory organization should not be repeated in the key

    | **Note**

    An example valid key is:

    File: ``components/component/ComponentName.ext``

    Key: ``"components.component_name.content_reference"``

Installation
============

``i18n-check`` is available for installation via `uv <https://docs.astral.sh/uv/>`_ or `pip <https://pypi.org/project/i18n-check/>`_:

.. code-block:: shell

    # Using uv (recommended - fast, Rust-based installer):
    uv pip install i18n-check

    # Or using pip:
    pip install i18n-check

The latest development version can further be installed via the `source code on GitHub <https://github.com/activist-org/i18n-check>`_:

.. code-block:: shell

    git clone https://github.com/activist-org/i18n-check.git
    cd i18n-check

    # With uv (recommended):
    uv sync --all-extras  # Install all dependencies
    source .venv/bin/activate  # Activate venv (macOS/Linux)
    # .venv\Scripts\activate  # Activate venv (Windows)

    # Or with pip:
    python -m venv .venv  # Create virtual environment
    source .venv/bin/activate  # Activate venv (macOS/Linux)
    # .venv\Scripts\activate  # Activate venv (Windows)
    pip install -e .

Commands
========

The following are example commands for `i18n-check`:

.. code-block:: shell

    i18n-check -h  # view the help
    i18n-check -gcf  # generate a configuration file
    i18n-check -gtf  # generate test frontends to experiment with
    i18n-check -a  # run all checks
    i18n-check -CHECK_ID  # run a specific check (see options below)

Arguments
=========

You provide ``i18n-check`` with the following arguments in the ``.i18n-check.yaml`` or ``.i18n-check.yml`` configuration file (see the configuration section below):

- ``src-dir``: The path to the directory that has source code to check
- ``i18n-dir``: The directory path to your i18n files
- ``i18n-src``: The name of the i18n source file
- ``file-types-to-check``: The file types that the checks should be ran against

Checks
======

There the following checks can ran across your codebase:

- ``key-formatting`` (``kf``): Does the i18n source file contain keys that don't follow the required formatting rules?
    - Format the keys in the source file to match the conventions.
    - Pass ``--fix`` (``-f``) to fix all formatting issues automatically.
- ``key-naming`` (``kn``): Are key names consistent with how and where they are used in the codebase?
    - Rename them so i18n key usage is consistent and their scope is communicated in their name.
    - Pass ``--fix`` (``-f``) to fix all naming issues automatically.
- ``nonexistent-keys`` (``nk``): Does the codebase include i18n keys that are not within the source file?
    - Check their validity and resolve if they should be added to the i18n files or replaced.
    - Pass ``--fix`` (``-f``) to interactively add nonexistent keys.
- ``unused-keys`` (``uk``): Does the source file have keys that are not used in the codebase?
    - Remove them so the localization team isn't working on strings that aren't used.
- ``non-source-keys`` (``nsk``): Do the target locale files have keys that are not in the source file?
    - Remove them as they won't be used in the application.
- ``repeat-keys`` (``rk``): Do any of localization files have repeat keys?
    - Separate them so that the values are not mixed when they're in production.
    - Note: The existence of repeat keys prevents keys from being sorted.
- ``repeat-values`` (``rv``): Does the source file have repeat values that can be combined into a single key?
    - Combine them so the localization team only needs to localize one of them.
- ``sorted-keys`` (``sk``): Are the i18n source and target locale files sorted alphabetically?
    - Sort them alphabetically to reduce merge conflicts from the files changing.
    - Pass ``--fix`` (``-f``) to sort the i18n files automatically.
    - Note: The ``--fix`` option for other checks will sort the keys if this check is active.
    - Note: Sorting is done such that periods come before underscores (some JSON extensions do otherwise).
- ``nested-files`` (``nf``): Do the i18n files contain nested JSON structures?
    - Flatten them to make replacing invalid keys easier with find-and-replace all.
- ``missing-keys`` (``mk``): Are any keys from the source file missing in the locale files?
    - Add the missing keys to ensure all translations are complete.
    - Keys with empty string values are also considered missing.
    - Pass ``--fix --locale ENTER_ISO_2_CODE`` (``-f -l ENTER_ISO_2_CODE``) to interactively add missing keys.
- ``aria-labels`` (``al``): Do keys that end in ``_aria_label`` end in punctuation?
    - Remove the punctuation as it negatively affects screen reader experience.
    - Pass ``--fix`` (``-f``) to remove punctuation automatically.
- ``alt-texts`` (``at``): Do keys that end in ``_alt_text`` lack proper punctuation?
    - Add periods to the end to comply with alt text guidelines.
    - Pass ``--fix`` (``-f``) to add periods automatically.

    | **Note**

    The ``aria-labels`` and ``alt-texts`` checks function for LTR and RTL languages.

Directions for how to fix the i18n files are provided when errors are raised. Checks can also be disabled in the workflow via options passed in the configuration YAML file.

Configuration
=============

The following details the ``.i18n-check.yaml`` configuration file, with a further example being the `configuration file for the i18n-check repository <https://github.com/activist-org/i18n-check/blob/main/.i18n-check.yaml>`_ that we use in testing.

    | **Note**

    Both ``.i18n-check.yaml`` and ``.i18n-check.yml`` file extensions are supported. If both files exist, ``.yaml`` will be preferred.

    | **Note**

    When ``global.active`` is set to ``true``, all checks are enabled by default. You can then explicitly disable specific checks by setting their ``active`` value to ``false``. This allows for more concise configuration files. For example:

    .. code-block:: yaml

        checks:
          global:
            active: true
          missing-keys:
            active: false # disabled even though global is active

.. code-block:: yaml

    src-dir: frontend
    i18n-dir: frontend/i18n
    i18n-src: frontend/i18n/en.json

    file-types-to-check: [.ts, .js]

    checks:
      # Global configurations are applied to all checks.
      global:
        active: true # enables all checks by default
        directories-to-skip: [frontend/node_modules]
        files-to-skip: []
      key-formatting:
        active: true # can be used to override individual checks
        keys-to-ignore: [] # regexes for ignoring keys
      key-naming:
        active: true
        directories-to-skip: []
        files-to-skip: []
        keys-to-ignore: []
      nonexistent-keys:
        active: true
        directories-to-skip: []
        files-to-skip: []
      unused-keys:
        active: true
        directories-to-skip: []
        files-to-skip: []
        keys-to-ignore: []
      non-source-keys:
        active: true
      repeat-keys:
        active: true
      repeat-values:
        active: true
      sorted-keys:
        active: true
      nested-files:
        active: true
      missing-keys:
        active: true
        locales-to-check: [] # iso codes, or leave empty to check all
      aria-labels:
        active: true
      alt-texts:
        active: true

pre-commit
==========

The following is an example `pre-commit <https://github.com/pre-commit/pre-commit>`_ hook:

.. code-block:: yaml

    - repo: local
      hooks:
        - id: run-i18n-check
        name: run i18n-check key-value checks
        files: ^src-dir/
        entry: i18n-check -a
        language: python
        pass_filenames: false
        additional_dependencies:
          - i18n-check

GitHub Action
=============

The following is an example YAML file for a GitHub Action to check your i18n files on PRs and commits:

.. code-block:: yaml

    name: pr_ci_i18n_check
    on:
      workflow_dispatch:
      pull_request:
        branches:
          - main
        types:
          - opened
          - reopened
          - synchronize
      push:
        branches:
          - main

    jobs:
      i18n_check:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout Project
            uses: actions/checkout@v4

          - name: Setup Python
            uses: actions/setup-python@v5
            with:
              python-version: "3.13"

          - name: Create Environment and Install
            run: |
              python -m pip install --upgrade uv
              uv venv
              . .venv/bin/activate
              uv pip install i18n-check

          - name: Execute All i18n-check Key-Value Checks
            run: |
              i18n-check -a

Contents
========

.. toctree::
    :maxdepth: 2

    i18n_check/index

Contributing
============

.. toctree::
    :maxdepth: 2

    notes

Project Indices
===============

* :ref:`genindex`
