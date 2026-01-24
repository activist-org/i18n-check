# Contributing to i18n-check

Thank you for contributing to `i18n-check`!

Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open-source project. In return, and in accordance with this project's [code of conduct](https://github.com/activist-org/i18n-check/tree/main/.github/CODE_OF_CONDUCT.md), other contributors will reciprocate that respect in addressing your issue or assessing patches and features.

If you have questions or would like to communicate with the team, please [join us in our public Matrix chat rooms](https://matrix.to/#/#activist_community:matrix.org). We'd be happy to hear from you!

<a id="contents"></a>

## **Contents**

- [First steps as a contributor](#first-steps-)
- [Learning the tech stack](#learning-the-tech-stack-)
- [Development environment](#dev-env-)
- [Linting](#linting-)
- [Testing](#testing-)
- [Issues and projects](#issues-projects-)
- [Bug reports](#bug-reports-)
- [Feature requests](#feature-requests-)
- [Pull requests](#pull-requests-)
- [Documentation](#documentation)

<a id="first-steps-"></a>

## First steps as a contributor [`⇧`](#contents)

Thank you for your interest in contributing to activist community projects! We look forward to welcoming you :) The following are some suggested steps for people interested in joining our community:

- Please join the [public Matrix chat](https://matrix.to/#/#activist_community:matrix.org) to connect with the community
  - [Matrix](https://matrix.org/) is a network for secure, decentralized communication
  - We'd suggest that you use the [Element](https://element.io/) client and [Element X](https://element.io/app) for a mobile app
  - The [General](https://matrix.to/#/!uIGQUxlCnEzrPiRsRw:matrix.org?via=matrix.org&via=effektio.org&via=acter.global) and [Development](https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz) channels would be great places to start!
  - Feel free to introduce yourself and tell us what your interests are if you're comfortable :)
- Consider joining our [bi-weekly developer sync](https://etherpad.wikimedia.org/p/activist-dev-sync)!

<a id="learning-the-tech-stack-"></a>

## Learning the tech stack [`⇧`](#contents)

`i18n-check` is very open to contributions from people in the early stages of their coding journey! The following is a select list of documentation pages to help you understand the technologies we use.

<details><summary>Docs for those new to programming</summary>
<p>

- [Mozilla Developer Network Learning Area](https://developer.mozilla.org/en-US/docs/Learn)
  - Doing MDN sections for HTML, CSS and JavaScript is the best ways to get into web development!
- [Open Source Guides](https://opensource.guide/)
  - Guides from GitHub about open-source software including how to start and much more!

</p>
</details>

<details><summary>Python learning docs</summary>
<p>

- [Python getting started guide](https://docs.python.org/3/tutorial/introduction.html)
- [Python getting started resources](https://www.python.org/about/gettingstarted/)

</p>
</details>

<a id="dev-env-"></a>

## Development environment [`⇧`](#contents)

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
  - `upstream` (`i18n-check` repository)

3. Create a virtual environment for i18n-check (Python `>=3.12`), activate it and install dependencies:

   > [!NOTE]
   > First, install `uv` if you don't already have it by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

   ```bash
   uv sync --all-extras  # create .venv and install all dependencies from uv.lock

   # Unix or macOS:
   source .venv/bin/activate

   # Windows:
   .venv\Scripts\activate.bat # .venv\Scripts\activate.ps1 (PowerShell)
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

<a id="linting-"></a>

## Linting [`⇧`](#contents)

[Ruff](https://github.com/astral-sh/ruff) is installed via the required packages to assure that errors are reported correctly. We'd also suggest that VS Code users install the [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff).

<a id="testing-"></a>

## Testing [`⇧`](#contents)

Please run the following commands from the project root to test:

```bash
# Format the src directory, lint the code and run static type checks:
ruff format ./src
ruff check ./src
mypy ./src --config-file ./pyproject.toml

# Run tests:
pytest

# To run a specific test:
pytest path/to/test_file.py::test_function

# To run with a coverage report as is done in PRs:
pytest . --cov=src --cov-report=term-missing --cov-config=./pyproject.toml
```

<a id="issues-projects"></a>

## Issues and projects [`⇧`](#contents)

The [issue tracker for i18n-check](https://github.com/activist-org/i18n-check/issues) is the preferred channel for [bug reports](#bug-reports), [features requests](#feature-requests) and [submitting pull requests](#pull-requests). The activist community also organizes related issues into [projects](https://github.com/activist-org/i18n-check/projects).

<a name="bug-reports"></a>

## Bug reports [`⇧`](#contents)

A bug is a _demonstrable problem_ that is caused by the code in the repository. Good bug reports are extremely helpful — thank you!

Guidelines for bug reports:

1. **Use the GitHub issue search** to check if the issue has already been reported.

2. **Check if the issue has been fixed** by trying to reproduce it using the latest `main` or development branch in the repository.

3. **Isolate the problem** to make sure that the code in the repository is _definitely_ responsible for the issue.

**Great Bug Reports** tend to have:

- A quick summary
- Steps to reproduce
- What you expected would happen
- What actually happens
- Notes (why this might be happening, things tried that didn't work, etc)

To make the above steps easier, the `i18n-check` team asks that contributors report bugs using the [bug report template](https://github.com/activist-org/i18n-check/issues/new?assignees=&labels=bug&projects=activist-org%2F1&template=bug_report.yml), with these issues further being marked with the [`Bug`](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue%20state%3Aopen%20type%3ABug) type.

Again, thank you for your time in reporting issues!

<a name="feature-requests-"></a>

## Feature requests [`⇧`](#contents)

Feature requests are more than welcome! Please take a moment to find out whether your idea fits with the scope and aims of the project. When making a suggestion, provide as much detail and context as possible, and further make clear the degree to which you would like to contribute in its development. Feature requests are marked with the [`Feature`](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue%20state%3Aopen%20type%3AFeature) type in the [issues](https://github.com/activist-org/i18n-check/issues).

<a name="pull-requests-"></a>

## Pull requests [`⇧`](#contents)

Good pull requests — patches, improvements and new features — are the foundation of our community making `i18n-check`. They should remain focused in scope and avoid containing unrelated commits. Note that all contributions to this project will be made under [the specified license](LICENSE.txt) and should follow the coding indentation and style standards (contact us if unsure).

**Please ask first** before embarking on any significant pull request (implementing features, refactoring code, etc), otherwise you risk spending a lot of time working on something that the developers might not want to merge into the project. With that being said, major additions are very appreciated!

When making a contribution, adhering to the [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow) process is the best way to get your work merged:

1. If you cloned a while ago, get the latest changes from upstream:

   ```bash
   git checkout <dev-branch>
   git pull upstream <dev-branch>
   ```

2. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix:

   ```bash
   git checkout -b <topic-branch-name>
   ```

3. Install [pre-commit](https://pre-commit.com/) to ensure that each of your commits is properly checked against our linter and formatters:

   ```bash
   # In the project root:
   pre-commit install

   # Then test the pre-commit hooks to see how it works:
   # uv run pre-commit run --all-files
   ```

> [!NOTE]
> pre-commit is Python package that can be installed via pip or any other Python package manager. You can also find it in our [uv.lock](./uv.lock) file.
>
> ```bash
> pip install pre-commit
> ```

> [!NOTE]
> If you are having issues with pre-commit and want to send along your changes regardless, you can ignore the pre-commit hooks via the following:
>
> ```bash
> git commit --no-verify -m "COMMIT_MESSAGE"
> ```

4. Commit your changes in logical chunks, and please try to adhere to [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

> [!NOTE]
> The following are tools and methods to help you write good commit messages ✨
>
> - [commitlint](https://commitlint.io/) helps write [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
> - Git's [interactive rebase](https://docs.github.com/en/github/getting-started-with-github/about-git-rebase) cleans up commits

5. Locally merge (or rebase) the upstream development branch into your topic branch:

   ```bash
   git pull --rebase upstream <dev-branch>
   ```

6. Push your topic branch up to your fork:

   ```bash
   git push origin <topic-branch-name>
   ```

7. [Open a Pull Request](https://help.github.com/articles/using-pull-requests/) with a clear title and description.

Thank you in advance for your contributions!

<a id="documentation"></a>

## Documentation [`⇧`](#contents)

The documentation for `i18n-check` can be found at [i18n-check.readthedocs.io](https://i18n-check.readthedocs.io/en/latest/). Documentation is an invaluable way to contribute to coding projects as it allows others to more easily understand the project structure and contribute. Issues related to documentation are marked with the [`documentation`](https://github.com/activist-org/i18n-check/labels/documentation) label.

### Function Docstrings

`i18n-check` generally follows [numpydoc conventions](https://numpydoc.readthedocs.io/en/latest/format.html) for documenting functions and Python code in general. Function docstrings should have the following format:

```py
def example_function(argument: argument_type) -> return_type:
    """
    An example docstring for a function so others understand your work.

    Parameters
    ----------
    argument : argument_type
        Description of your argument.

    Returns
    -------
    return_value : return_type
        Description of your return value.

    Raises
    ------
    ErrorType
        Description of the error and the condition that raises it.
    """

    ...

    return return_value
```

### Building the Docs

Use the following commands to build the documentation locally:

```bash
cd docs
make html
```

You can then open `index.html` within `docs/build/html` to check the local version of the documentation.
