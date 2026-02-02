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

# Contents

- [About i18n-check](#about-i18n-check)
- [Key Conventions](#key-conventions)
- [Installation](#installation)
  - [Users](#users)
  - [Development Build](#development-build)
- [How It Works](#how-it-works)
  - [Commands](#commands)
  - [Checks](#checks)
  - [Example Responses](#example-responses)
- [Configuration](#configuration)
  - [YAML File](#yaml-file)
  - [Arguments](#arguments)
  - [Additional Arguments](#additional-arguments)
  - [pre-commit](#pre-commit)
  - [GitHub Action](#github-action)
- [Contributing](#contributing)
  - [New Contributors](#new-contributors)
  - [How to Help](#how-to-help)
  - [Contact the Team](#contact-the-team)
- [Environment setup](#environment-setup)
- [Contributors](#contributors)

# About i18n-check

`i18n-check` is a Python package that automates the validation of keys and values for your internationalization and localization processes.

Developed by the [activist community](https://github.com/activist-org), this package helps keep development and i18n/L10n teams in sync when using JSON-based localization processes.

# Key Conventions

`i18n-check` enforces these conventions for all keys:

- All keys must begin with `i18n.`.
- The base path must be the file path where the key is used.
- If a key is used in more than one file, the base path must be the lowest common directory and end with `_global`.
- Base paths must be followed by a minimally descriptive content reference (`i18n-check` only checks content references for formatting).
- Separate base paths with periods (`.`).
- Separate directory / file name components and content references with underscores (`_`).
- Repeated words in the file path, including the file name, must not be repeated in the key.

> [!TIP]
> Example of a valid file / key pair:
>
> **File:** `components/component/ComponentName.ext`
>
> **Key:** `"i18n.components.component_name.content_reference"`

# Installation

## Users

You can install `i18n-check` using [uv](https://docs.astral.sh/uv/) (recommended) or [pip](https://pypi.org/project/i18n-check/).

### uv

(Recommended - fast, Rust-based installer)

```bash
uv pip install i18n-check
```

### pip

```bash
pip install i18n-check
```

## Development Build

You can install the latest development build using uv, pip, or by cloning the repository.

### Clone the Repository (Development Build)

```bash
git clone https://github.com/activist-org/i18n-check.git  # or ideally your fork
cd i18n-check
```

### uv (Development Build)

```bash
uv sync --all-extras  # install all dependencies
source .venv/bin/activate  # activate venv (macOS/Linux)
# .venv\Scripts\activate  # activate venv (Windows)
```

### pip (Development Build)

```bash
python -m venv .venv  # create virtual environment
source .venv/bin/activate  # activate venv (macOS/Linux)
# .venv\Scripts\activate  # activate venv (Windows)
pip install -e .
```

# How It Works

## Commands

These are some example commands:

**View Help**

```bash
i18n-check -h
```

**Generate a Configuration File**

```bash
i18n-check -gcf
```

**Generate Test Frontends**

```bash
i18n-check -gtf
```

**Run All Checks**

```bash
i18n-check -a
```

**Run a Specific [Check](#checks)**

```bash
i18n-check -CHECK_ID
```

**Interactive Mode - Add Missing Keys**

```bash
i18n-check -mk -f -l ENTER_ISO_2_CODE
```

## Checks

When `i18n-check` finds errors, it provides directions for resolving them. You can also disable checks in the workflow by modifying the configuration [YAML file](#yaml-file).

You can run these checks across your codebase:

| Check                                                                                        | Command                   | Resolution                                                                                                                                                                              | Fix Command                                                                                                                                              |
| -------------------------------------------------------------------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Does the source file contain keys that don't follow the required formatting rules?           | `key-formatting` (`kf`)   | Format the keys in the source file to match the conventions.                                                                                                                            | `--fix` (`-f`) to fix all formatting issues automatically.                                                                                               |
| Are key names consistent with how and where they are used in the codebase?                   | `key-naming` (`kn`)       | Rename them so i18n key usage is consistent and their scope is communicated in their name.                                                                                              | `--fix` (`-f`) to fix all naming issues automatically.                                                                                                   |
| Does the codebase include i18n keys that are not within the source file?                     | `nonexistent-keys` (`nk`) | Check their validity and resolve if they should be added to the i18n files or replaced.                                                                                                 | `--fix` (`-f`) to interactively add nonexistent keys.                                                                                                    |
| Does the source file have keys that are not used in the codebase?                            | `unused-keys` (`uk`)      | Remove them so the localization team isn't working on strings that aren't used.                                                                                                         | n/a                                                                                                                                                      |
| Do the target locale files have keys that are not in the source file?                        | `non-source-keys` (`nsk`) | Remove them as they won't be used in the application.                                                                                                                                   | n/a                                                                                                                                                      |
| Do any of localization files have repeat keys?                                               | `repeat-keys` (`rk`)      | Separate them so that the values are not mixed when they're in production. <br> <br> **Note:** The existence of repeat keys prevents keys from being sorted by the `sorted-keys` check. | n/a                                                                                                                                                      |
| Does the source file have repeat values that can be combined into a single key?              | `repeat-values` (`rv`)    | Combine them so the localization team only needs to localize one of them.                                                                                                               | n/a                                                                                                                                                      |
| Are the i18n source and target locale files sorted alphabetically?                           | `sorted-keys` (`sk`)      | Sort them alphabetically to reduce merge conflicts from the files changing. Sorting is done such that periods come before underscores (some JSON extensions do otherwise).              | `--fix` (`-f`) to sort the i18n files automatically. <br> <br> **Note:** The `--fix` option for other checks will sort the keys if this check is active. |
| Do the i18n files contain nested JSON structures?                                            | `nested-files` (`nf`)     | Flatten them to make replacing invalid keys easier with find-and-replace all.                                                                                                           | n/a                                                                                                                                                      |
| Are any keys from the source file missing in the locale files?                               | `missing-keys` (`mk`)     | Add the missing keys to ensure all translations are complete. <br> Keys with empty string values are considered missing.                                                                | `--fix --locale ENTER_ISO_2_CODE` (`-f -l ENTER_ISO_2_CODE`) to interactively add missing keys.                                                          |
| For both LTR and RTL languages, do keys that end in `_aria_label` end in punctuation?        | `aria-labels` (`al`)      | Remove the punctuation, as it negatively affects screen reader experience.                                                                                                              | `--fix` (`-f`) to remove punctuation automatically.                                                                                                      |
| For both LTR and RTL languages, are keys that end in `_alt_text` missing proper punctuation? | `alt-texts` (`at`)        | Add periods to the end to comply with alt text guidelines.                                                                                                                              | `--fix` (`-f`) to add periods automatically.                                                                                                             |

## Example Responses

These GIFs show the response to the command `i18n-check -a` when all checks fail or pass.

### All Checks Fail

![i18n_check_all_fail](https://github.com/user-attachments/assets/757a9f6f-7bde-40db-941d-c4e82855a453)

### All Checks Pass

![i18n_check_all_pass](https://github.com/user-attachments/assets/c024c368-7691-4489-b8b8-a9844d386177)

# Configuration

## YAML File

You can configure `i18n-check` using the `.i18n-check.yaml` (or `.yml`) configuration file.

For an example, see the [configuration file for this repository](/.i18n-check.yaml) that we use in testing.

The following details the potential contents of this file:

> [!NOTE]
> When `global.active` is set to `true`, all checks are enabled by default. You can then disable specific checks by setting their `active` value to `false`. This allows for more concise configuration files. Example:
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

## Arguments

In the `.i18n-check.yaml` or `.i18n-check.yml` [configuration](#configuration) file, provide these arguments:

- `src-dir`: The directory path to your source code.
- `i18n-dir`: The directory path to your i18n files.
- `i18n-src`: The name of your i18n source file.
- `file-types-to-check`: The file types to include in the check.

## Additional Arguments

You can find common additional arguments for using specific web frameworks here:

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

## pre-commit

This is an example [pre-commit](https://github.com/pre-commit/pre-commit) hook:

```yaml
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
```

## GitHub Action

This is an example YAML file for a GitHub Action to check your `i18n-files` on PRs and commits:

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
          python-version: "3.12"

      - name: Install uv
        uses: astral-sh/setup-uv@v7

      - name: Install Dependencies
        run: uv sync --frozen --all-extras

      - name: Execute All i18n-check Key-Value Checks
        run: |
          uv run i18n-check -a
```

# Contributing

See the [contribution guidelines](CONTRIBUTING.md) before contributing.

We track work that is in progress or might be implemented in the [issues](https://github.com/activist-org/i18n-check/issues) and [projects](https://github.com/activist-org/i18n-check/projects).

Just because an issue is assigned doesn't mean you can't contribute. Write [in the issues](https://github.com/activist-org/i18n-check/issues) and we may reassign it to you.

Check the [`-next release-`](https://github.com/activist-org/i18n-check/labels/-next%20release-) and [`-priority-`](https://github.com/activist-org/i18n-check/labels/-priority-) labels to find the most important [issues](https://github.com/activist-org/i18n-check/issues).

## New Contributors

Issues labelled [`good first issue`](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are the best choice for new contributors.

New to coding or our tech stack? We've collected [links to helpful documentation](CONTRIBUTING.md#learning-the-tech-stack).

We would be happy to discuss granting you further rights as a contributor after your first pull requests, with a maintainer role then being possible after continued interest in the project. activist seeks to be an inclusive, diverse, and supportive organization. We'd love to have you on the team! Please see the [mentorship and growth section of the contribution guide](CONTRIBUTING.md#mentorship-and-growth-) for further information.

## How to Help

- 🐞 [Report bugs](https://github.com/activist-org/i18n-check/issues/new?assignees=&labels=bug&template=bug_report.yml) as they're found.
- ✨ Work with us on [new features](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue+is%3Aopen+label%3Afeature).
- 📝 Improve the [documentation](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation) to support onboarding and project uptake.

## Contact the Team

<a href="https://matrix.to/#/#activist_community:matrix.org"><img src="https://raw.githubusercontent.com/activist-org/Organization/main/resources/images/logos/MatrixLogoGrey.png" width="175" alt="Public Matrix Chat" align="right"></a>

activist uses [Matrix](https://matrix.org/) for team communication. [Join us in our public chat rooms](https://matrix.to/#/#activist_community:matrix.org) to share ideas, ask questions, or just say hi to the team.

We recommend using the [Element](https://element.io/) client and [Element X](https://element.io/app) for a mobile app.

# Environment setup

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

> [!TIP]
> Contact the team in the [Development room on Matrix](https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz) if you need help setting up your environment.

# Contributors

Thanks to all our amazing [contributors](https://github.com/activist-org/i18n-check/graphs/contributors)! ❤️

<a href="https://github.com/activist-org/i18n-check/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=activist-org/i18n-check" />
</a>
