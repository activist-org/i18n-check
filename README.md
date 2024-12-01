<div align="center">
  <a href="https://github.com/activist-org/i18n-check-action"><img src="https://raw.githubusercontent.com/activist-org/i18n-check-action/main/.github/resources/i18nCheckGitHubBanner.png" width=1024 alt="i18n check logo"></a>
</div>

[![issues](https://img.shields.io/github/issues/activist-org/i18n-check-action?label=%20&logo=github)](https://github.com/activist-org/i18n-check-action/issues)
[![python](https://img.shields.io/badge/Python-4B8BBE.svg?logo=python&logoColor=ffffff)](https://github.com/activist-org/i18n-check-action/blob/main/CONTRIBUTING.md)
[![license](https://img.shields.io/github/license/activist-org/i18n-check-action.svg?label=%20)](https://github.com/activist-org/i18n-check-action/blob/main/LICENSE.txt)
[![coc](https://img.shields.io/badge/Contributor%20Covenant-ff69b4.svg)](https://github.com/activist-org/i18n-check-action/blob/main/.github/CODE_OF_CONDUCT.md)
[![matrix](https://img.shields.io/badge/Matrix-000000.svg?logo=matrix&logoColor=ffffff)](https://matrix.to/#/#activist_community:matrix.org)

### A GitHub action to check i18n/L10n keys and values

`i18n-check` is a GitHub action used to automate the validation of keys and values of your internationalization and localization processes.

Developed by the [activist community](https://github.com/activist-org), this action is meant to assure that development and i18n/L10n teams are in sync when using JSON based localization processes. The action can be expanded later to work for other file type processes as needed.

<a id="contents"></a>

# **Contents**

- [Conventions](#contentions)
- [How it works](#how-it-works)

<a id="conventions"></a>

# Conventions [`⇧`](#contents)

[activist](https://github.com/activist-org/activist) i18n keys follow the following conventions that are enforced by `i18n-check`:

- All key base paths should be the file path where the key is used
- If a key is used in more than one file, then the lowest common directory followed by `_global` is the base path
- Base paths should be followed by a minimally descriptive content reference
  - Only the formatting of these content references is checked via `i18n-check`
- Separate base directory paths by periods (`.`)
- Separate all directory and file name components as well as content references by underscores (`_`)
- Repeat words in file paths for organization should not be repeated in the key

> [!NOTE]
> An example valid key is:
>
> `"components.component_name.CONTENT_REFERENCE"` for a key used in `components/component/ComponentName.ext`

<a id="how-it-works"></a>

# How it works [`⇧`](#contents)

You provide `i18n-check` with the following arguments:

- `src-dir`: The path to the directory that has source code to check
- `i18n-dir`: The directory path to your i18n files
- `i18n-src`: The name of the i18n source file

From there the following checks are ran across your codebase:

- `key_identifiers`: Does the source file have keys that don't match the above format or name conventions?
- `unused_keys`: Does the source file have keys that are not used in the codebase?
- `non_source_keys`: Do the target files have keys that are not in the source file?
- `repeat_values`: Does the source file have repeat values that can be combined into a single key?

Each of the above checks is ran in parallel with directions for how to fix the i18n files being provided when errors are raised. Checks can also be disabled in the workflow via options passed in the YAML file.
