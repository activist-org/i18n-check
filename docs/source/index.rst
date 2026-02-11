.. _top:

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

Contents
========

- `About i18n-check`_
- `Installation`_
- `Key Conventions`_
- `How It Works`_
- `Configuration`_
- `Contributing`_

About i18n-check
================

``i18n-check`` is a Python package that automates the validation of keys and values for your internationalization and localization processes.

Developed by the `activist community <https://github.com/activist-org>`_, this package helps keep development and i18n/L10n teams in sync when using JSON-based localization processes.

Installation
============

Users
-----

You can install ``i18n-check`` using `uv <https://docs.astral.sh/uv/>`_ (recommended) or `pip <https://pypi.org/project/i18n-check/>`_.

uv
^^

(Recommended - fast, Rust-based installer)

.. code-block:: bash

   uv pip install i18n-check

pip
^^^

.. code-block:: bash

   pip install i18n-check

Development Build
-----------------

You can install the latest development build using uv, pip, or by cloning the repository.

Clone the Repository (Development Build)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   git clone https://github.com/activist-org/i18n-check.git  # or ideally your fork
   cd i18n-check

uv (Development Build)
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   uv sync --all-extras  # install all dependencies
   source .venv/bin/activate  # activate venv (macOS/Linux)
   # .venv\Scripts\activate  # activate venv (Windows)

pip (Development Build)
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python -m venv .venv  # create virtual environment
   source .venv/bin/activate  # activate venv (macOS/Linux)
   # .venv\Scripts\activate  # activate venv (Windows)
   pip install -e .

Key Conventions
===============

``i18n-check`` enforces these conventions for all keys:

- All keys must begin with ``i18n.``.
- The base path must be the file path where the key is used.
- If a key is used in more than one file, the base path must be the lowest common directory and end with ``_global``.
- Base paths must be followed by a minimally descriptive content reference (``i18n-check`` only checks content references for formatting).
- Separate base paths with periods (``.``).
- Separate directory / file name components and content references with underscores (``_``).
- Repeated words in the file path, including the file name, must not be repeated in the key.

.. note::
   Example of a valid file / key pair:

   **File:** ``components/component/ComponentName.ext``

   **Key:** ``"i18n.components.component_name.content_reference"``

How It Works
============

Commands
--------

These are some example commands:

**View Help**

.. code-block:: bash

   i18n-check -h

**Generate a Configuration File**

.. code-block:: bash

   i18n-check -gcf

**Generate Test Frontends**

.. code-block:: bash

   i18n-check -gtf

**Run All Checks**

.. code-block:: bash

   i18n-check -a

**Run a Specific Check**

.. code-block:: bash

   i18n-check -CHECK_ID

**Interactive Mode - Add Missing Keys**

.. code-block:: bash

   i18n-check -mk -f -l ENTER_ISO_2_CODE

Checks
------

When ``i18n-check`` finds errors, it provides directions for resolving them. You can also disable checks in the workflow by modifying the configuration `YAML file`_.

You can run these checks across your codebase:

+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Check                        | Command            | Resolution                             | Fix Command                            |
+==============================+====================+========================================+========================================+
| Does the source file contain | ``key-formatting`` | Format the keys in the source file to  | ``--fix`` (``-f``) to fix all          |
| keys that don't follow the   | (``kf``)           | match the conventions.                 | formatting issues automatically.       |
| required formatting rules?   |                    |                                        |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Are key names consistent     | ``key-naming``     | Rename them so i18n key usage is       | ``--fix`` (``-f``) to fix all naming   |
| with how and where they are  | (``kn``)           | consistent and their scope is          | issues automatically.                  |
| used in the codebase?        |                    | communicated in their name.            |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Does the codebase include    | ``nonexistent-     | Check their validity and resolve if    | ``--fix`` (``-f``) to interactively    |
| i18n keys that are not       | keys`` (``nk``)    | they should be added to the i18n files | add nonexistent keys.                  |
| within the source file?      |                    | or replaced.                           |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Does the source file have    | ``unused-keys``    | Remove them so the localization team   | n/a                                    |
| keys that are not used in    | (``uk``)           | isn't working on strings that aren't   |                                        |
| the codebase?                |                    | used.                                  |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Do the target locale files   | ``non-source-      | Remove them as they won't be used in   | n/a                                    |
| have keys that are not in    | keys`` (``nsk``)   | the application.                       |                                        |
| the source file?             |                    |                                        |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Do any of localization files | ``repeat-keys``    | Separate them so that the values are   | n/a                                    |
| have repeat keys?            | (``rk``)           | not mixed when they're in production.  |                                        |
|                              |                    |                                        |                                        |
|                              |                    | Note: The existence of repeat keys     |                                        |
|                              |                    | prevents keys from being sorted by the |                                        |
|                              |                    | sorted-keys check.                     |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Does the source file have    | ``repeat-values``  | Combine them so the localization team  | n/a                                    |
| repeat values that can be    | (``rv``)           | only needs to localize one of them.    |                                        |
| combined into a single key?  |                    |                                        |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Are the i18n source and      | ``sorted-keys``    | Sort them alphabetically to reduce     | ``--fix`` (``-f``) to sort the i18n    |
| target locale files sorted   | (``sk``)           | merge conflicts from the files         | files automatically.                   |
| alphabetically?              |                    | changing. Sorting is done such that    |                                        |
|                              |                    | periods come before underscores (some  | Note: The --fix option for other       |
|                              |                    | JSON extensions do otherwise).         | checks will sort the keys if this      |
|                              |                    |                                        | check is active.                       |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Do the i18n files contain    | ``nested-files``   | Flatten them to make replacing invalid | n/a                                    |
| nested JSON structures?      | (``nf``)           | keys easier with find-and-replace all. |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| Are any keys from the source | ``missing-keys``   | Add the missing keys to ensure all     | ``--fix --locale ENTER_ISO_2_CODE``    |
| file missing in the locale   | (``mk``)           | translations are complete.             | (``-f -l ENTER_ISO_2_CODE``) to        |
| files?                       |                    |                                        | interactively add missing keys.        |
|                              |                    | Keys with empty string values are      |                                        |
|                              |                    | considered missing.                    |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| For both LTR and RTL         | ``aria-labels``    | Remove the punctuation, as it          | ``--fix`` (``-f``) to remove           |
| languages, do keys that end  | (``al``)           | negatively affects screen reader       | punctuation automatically.             |
| in _aria_label end in        |                    | experience.                            |                                        |
| punctuation?                 |                    |                                        |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+
| For both LTR and RTL         | ``alt-texts``      | Add periods to the end to comply with  | ``--fix`` (``-f``) to add periods      |
| languages, are keys that end | (``at``)           | alt text guidelines.                   | automatically.                         |
| in _alt_text missing proper  |                    |                                        |                                        |
| punctuation?                 |                    |                                        |                                        |
+------------------------------+--------------------+----------------------------------------+----------------------------------------+

Example Responses
-----------------

These GIFs show the response to the command ``i18n-check -a`` when all checks fail or pass.

All Checks Fail
^^^^^^^^^^^^^^^

.. image:: https://github.com/user-attachments/assets/757a9f6f-7bde-40db-941d-c4e82855a453
   :alt: i18n_check_all_fail

All Checks Pass
^^^^^^^^^^^^^^^

.. image:: https://github.com/user-attachments/assets/c024c368-7691-4489-b8b8-a9844d386177
   :alt: i18n_check_all_pass

Configuration
=============

YAML File
---------

You can configure ``i18n-check`` using the ``.i18n-check.yaml`` (or ``.yml``) configuration file.

For an example, see the `configuration file for this repository <.i18n-check.yaml>`_ that we use in testing.

The following details the potential contents of this file:

.. note::
   When ``global.active`` is set to ``true``, all checks are enabled by default. You can then disable specific checks by setting their ``active`` value to ``false``. This allows for more concise configuration files. Example:

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

Arguments
---------

In the ``.i18n-check.yaml`` or ``.i18n-check.yml`` `configuration`_ file, provide these arguments:

- ``src-dir``: The directory path to your source code.
- ``i18n-dir``: The directory path to your i18n files.
- ``i18n-src``: The name of your i18n source file.
- ``file-types-to-check``: The file types to include in the check.

Additional Arguments
--------------------

You can find common additional arguments for using specific web frameworks here:

.. raw:: html

   <details><summary>Vue.js</summary>
   <p>

.. code-block:: yaml

   file_types_to_check: [.vue]

   checks:
     global:
       directories_to_skip: [frontend/.nuxt, frontend/.output, frontend/dist]

.. raw:: html

   </p>
   </details>

pre-commit
----------

This is an example of a `prek <https://prek.j178.dev/>`_ or `pre-commit <https://github.com/pre-commit/pre-commit>`_ hook:

.. code-block:: yaml

   - repo: local
     hooks:
       - id: run-i18n-check
         name: run i18n-check key-value checks
         files: ^src-dir/
         entry: uv run i18n-check -a
         language: python
         pass_filenames: false
         additional_dependencies:
           - i18n-check

GitHub Action
-------------

This is an example YAML file for a GitHub Action to check your ``i18n-files`` on PRs and commits:

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
             python-version: "3.12"

         - name: Install uv
           uses: astral-sh/setup-uv@v7

         - name: Install Dependencies
           run: uv sync --frozen --all-extras

         - name: Execute All i18n-check Key-Value Checks
           run: |
             uv run i18n-check -a

Contributing
============

See the `contribution guidelines <CONTRIBUTING.md>`_ before contributing. You can help by:

- 🐞 Reporting bugs.
- ✨ Working with us on new features.
- 📝 Improving the documentation.

We track work that is in progress or may be implemented in the `issues <https://github.com/activist-org/i18n-check/issues>`_ and `projects <https://github.com/activist-org/i18n-check/projects>`_.

Contact the Team
----------------

.. image:: https://raw.githubusercontent.com/activist-org/Organization/main/resources/images/logos/MatrixLogoGrey.png
   :width: 175
   :alt: Public Matrix Chat
   :align: right
   :target: https://matrix.to/#/#activist_community:matrix.org

activist uses `Matrix <https://matrix.org/>`_ for team communication. `Join us in our public chat rooms <https://matrix.to/#/#activist_community:matrix.org>`_ to share ideas, ask questions, or just say hi to the team.

We recommend using the `Element <https://element.io/>`_ client and `Element X <https://element.io/app>`_ for a mobile app.

Contributors
------------

Thanks to all our amazing `contributors <https://github.com/activist-org/i18n-check/graphs/contributors>`_! ❤️

.. image:: https://contrib.rocks/image?repo=activist-org/i18n-check
   :target: https://github.com/activist-org/i18n-check/graphs/contributors

Contents
========

.. toctree::
    :maxdepth: 2

    i18n_check/index

Development
===========

.. toctree::
    :maxdepth: 2

    notes

Project Indices
===============

* :ref:`genindex`
