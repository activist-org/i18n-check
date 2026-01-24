=========
Changelog
=========

See the `releases for i18n-check <https://github.com/activist-org/i18n-check/releases>`_ for an up to date list of versions and their release dates.

``i18n-check`` tries to follow `semantic versioning <https://semver.org/>`_, a ``MAJOR.MINOR.PATCH`` version where increments are made of the:


* ``MAJOR`` version when we make incompatible API changes
* ``MINOR`` version when we add functionality in a backwards compatible manner
* ``PATCH`` version when we make backwards compatible bug fixes

Emojis for the following are chosen based on `gitmoji <https://gitmoji.dev/>`_.

i18n-check 1.18.0
-----------------

⬆️ Dependencies
~~~~~~~~~~~~~~~

* Dependency management was switched over to using `uv <https://docs.astral.sh/uv/>`_.

i18n-check 1.17.0
-----------------

⬆️ Dependencies
~~~~~~~~~~~~~~~

* Dependencies were updated given dependabot warnings.
* The minimum Python version was set to 3.12 to assure that we're only deploying versions that are allowed for dependencies.

i18n-check 1.16.2
-----------------

⬆️ Dependencies
~~~~~~~~~~~~~~~

* Dependencies were updated given dependabot warnings.

i18n-check 1.16.1
-----------------

✅ Tests
~~~~~~~~

* Tests have been updated to pass given changes to the CLI outputs.

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* The name of the i18n source file has been added to the output for those checks that relate to it.
* The ``aria-labels`` and ``alt-texts`` checks now include a more verbose error message that provides more context on the issues.

i18n-check 1.16.0
-----------------

✨ Features
~~~~~~~~~~~

* A ``keys-to-ignore`` option has been added to the ``unused-keys`` check.

✅ Tests
~~~~~~~~

* Tests have been added to check the ``keys-to-ignore`` functionality within ``unused-keys`` via the testing configuration file being modified to ignore unused keys.

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* Minor cleanup of the code was done.

i18n-check 1.15.5
-----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* Fixed a bug where the ``repeat-values`` check would fail if keys were not used in files as some projects may not be using the ``key-naming`` check (`#84 <https://github.com/activist-org/i18n-check/issues/84>`_).
* The way in which a ``repeat-values`` suggested key is derived was improved to assure that having different keys with the same value across multiple files is properly accounted for in the suggestion (`#84 <https://github.com/activist-org/i18n-check/issues/84>`_).

✅ Tests
~~~~~~~~

* Tests were improved for the ``repeat-values`` check such that a directory structure within a suggestion is also asserted.

i18n-check 1.15.4
-----------------

⬆️ Dependencies
~~~~~~~~~~~~~~~

* Updated all dependencies given Dependabot requirements and set version numbers to be non-explicit.

i18n-check 1.15.3
-----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* The error messages that direct the user to the ``i18n-check`` configuration file now react to if it's ``.i18n-check.yaml`` (the default) or ``.i18n-check.yml``.

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* Check error messages were improved for clarity.

i18n-check 1.15.2
-----------------

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* The error messages for checks were improved and reformatted.

i18n-check 1.15.1
-----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* There was a grammar error in the ``sorted-keys`` check output if there was only one unsorted file.
* The order of the ``sorted-keys`` check error message was made more sensible.

i18n-check 1.15.0
-----------------

✨ Features
~~~~~~~~~~~

* The ``invalid-keys`` check was split into ``key-naming`` and ``key-formatting`` checks (`#81 <https://github.com/activist-org/i18n-check/issues/81>`_).
* CLI outputs of check names are now kebab-case instead of snake_case for consistency with the ``--help`` functionality messages.

🐞 Bug Fixes
~~~~~~~~~~~~

* The CLI arguments were not ordered in a sensible way in the ``--help`` output and some entries were wrong.

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* All necessary changes were made to reflect the two new checks and remove ``invalid-keys``.

📝 Documentation
~~~~~~~~~~~~~~~~

* Documentation was updated to reflect the two newly separated checks and removal of ``invalid-keys``.

i18n-check 1.14.0
-----------------

✨ Features
~~~~~~~~~~~

* The CLI now sorts all required locale files if the ``sorted-keys`` check is activated when ``--fix`` options are used for the ``invalid-keys``, ``missing-keys`` and ``nonexistent-keys`` checks (`#78 <https://github.com/activist-org/i18n-check/issues/78>`_).
* The ``sorted-keys`` check only functions if the ``repeat-keys`` check has passed for the given JSON file.
    * The user is warned if there are repeated keys so these can be fixed before sorting.

🐞 Bug Fixes
~~~~~~~~~~~~

* The ``aria-labels`` and ``alt-texts`` checks now function properly for RTL and LTR languages (`#70 <https://github.com/activist-org/i18n-check/issues/70>`_).

✅ Tests
~~~~~~~~

* RTL text examples were added into the ``test_frontends/all_checks_fail`` files to assure that punctuation fixes are tested for appropriately.

i18n-check 1.13.0
-----------------

✨ Features
~~~~~~~~~~~

* The CLI can now be configured with either a ``.yaml`` or ``.yml`` file (`#75 <https://github.com/activist-org/i18n-check/issues/75>`_).
* The ``nonexistent-keys`` check now has a ``--fix`` argument that allows the user to add missing keys to the i18n source file (`#69 <https://github.com/activist-org/i18n-check/issues/69>`_).

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* The ``missing-keys`` check ``--fix`` method now calls the ``map_keys_to_files`` function only once to speed up execution.

i18n-check 1.12.0
-----------------

✨ Features
~~~~~~~~~~~

* ``i18n-check --all --fix`` (``i18n-check -a -f``) can be ran to fix all checks that do not require user input.
    * The user is warned if there are failing checks that require user input to fix or don't have a fix option.
* The results of the ``collect_files_to_check`` and ``get_all_json_files`` utility functions have been cached using ``@lru_cache`` on private functions that are called within them (`#72 <https://github.com/activist-org/i18n-check/issues/72>`_).

🐞 Bug Fixes
~~~~~~~~~~~~

* Removed ``run_check`` from the codebase as certain operating systems are not able to set their ``__name__`` variable appropriately to run Python files as scripts via the CLI (`#68 <https://github.com/activist-org/i18n-check/issues/68>`_).
    * All checks are now ran as functions rather than as scripts.
* All configuration paths are loaded and appended to the current working directory to assure accurate path derivations (`#68 <https://github.com/activist-org/i18n-check/issues/68>`_).
    * Path separators are also normalized across operating systems.
* The path for generated configuration files is now set to the current working directory instead of relative to the configuration generation file.

✅ Tests
~~~~~~~~

* Tests were refactored to account for the changes to the codebase above.

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* ``file_types`` was renamed ``file_types_to_check`` in all instances to make its usage more clear and for standardization.
* Instances of ``non_existent`` and ``non-existent`` we changed to ``nonexistent`` given the proper spelling of the word.
* The ``nested-keys`` check was changed to ``nested-files`` to not conflict with ``nonexistent-keys``.

⬆️ Dependencies
~~~~~~~~~~~~~~~

* Python `packaging <https://github.com/pypa/packaging>`_ was added into the dependencies.
* Development and production dependencies were upgraded.

i18n-check 1.11.0
-----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* The manner in which paths to be skipped are derived has been switched from strings to ``pathlib.Path`` objects to assurer that it works across operating systems (`#68 <https://github.com/activist-org/i18n-check/issues/68>`_).

✅ Tests
~~~~~~~~

* The CI workflow was split into one that's focussed on linting and formatting and another that runs ``pytest`` based tests.
* ``pytest`` tests are now checked against Linux, macOS and Windows.
* Tests were refactored where needed to account for the new ways of deriving paths to skipped directories and files as well as to assure that they work across operating systems.

📝 Documentation
~~~~~~~~~~~~~~~~

* Testing shields in main doc pages were split based on new CI tests for multiple operating systems.

i18n-check 1.10.1
-----------------

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* The error messages of the sorted keys check have been reformatted.

📝 Documentation
~~~~~~~~~~~~~~~~

* The sorting technique of the sorted keys check that puts periods before underscores was noted.

i18n-check 1.10.0
-----------------

✨ Features
~~~~~~~~~~~

* The check and ``--fix`` options for aria label and alt text checks now works for all i18n files including locales, not just the ``i18n-src`` file.

🐞 Bug Fixes
~~~~~~~~~~~~

* A formatting error in the tip to use ``--fix`` in the sorted keys check was fixed.

✅ Tests
~~~~~~~~

* Tests were refactored to use the test frontend directories more and share variables via the ``test_utils.py`` file.
* Tests of the aria label and alt text checks were rewritten to account for the new functionalities.

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* Various code improvements to assure that files are sharing variables and that arguments are named appropriately.

i18n-check 1.9.0
----------------

✨ Features
~~~~~~~~~~~

* A new missing keys check has been added to validate if any of the locale JSON files are missing keys that are present in the source file (`#38 <https://github.com/activist-org/i18n-check/issues/38>`_).
    * The ``--fix`` argument for this check uses an interactive mode to add translations that the user enters into the terminal into a locale file of choice (`#41 <https://github.com/activist-org/i18n-check/issues/41>`_).
* A new sorted keys check has been added to make sure that the i18n JSON files are alphabetical (`#40 <https://github.com/activist-org/i18n-check/issues/40>`_).
    * The ``--fix`` argument sorts the i18n JSON files for the user.
* A new aria label check has been added to make sure that i18n keys that end in ``_aria_label`` dom't have values that end in punctuation (`#48 <https://github.com/activist-org/i18n-check/issues/48>`_).
    * The ``--fix`` argument removes all punctuation in these values.
* A new alt text check has been added to make sure that i18n keys that end in ``_alt_text`` have values that end in a period (`#49 <https://github.com/activist-org/i18n-check/issues/49>`_).
    * The ``--fix`` argument adds periods to these values.
* The user can now ignore certain regex patterns in their i18n keys within the ``invalid-keys`` check (`#52 <https://github.com/activist-org/i18n-check/issues/52>`_, `#58 <https://github.com/activist-org/i18n-check/issues/58>`_).
* In the ``invalid-keys`` check the ``--fix`` argument now uses just the global directories and files to skip to assure that all instances of keys are replaced even if their locations should not be factored into the names of the key (`#59 <https://github.com/activist-org/i18n-check/issues/59>`_).

🐞 Bug Fixes
~~~~~~~~~~~~

* Fixed an issue where the repeat values check was providing a suggestion for the new key that was sometimes invalid when checked against the ``invalid-keys`` check when the key was used in multiple files (`#50 <https://github.com/activist-org/i18n-check/issues/50>`_).
* Fixed a bug where repeat values with ``_lower`` at the end of their keys were not being removed from the count of repeats for value.

📝 Documentation
~~~~~~~~~~~~~~~~

* Extensive documentation was written for all new checks.

i18n-check 1.8.1
----------------

✨ Features
~~~~~~~~~~~

* The user is made aware of how to skip the i18n-check errors within Git commit hooks via the ``--no-verify`` option (`#55 <https://github.com/activist-org/i18n-check/issues/55>`_).

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* Variable names in tests were standardized.

i18n-check 1.8.0
----------------

✨ Features
~~~~~~~~~~~

* The user can now fix invalid key names via a ``--fix`` (``-f``) option on the ``invalid-keys`` check (`#37 <https://github.com/activist-org/i18n-check/issues/37>`_).

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* The ``key-identifiers`` check was renamed ``invalid-keys`` and the ``invalid-keys`` check was renamed ``non-existent-keys`` (`#53 <https://github.com/activist-org/i18n-check/issues/53>`_).

📝 Documentation
~~~~~~~~~~~~~~~~

* The docs were updated to reflect the name changes of the checks (`#53 <https://github.com/activist-org/i18n-check/issues/53>`_).

i18n-check 1.7.1
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* Assure that the CLI exits with exit code 1 on check errors when running all checks.

i18n-check 1.7.0
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* Improved CLI output for ``i18n-check -a`` (all checks) by suppressing redundant subprocess error messages while preserving actual check error details (`#45 <https://github.com/activist-org/i18n-check/issues/45>`_).

✅ Tests
~~~~~~~~

* The upgrade functionality of the CLI is now comprehensively tested.
* Added comprehensive unit tests for the ``run_check()`` function's error suppression functionality.

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* Check variable assignments were cleaned up the utility file.
* The upgrade message instructs the user to use the built in upgrade functionality.
* Enhanced ``run_check()`` utility function with optional ``suppress_errors`` parameter for cleaner CLI output.

⬆️ Dependencies
~~~~~~~~~~~~~~~

* Dependencies were updated due to detected vulnerabilities.

i18n-check 1.6.0
----------------

✨ Features
~~~~~~~~~~~

* Repeat key values are now sorted, which further helps with test determinism.
* Repeat value error messages have been expanded with more information about the values and how to fix them.

🐞 Bug Fixes
~~~~~~~~~~~~

* The repeat values check has been fixed to allow for ``_lower`` to be used in keys where the lower case version of another value should be ignored.

✅ Tests
~~~~~~~~

* Tests have been refactored to account for the new changes in this version.

i18n-check 1.5.1
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* mypy errors were fixed for an invalid use of backslashes within f-strings in check error messages.

i18n-check 1.5.0
----------------

✨ Features
~~~~~~~~~~~

* Individual checks can now be explicitly disabled even when the global.active option in the configuration YAML is set to true, allowing for more concise configuration files (`#39 <https://github.com/activist-org/i18n-check/issues/39>`_).
* Rich text support has been added to CLI outputs such that error messages are red and successes are green (`#36 <https://github.com/activist-org/i18n-check/issues/36>`_).
* Emojis have been added to error and success messages to make the sections more clear.
* Check errors are now registered with ``sys.exit(1)`` rather than ``ValueError`` so that the output doesn't have the value error texts printed.
    * This makes seeing the actual check errors much easier as they're the main outputs now.
* The error messages are for checks are now standardized and list the check name at the start.

🐞 Bug Fixes
~~~~~~~~~~~~

* All checks now raises a ``sys.exit(1)`` as with individual checks so that GitHub workflows, pre-commit and other systems running ``i18n-check`` will fail.
* The error messages are now combined into one message to assure that they're not mixed together with other parallel error outputs (`#44 <https://github.com/activist-org/i18n-check/issues/44>`_).
* The pseudo code in the test frontends has been fixed so that the ``all_checks_pass`` frontend passes all checks.

✅ Tests
~~~~~~~~

* Tests have been refactored to account for the new changes in this version.

i18n-check 1.4.1
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* Repeat values within directory paths are handled appropriately to assure that sub directory names that are within component names are not repeated in the resulting keys.

📝 Documentation
~~~~~~~~~~~~~~~~

* Expanded the parameter and return documentation in function docstrings.

i18n-check 1.4.0
----------------

✨ Features
~~~~~~~~~~~

* The upgrade command now upgrades the package via pip rather than bringing down GitHub files and installing them directly.

🐞 Bug Fixes
~~~~~~~~~~~~

* Dependencies were updated and unpinned in production to allow the CLI to more easily be installed in other projects.

i18n-check 1.3.3
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* Fix to the subprocess call for running package modules and assuring that file names in run command arguments don't include ``.py`` (`#35 <https://github.com/activist-org/i18n-check/issues/35>`_).

i18n-check 1.3.2
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* The calls to checks is now done via ``python -m`` and the package module path rather than the path to the file itself to make it work more effectively in other environments (`#35 <https://github.com/activist-org/i18n-check/issues/35>`_).

i18n-check 1.3.1
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* The path to the configuration file uses ``Path`` to make the location of the file more explicit (`#35 <https://github.com/activist-org/i18n-check/issues/35>`_).

i18n-check 1.3.0
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* The ``i18n-check`` source file is referred to generally in error outputs instead of using a specific localization for the source file.
* The upgrade tests were removed to avoid tar balls rewriting local development files during testing (`#34 <https://github.com/activist-org/i18n-check/issues/34>`_).
* The path to the configuration file now no longer requires a call to ``Path`` to make it work more seamlessly with GitHub Actions (`#35 <https://github.com/activist-org/i18n-check/issues/35>`_).

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* The name of the config file path was changed to be more explicit.

i18n-check 1.2.0
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* The fixes for the configuration file path were finalized with the file being controlled by the generate configuration file process and loaded into the rest of the package.
* The ``run_check`` function now correctly derives its path based on the file and not the ``src`` directory.
* The way that checks were being loaded in when only the global check option was set has been fixed.
* The naming criteria of keys was fixed so that they always start with ``i18n.``.

i18n-check 1.1.0
----------------

🐞 Bug Fixes
~~~~~~~~~~~~

* The check for the configuration file is now within the utils file to assure that the generate configuration file workflow is ran.
* The directory that the utils file is checking is the current working directory rather than the project root.

i18n-check 1.0.0
----------------

✨ Features
~~~~~~~~~~~

* Python files that were used to check i18n files and the frontend code have been moved from the `activist repo <https://github.com/activist-org/activist/>`_ to their own codebase (`#1 <https://github.com/activist-org/i18n-check/issues/1>`_).
    * Checks brought over include:
        * Whether key identifiers match naming standards
        * Whether the frontend includes keys that are not in the i18n source file
        * Whether the i18n source file includes keys that aren't used in the frontend
        * Whether target locale files include keys that are not in the i18n source file
        * Whether there are repeat values in the i18n source file
* A CLI has been been written to easily run the checks based on a YAML configuration file (`#4 <https://github.com/activist-org/i18n-check/issues/4>`_).
    * All checks can be ran via the CLI both individually and together
    * The CLI can be used to upgrade itself
* The original checks were expanded with warnings for nested JSON files and that i18n keys were repeated (`#5 <https://github.com/activist-org/i18n-check/issues/5>`_, `#15 <https://github.com/activist-org/i18n-check/issues/15>`_).
* The user can generate test frontends for easier onboarding to the project (`#23 <https://github.com/activist-org/i18n-check/issues/23>`_).
* The config file is checked for and an interactive workflow is used to create one if it's missing (`#24 <https://github.com/activist-org/i18n-check/issues/24>`_).
* Directories to skip and files to skip are based on a global and per-check basis for those checks that do read in frontend files (`#29 <https://github.com/activist-org/i18n-check/issues/29>`_).
* When running all checks they are ran in parallel (`#31 <https://github.com/activist-org/i18n-check/issues/31>`_).

🎨 Design
~~~~~~~~~

* A logo and icon have been designed for the package.

⚖️ Legal
~~~~~~~~

* The code has been appropriately licensed and includes SPDX license identifiers in all files.
* A security file has been added to the repo to make steps clear.

✅ Tests
~~~~~~~~

* Testing has been written for both the checks and the CLI functionalities (`#2 <https://github.com/activist-org/i18n-check/issues/2>`_, `#14 <https://github.com/activist-org/i18n-check/issues/14>`_).
    * The testing process uses the test frontends that the user can experiment with.
* GitHub Actions based checks are used to validate file license headers, ruff based code formatting, mypy static type checking and pytest based tests on each pull request.
* pre-commit hooks are used to enforce code quality before commits during development.

📝 Documentation
~~~~~~~~~~~~~~~~

* All onboarding documentation has been written including an extensive readme, a contributing guide and GitHub templates to help people contribute effectively.
* Read the Docs documentation has been generated for the project and can be found at `i18n-check.readthedocs.io <https://i18n-check.readthedocs.io/en/latest/>`_ (`#21 <https://github.com/activist-org/i18n-check/issues/21>`_).
* All docstrings for functions and classes were standardized based on numpydoc (`#19 <https://github.com/activist-org/i18n-check/issues/19>`_).

♻️ Code Refactoring
~~~~~~~~~~~~~~~~~~~

* Reusable code was moved into common utility functions (`#6 <https://github.com/activist-org/i18n-check/issues/6>`_).
