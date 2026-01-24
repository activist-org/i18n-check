<div align="center">
  <a href="https://github.com/activist-org/i18n-check"><img src="https://raw.githubusercontent.com/activist-org/i18n-check/main/.github/resources/images/i18nCheckGitHubBanner.png" width=1024 alt="i18n check logo"></a>
</div>

[![rtd](https://img.shields.io/readthedocs/i18n-check.svg?label=%20&logo=read-the-docs&logoColor=ffffff)](http://i18n-check.readthedocs.io/en/latest/)
[![pr_ci](https://img.shields.io/github/actions/workflow/status/activist-org/i18n-check/pr_ci.yaml?branch=main&label=%20&logo=ruff&logoColor=ffffff)](https://github.com/activist-org/i18n-check/actions/workflows/pr_ci.yaml)
[![python_package_ci](https://img.shields.io/github/actions/workflow/status/activist-org/i18n-check/python_package_ci.yaml?branch=main&label=%20&logo=pytest&logoColor=ffffff)](https://github.com/activist-org/i18n-check/actions/workflows/python_package_ci.yaml)
[![issues](https://img.shields.io/github/issues/activist-org/i18n-check?label=%20&logo=github)](https://github.com/activist-org/i18n-check/issues)
[![python](https://img.shields.io/badge/Python-4B8BBE.svg?logo=python&logoColor=ffffff)](https://github.com/activist-org/i18n-check/blob/main/CONTRIBUTING.md)
[![pypi](https://img.shields.io/pypi/v/i18n-check.svg?label=%20&color=4B8BBE)](https://pypi.org/project/i18n-check/)
[![pypistatus](https://img.shields.io/pypi/status/i18n-check.svg?label=%20)](https://pypi.org/project/i18n-check/)
[![license](https://img.shields.io/github/license/activist-org/i18n-check.svg?label=%20)](https://github.com/activist-org/i18n-check/blob/main/LICENSE.txt)
[![coc](https://img.shields.io/badge/Contributor%20Covenant-ff69b4.svg)](https://github.com/activist-org/i18n-check/blob/main/.github/CODE_OF_CONDUCT.md)
[![matrix](https://img.shields.io/badge/Matrix-000000.svg?logo=matrix&logoColor=ffffff)](https://matrix.to/#/#activist_community:matrix.org)

### Check i18n/L10n keys and values

`i18n-check` is a Python package to automate the validation of keys and values of your internationalization and localization processes.

Developed by the [activist community](https://github.com/activist-org), this package is meant to assure that development and i18n/L10n teams are in sync when using JSON based localization processes. The checks can be expanded later to work for other file types as needed.

<a id="contents"></a>

# **Contents**

- [Conventions](#contentions-)
- [Installation](#installation-)
- [How it works](#how-it-works-)
  - [Commands](#commands-)
  - [Previews](#previews-)
  - [Arguments](#arguments-)
  - [Checks](#checks-)
- [Configuration](#configuration-)
  - [YAML File](#yaml-file-)
  - [Additional Arguments](#additional-arguments-)
  - [pre-commit](#pre-commit-)
  - [GitHub Action](#github-action-)
- [Contributing](#contributing)
- [Environment setup](#environment-setup-)
- [Contributors](#contributors-)

<a id="conventions-"></a>

# Conventions [`⇧`](#contents)

[activist](https://github.com/activist-org/activist) i18n keys follow the following conventions that are enforced by `i18n-check`:

- All key base paths should be the file path where the key is used prepended with `i18n.`
  - Starting i18n keys with a common identifier allows them to be found within checks
- If a key is used in more than one file, then the lowest common directory followed by `_global` is the base path
- Base paths should be followed by a minimally descriptive content reference
  - Only the formatting of these content references is checked via `i18n-check`
- Separate base directory paths by periods (`.`)
- Separate all directory and file name components as well as content references by underscores (`_`)
- Repeat words in file paths for sub directory organization should not be repeated in the key

> [!NOTE]
> An example valid key is:
>
> File: `components/component/ComponentName.ext`
>
> Key: `"components.component_name.content_reference"`

<a id="installation-"></a>

# Installation [`⇧`](#contents)

`i18n-check` is available for installation via [uv](https://docs.astral.sh/uv/) (recommended) or [pip](https://pypi.org/project/i18n-check/).

### For Users

```bash
# Using uv (recommended - fast, Rust-based installer):
uv pip install i18n-check

# Or using pip:
pip install i18n-check
```

### For Development Build

```bash
git clone https://github.com/activist-org/i18n-check.git  # or ideally your fork
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
```

<a id="how-it-works-"></a>

# How it works [`⇧`](#contents)

<a id="commands-"></a>

### Commands [`⇧`](#contents)

The following are example commands for `i18n-check`:

```bash
i18n-check -h  # view the help
i18n-check -gcf  # generate a configuration file
i18n-check -gtf  # generate test frontends to experiment with
i18n-check -a  # run all checks
i18n-check -CHECK_ID  # run a specific check (see options below)
i18n-check -mk -f -l ENTER_ISO_2_CODE  # interactive mode to add missing keys
```

<a id="previews-"></a>

### Previews [`⇧`](#contents)

The following GIFs show the response to the command `i18n-check -a` when all checks fail and when all checks pass:

![i18n_check_all_fail](https://github.com/user-attachments/assets/757a9f6f-7bde-40db-941d-c4e82855a453)

![i18n_check_all_pass](https://github.com/user-attachments/assets/c024c368-7691-4489-b8b8-a9844d386177)

<a id="arguments-"></a>

### Arguments [`⇧`](#contents)

You provide `i18n-check` with the following arguments in the `.i18n-check.yaml` or `.i18n-check.yml` configuration file (see [configuration](#configuration-) below):

- `src-dir`: The path to the directory that has source code to check
- `i18n-dir`: The directory path to your i18n files
- `i18n-src`: The name of the i18n source file
- `file-types-to-check`: The file types that the checks should be ran against

<a id="checks-"></a>

### Checks [`⇧`](#contents)

There the following checks can ran across your codebase:

- `key-formatting` (`kf`): Does the i18n source file contain keys that don't follow the required formatting rules?
  - Format the keys in the source file to match the conventions.
  - Pass `--fix` (`-f`) to fix all formatting issues automatically.
- `key-naming` (`kn`): Are key names consistent with how and where they are used in the codebase?
  - Rename them so i18n key usage is consistent and their scope is communicated in their name.
  - Pass `--fix` (`-f`) to fix all naming issues automatically.
- `nonexistent-keys` (`nk`): Does the codebase include i18n keys that are not within the source file?
  - Check their validity and resolve if they should be added to the i18n files or replaced.
  - Pass `--fix` (`-f`) to interactively add nonexistent keys.
- `unused-keys` (`uk`): Does the source file have keys that are not used in the codebase?
  - Remove them so the localization team isn't working on strings that aren't used.
- `non-source-keys` (`nsk`): Do the target locale files have keys that are not in the source file?
  - Remove them as they won't be used in the application.
- `repeat-keys` (`rk`): Do any of localization files have repeat keys?
  - Separate them so that the values are not mixed when they're in production.
  - Note: The existence of repeat keys prevents keys from being sorted.
- `repeat-values` (`rv`): Does the source file have repeat values that can be combined into a single key?
  - Combine them so the localization team only needs to localize one of them.
- `sorted-keys` (`sk`): Are the i18n source and target locale files sorted alphabetically?
  - Sort them alphabetically to reduce merge conflicts from the files changing.
  - Pass `--fix` (`-f`) to sort the i18n files automatically.
  - Note: The `--fix` option for other checks will sort the keys if this check is active.
  - Note: Sorting is done such that periods come before underscores (some JSON extensions do otherwise).
- `nested-files` (`nf`): Do the i18n files contain nested JSON structures?
  - Flatten them to make replacing invalid keys easier with find-and-replace all.
- `missing-keys` (`mk`): Are any keys from the source file missing in the locale files?
  - Add the missing keys to ensure all translations are complete.
  - Keys with empty string values are also considered missing.
  - Pass `--fix --locale ENTER_ISO_2_CODE` (`-f -l ENTER_ISO_2_CODE`) to interactively add missing keys.
- `aria-labels` (`al`): Do keys that end in `_aria_label` end in punctuation?
  - Remove the punctuation as it negatively affects screen reader experience.
  - Pass `--fix` (`-f`) to remove punctuation automatically.
- `alt-texts` (`at`): Do keys that end in `_alt_text` lack proper punctuation?
  - Add periods to the end to comply with alt text guidelines.
  - Pass `--fix` (`-f`) to add periods automatically.

> [!NOTE]
> The `aria-labels` and `alt-texts` checks function for LTR and RTL languages.

Directions for how to fix the i18n files are provided when errors are raised. Checks can also be disabled in the workflow via options passed in the configuration YAML file.

<a id="configuration-"></a>

# Configuration [`⇧`](#contents)

<a id="yaml-file-"></a>

### YAML File [`⇧`](#contents)

The following details the `.i18n-check.yaml` configuration file, with a further example being the [configuration file for this repository](/.i18n-check.yaml) that we use in testing.

> [!NOTE]
> Both `.i18n-check.yaml` and `.i18n-check.yml` file extensions are supported. If both files exist, `.yaml` will be preferred.

> [!NOTE]
> When `global.active` is set to `true`, all checks are enabled by default. You can then explicitly disable specific checks by setting their `active` value to `false`. This allows for more concise configuration files. For example:
>
> ```yaml
> checks:
>   global:
>     active: true
>   missing-keys:
>     active: false # disabled even though global is active
> ```

```yaml
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
```

<a id="additional-arguments-"></a>

### Additional Arguments [`⇧`](#contents)

Common additional arguments for using specific web frameworks can be found in the dropdowns below:

<details><summary>Vue.js</summary>
<p>

```yaml
file_types_to_check: [.vue]

checks:
  global:
    directories_to_skip: [frontend/.nuxt, frontend/.output, frontend/dist]
```

</p>
</details>

<a id="pre-commit-"></a>

### pre-commit [`⇧`](#contents)

The following is an example [pre-commit](https://github.com/pre-commit/pre-commit) hook:

```yaml
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
```

<a id="github-action-"></a>

### GitHub Action [`⇧`](#contents)

The following is an example YAML file for a GitHub Action to check your i18n files on PRs and commits:

```yaml
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
```

<a id="contributing"></a>

# Contributing [`⇧`](#contents)

<a href="https://matrix.to/#/#activist_community:matrix.org"><img src="https://raw.githubusercontent.com/activist-org/Organization/main/resources/images/logos/MatrixLogoGrey.png" width="175" alt="Public Matrix Chat" align="right"></a>

activist uses [Matrix](https://matrix.org/) for internal communication. You're more than welcome to [join us in our public chat rooms](https://matrix.to/#/#activist_community:matrix.org) to share ideas, ask questions or just say hi to the team :) We'd suggest that you use the [Element](https://element.io/) client and [Element X](https://element.io/app) for a mobile app.

Please see the [contribution guidelines](CONTRIBUTING.md) if you are interested in contributing. Work that is in progress or could be implemented is tracked in the [issues](https://github.com/activist-org/i18n-check/issues) and [projects](https://github.com/activist-org/i18n-check/projects).

> [!NOTE]
> Just because an issue is assigned on GitHub doesn't mean the team isn't open to your contribution! Feel free to write [in the issues](https://github.com/activist-org/i18n-check/issues) and we can potentially reassign it to you.

Also check the [`-next release-`](https://github.com/activist-org/i18n-check/labels/-next%20release-) and [`-priority-`](https://github.com/activist-org/i18n-check/labels/-priority-) labels in the [issues](https://github.com/activist-org/i18n-check/issues) for those that are most important, as well as those marked [`good first issue`](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) that are tailored for first-time contributors. For those new to coding or our tech stack, we've collected [links to helpful documentation pages](CONTRIBUTING.md#learning-the-tech-stack-) in the [contribution guidelines](CONTRIBUTING.md).

We would be happy to discuss granting you further rights as a contributor after your first pull requests, with a maintainer role then being possible after continued interest in the project. activist seeks to be an inclusive, diverse and supportive organization. We'd love to have you on the team!

<a id="how-you-can-help"></a>

## How you can help [`⇧`](#contents)

- [Reporting bugs](https://github.com/activist-org/i18n-check/issues/new?assignees=&labels=bug&template=bug_report.yml) as they're found 🐞
- Working with us on [new features](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue+is%3Aopen+label%3Afeature) ✨
- [Documentation](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation) for onboarding and project cohesion 📝

<a id="environment-setup-"></a>

# Environment setup [`⇧`](#contents)

1. First and foremost, please see the suggested IDE setup in the dropdown below to make sure that your editor is ready for development.

> [!IMPORTANT]
>
> <details><summary>Suggested IDE setup</summary>
>
> <p>
>
> VS Code
>
> Install the following extensions:
>
> - [charliermarsh.ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
> - [streetsidesoftware.code-spell-checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
>
> </p>
> </details>

2. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the [i18n-check repo](https://github.com/activist-org/i18n-check), clone your fork, and configure the remotes:

> [!NOTE]
>
> <details><summary>Consider using SSH</summary>
>
> <p>
>
> Alternatively to using HTTPS as in the instructions below, consider SSH to interact with GitHub from the terminal. SSH allows you to connect without a user-pass authentication flow.
>
> To run git commands with SSH, remember then to substitute the HTTPS URL, `https://github.com/...`, with the SSH one, `git@github.com:...`.
>
> - e.g. Cloning now becomes `git clone git@github.com:<your-username>/i18n-check.git`
>
> GitHub also has their documentation on how to [Generate a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) 🔑
>
> </p>
> </details>

```bash
# Clone your fork of the repo into the current directory.
git clone https://github.com/<your-username>/i18n-check.git
# Navigate to the newly cloned directory.
cd i18n-check
# Assign the original repo to a remote called "upstream".
git remote add upstream https://github.com/activist-org/i18n-check.git
```

- Now, if you run `git remote -v` you should see two remote repositories named:
  - `origin` (forked repository)
  - `upstream` (i18n-check repository)

3. Create a virtual environment for i18n-check (Python `>=3.12`), activate it and install dependencies:

   > [!NOTE]
   > First, install `uv` if you don't already have it by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

   ```bash
   uv sync --all-extras  # create .venv and install all dependencies from uv.lock

   # Unix or macOS:
   source .venv/bin/activate

   # Windows:
   .venv\Scripts\activate.bat  # .venv\Scripts\activate.ps1 (PowerShell)
   ```

> [!NOTE]
> If you change dependencies in `pyproject.toml`, regenerate the lock file with the following command:
>
> ```bash
> uv lock  # refresh uv.lock for reproducible installs
> ```

After activating the virtual environment, set up [pre-commit](https://pre-commit.com/) by running:

```bash
pre-commit install
# uv run pre-commit run --all-files  # lint and fix common problems in the codebase
```

You're now ready to work on `i18n-check`!

> [!NOTE]
> Feel free to contact the team in the [Development room on Matrix](https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz) if you're having problems getting your environment setup!

<a id="contributors-"></a>

# Contributors [`⇧`](#contents)

Thanks to all our amazing [contributors](https://github.com/activist-org/i18n-check/graphs/contributors)! ❤️

<a href="https://github.com/activist-org/i18n-check/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=activist-org/i18n-check" />
</a>
