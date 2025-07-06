# Changelog

See the [releases for i18n-check](https://github.com/activist-org/i18n-check/releases) for an up to date list of versions and their release dates.

`i18n-check` tries to follow [semantic versioning](https://semver.org/), a MAJOR.MINOR.PATCH version where increments are made of the:

- MAJOR version when we make incompatible API changes
- MINOR version when we add functionality in a backwards compatible manner
- PATCH version when we make backwards compatible bug fixes

Emojis for the following are chosen based on [gitmoji](https://gitmoji.dev/).

## [Upcoming] i18n-check 1.x

## i18n-check 1.5.1

### 🐞 Bug Fixes

- mypy errors were fixed for an invalid use of backslashes within f-strings.

## i18n-check 1.5.0

### ✨ Features

- Individual checks can now be explicitly disabled even when the global.active option in the configuration YAML is set to true, allowing for more concise configuration files ([#39](https://github.com/activist-org/i18n-check/issues/39)).
- Rich text support has been added to CLI outputs such that error messages are red and successes are green ([#36](https://github.com/activist-org/i18n-check/issues/36)).
- Emojis have been added to error and success messages to make the sections more clear.
- Check errors are now registered with `sys.exit(1)` rather than `ValueError` so that the output doesn't have the value error texts printed.
  - This makes seeing the actual check errors much easier as they're the main outputs now.
- The error messages are for checks are now standardized and list the check name at the start.

### 🐞 Bug Fixes

- All checks now raises a `sys.exit(1)` as with individual checks so that GitHub workflows, pre-commit and other systems running i18n-check will fail.
- The error messages are now combined into one message to assure that they're not mixed together with other parallel error outputs ([#44](https://github.com/activist-org/i18n-check/issues/44)).
- The pseudo code in the test frontends has been fixed so that the `all_checks_pass` frontend passes all checks.

### ✅ Tests

- Tests have been refactored to account for the new changes in this version.

## i18n-check 1.4.1

### 🐞 Bug Fixes

- Repeat values within directory paths are handled appropriately to assure that sub directory names that are within component names are not repeated in the resulting keys.

### 📝 Documentation

- Expanded the parameter and return documentation in function docstrings.

## i18n-check 1.4.0

### ✨ Features

- The upgrade command now upgrades the package via pip rather than bringing down GitHub files and installing them directly.

### 🐞 Bug Fixes

- Dependencies were updated and unpinned in production to allow the CLI to more easily be installed in other projects.

## i18n-check 1.3.3

### 🐞 Bug Fixes

- Fix to the subprocess call for running package modules and assuring that file names in run command arguments don't include `.py` ([#35](https://github.com/activist-org/i18n-check/issues/35)).

## i18n-check 1.3.2

### 🐞 Bug Fixes

- The calls to checks is now done via `python -m` and the package module path rather than the path to the file itself to make it work more effectively in other environments ([#35](https://github.com/activist-org/i18n-check/issues/35)).

## i18n-check 1.3.1

### 🐞 Bug Fixes

- The path to the configuration file uses `Path` to make the location of the file more explicit ([#35](https://github.com/activist-org/i18n-check/issues/35)).

## i18n-check 1.3.0

### 🐞 Bug Fixes

- The i18n-check source file is referred to generally in error outputs instead of using a specific localization for the source file.
- The upgrade tests were removed to avoid tar balls rewriting local development files during testing ([#34](https://github.com/activist-org/i18n-check/issues/34)).
- The path to the configuration file now no longer requires a call to `Path` to make it work more seamlessly with GitHub Actions ([#35](https://github.com/activist-org/i18n-check/issues/35)).

### ♻️ Code Refactoring

- The name of the config file path was changed to be more explicit.

## i18n-check 1.2.0

### 🐞 Bug Fixes

- The fixes for the configuration file path were finalized with the file being controlled by the generate configuration file process and loaded into the rest of the package.
- The `run_check` function now correctly derives its path based on the file and not the `src` directory.
- The way that checks were being loaded in when only the global check option was set has been fixed.
- The naming criteria of keys was fixed so that they always start with `i18n.`.

## i18n-check 1.1.0

### 🐞 Bug Fixes

- The the check for the configuration file is now within the utils file to assure that the generate configuration file workflow is ran.
- The directory that the utils file is checking is the current working directory rather than the project root.

## i18n-check 1.0.0

### ✨ Features

- Python files that were used to check i18n files and the frontend code have been moved from the [activist repo](https://github.com/activist-org/activist/) to their own codebase ([#1](https://github.com/activist-org/i18n-check/issues/1)).
  - Checks brought over include:
    - Whether key identifiers match naming standards
    - Whether the frontend includes keys that are not in the i18n source file
    - Whether the i18n source file includes keys that aren't used in the frontend
    - Whether target locale files include keys that are not in the i18n source file
    - Whether there are repeat values in the i18n source file
- A CLI has been been written to easily run the checks based on a YAML configuration file ([#4](https://github.com/activist-org/i18n-check/issues/4)).
  - All checks can be ran via the CLI both individually and together
  - The CLI can be used to upgrade itself
- The original checks were expanded with warnings for nested JSON files and that i18n keys were repeated ([#5](https://github.com/activist-org/i18n-check/issues/5), [#15](https://github.com/activist-org/i18n-check/issues/15)).
- The user can generate test frontends for easier onboarding to the project ([#23](https://github.com/activist-org/i18n-check/issues/23)).
- The config file is checked for and an interactive workflow is used to create one if it's missing ([#24](https://github.com/activist-org/i18n-check/issues/24)).
- Directories to skip and files to skip are based on a global and per-check basis for those checks that do read in frontend files ([#29](https://github.com/activist-org/i18n-check/issues/29)).
- When running all checks they are ran in parallel ([#31](https://github.com/activist-org/i18n-check/issues/31)).

### 🎨 Design

- A logo and icon have been designed for the package.

### ⚖️ Legal

- The code has been appropriately licensed and includes SPDX license identifiers in all files.
- A security file has been added to the repo to make steps clear.

### ✅ Tests

- Testing has been written for both the checks and the CLI functionalities ([#2](https://github.com/activist-org/i18n-check/issues/2), [#14](https://github.com/activist-org/i18n-check/issues/14)).
  - The testing process uses the test frontends that the user can experiment with.
- GitHub Actions based checks are used to validate file license headers, ruff based code formatting, mypy static type checking and pytest based tests on each pull request.
- pre-commit hooks are used to enforce code quality before commits during development.

### 📝 Documentation

- All onboarding documentation has been written including an extensive readme, a contributing guide and GitHub templates to help people contribute effectively.
- Read the Docs documentation has been generated for the project and can be found at [i18n-check.readthedocs.io](https://i18n-check.readthedocs.io/en/latest/) ([#21](https://github.com/activist-org/i18n-check/issues/21)).
- All docstrings for functions and classes were standardized based on numpydoc ([#19](https://github.com/activist-org/i18n-check/issues/19)).

### ♻️ Code Refactoring

- Reusable code was moved into common utility functions ([#6](https://github.com/activist-org/i18n-check/issues/6)).
