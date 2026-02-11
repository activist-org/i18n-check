# Contributing to i18n-check

> [!IMPORTANT]
>
> Thank you for your interest in contributing to `i18n-check`!
>
> Please take a moment to review this document. Doing so will help make the contribution process easy and effective for everyone.
>
> By following this guide, you show respect for the time of those who manage and develop this open-source project. 
>
> In return, and in accordance with this project's [code of conduct](https://github.com/activist-org/i18n-check/tree/main/.github/CODE_OF_CONDUCT.md), other contributors will reciprocate that respect as they address your issue or assess patches / features.
>
> To contact us, [join our public Matrix chat rooms](https://matrix.to/#/#activist_community:matrix.org). We'd be happy to hear from you!

# Contents

- [Get Started as a Contributor](#get-started-as-a-contributor)
    - [Choose Your First Issue](#choose-your-first-issue)
    - [Mentorship and Growth](#mentorship-and-growth)
    - [Learn the Tech Stack](#learn-the-tech-stack)
- [Development Environment](#devolpment-environment)
    - [Linting and Testing](#linting-and-testing)
- [Creating Issues](#creating-issues)
    - [Bug Reports](#bug-reports)
    - [Feature Requests](#feature-requests)
    - [Pull Requests](#pull-requests)
- [Documentation](#documentation)
    - [Function Docstrings](#function-docstrings)
    - [Build the Documentation Locally](#build-the-documentation-locally)

# Get Started as a Contributor

The `i18n-check` community looks forward to welcoming you as a contributor! 

We recommend these first steps for anyone interested in joining us:

1. Join the [public Matrix chat](https://matrix.to/#/#activist_community:matrix.org) to connect with the community. [Matrix](https://matrix.org/) is a network for secure, decentralized communication
  - We recommend you use the [Element](https://element.io/) client and [Element X](https://element.io/app) for a mobile app.
2. If you're comfortable, introduce yourself and tell us about your interests in the [General](https://matrix.to/#/!uIGQUxlCnEzrPiRsRw:matrix.org?via=matrix.org&via=effektio.org&via=acter.global) channel.
3. Take a look at the [Development](https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz) channel for recent development discussions.
4. Consider joining our [bi-weekly developer sync](https://etherpad.wikimedia.org/p/activist-dev-sync) Newcomers are always welcome!

## Choose Your First Issue

Issues labelled [`good first issue`](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are the best choice for new contributors.

Just because an issue is assigned doesn't mean you can't contribute. Write [in the issues](https://github.com/activist-org/i18n-check/issues) and we may reassign it to you.

Check the [`-next release-`](https://github.com/activist-org/i18n-check/labels/-next%20release-) and [`-priority-`](https://github.com/activist-org/i18n-check/labels/-priority-) labels to find the most important [issues](https://github.com/activist-org/i18n-check/issues).

We would be happy to discuss granting you further rights as a contributor after your first pull requests, with a maintainer role then being possible after continued interest in the project. activist seeks to be an inclusive, diverse, and supportive organization. We'd love to have you on the team!

## Mentorship and Growth

Onboarding and mentoring new members is vital to a healthy open-source community. 

We need contributors who are onboarded to gain new skills and take on greater roles by triaging issues, reviewing contributions, and maintaining the project. We also need them to help new contributors to grow as well.

Please let us know if you have mentorship goals and we'll work with you to achieve them.

We also have expectations about the behavior of those who want to grow with us. Mentorship is earned, not given. 

To be blunt, those who are mainly sending AI generated contributions are not demonstrating an interest in growing their skills and are not helping to develop the project. This is not to say that all uses of AI for contributions are bad, but **AI should be a tool, not the contributor itself**.

Continued constructive contributions, new open issues, and clear communication helps the project. We would be happy to help community members who can make these contributions to expand their skills and take on further responsibilities.

If you like the sound of this, then we look forward to working with you!

## Learn the Tech Stack

`i18n-check` is open to contributions from people in the early stages of their coding journey! 

This is a select list of documentation to help you understand the technologies we use:

<details><summary>Docs for new developers</summary>
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

<sub><a href="#top">Back to top.</a></sub>

# Development Environment

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

> [!TIP]
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

3. Install `uv` if you don't already have it by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

4. Create a virtual environment for i18n-check (Python `>=3.12`), activate it and install dependencies:

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

After activating the virtual environment, set up [prek](https://prek.j178.dev/) by running:

```bash
prek install
# uv run prek run --all-files  # lint and fix common problems in the codebase
```

You're now ready to work on `i18n-check`!

> [!TIP]
> Contact the team in the [Development room on Matrix](https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz) if you need help setting up your environment.

## Linting and Testing

To ensure errors are reported correctly, [Ruff](https://github.com/astral-sh/ruff) is included in the required packages. 

For VS Code users, we recommend you install the [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff).

To test your changes, run these commands from the project root:

**Format the src Directory**

```bash
ruff format ./src
```

**Lint the Code**

```bash
ruff check ./src
```

**Run Static Type Tests**

```bash
mypy ./src --config-file ./pyproject.toml
```

**Run Tests**

```bash
pytest
```

**Run a Specific Test**

```bash
pytest path/to/test_file.py::test_function
```

**Run Tests with a Coverage Report**

```bash
pytest . --cov=src --cov-report=term-missing --cov-config=./pyproject.toml
```

<sub><a href="#top">Back to top.</a></sub>

# Creating Issues

The GitHub [issue tracker](https://github.com/activist-org/i18n-check/issues) is our preferred channel for [bug reports](#bug-reports), [features requests](#feature-requests) and [submitting pull requests](#pull-requests). 

We also organize related issues into [projects](https://github.com/activist-org/i18n-check/projects).

## Bug Reports

> [!IMPORTANT]
> We define a bug as a demonstrable problem caused by code in the repository. 

Good bug reports are extremely helpful, and we greatly appreciate them.

To submit a bug report:

1. Check if the bug has already been reported by searching issues on GitHub. Filter for issues marked with the marked with the [`Bug`](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue%20state%3Aopen%20type%3ABug) label.

2. Try to reproduce the bug using the latest `main` or development branch in the repository. This ensures it hasn't already been fixed.

3. Isolate the problem to make sure that the code in the repository is definitely responsible for the bug.

4. If you're confident you've found a bug, report it using the [bug report template](https://github.com/activist-org/i18n-check/issues/new?assignees=&labels=bug&projects=activist-org%2F1&template=bug_report.yml). 

We thank you for the time you take to report bugs!

## Feature Requests

> [!IMPORTANT]
> Before you submit a request, please take a moment to check whether your idea fits with the scope and aims of the project.

Feature requests are welcome! 

When you submit a feature request, provide as much detail and context as possible. Please also let us know whether you would like to contribute to the development. 

Submit your request using the [issue tracker](https://github.com/activist-org/i18n-check/issues).

We mark feature requests with the [`Feature`](https://github.com/activist-org/i18n-check/issues?q=is%3Aissue%20state%3Aopen%20type%3AFeature) label.

## Pull Requests

> [!IMPORTANT]
> All contributions to this project will be made under [the specified license](LICENSE.txt) and should follow the coding indentation and style standards (contact us if unsure). 
>
>The best way to get your work merged is to follow the [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow) process.

Good pull requests should remain focused in scope and avoid containing unrelated commits.

**Please ask first** before embarking on any significant pull request, otherwise you risk spending a lot of time working on something that the developers might not want to merge into the project. With that being said, major additions are very appreciated!

### Install prek

Before you submit a pull request, install [prek](https://prek.j178.dev/) to ensure your commits are properly checked by our linter and formatters.

prek is Python package that you can install via pip or any other Python package manager. You can also find it in our [uv.lock](./uv.lock) file.

To install prek:

   ```bash
   # In the project root:
   prek install

   # Then test the pre-commit hooks to see how it works:
   uv run prek run --all-files
   ```

If you're having difficulties with prek and you want to submit your changes anyway, you can ignore the pre-commit hook with:

```bash
git commit --no-verify -m "COMMIT_MESSAGE"
```

### Commit Changes and Submit a Pull Request

> [!NOTE]
> These are some tools and methods to help you write good commit messages:
>
> - [commitlint](https://commitlint.io/) helps write [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
> - Git's [interactive rebase](https://docs.github.com/en/github/getting-started-with-github/about-git-rebase) cleans up commits.

To commit changes and submit a pull request:

1. Make sure your repository has the latest upstream changes:

   ```bash
   git checkout <dev-branch>
   git pull upstream <dev-branch>
   ```

2. Create a new topic branch off the main project branch:

   ```bash
   git checkout -b <topic-branch-name>
   ```

3. Commit your changes in logical chunks, and please try to adhere to [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).


4. Locally merge or rebase the upstream main development branch into your topic branch:

   ```bash
   git pull --rebase upstream <dev-branch>
   ```

5. Push your topic branch to your fork:

   ```bash
   git push origin <topic-branch-name>
   ```

6. [Open a Pull Request](https://help.github.com/articles/using-pull-requests/) with a clear title and description.

Thank you in advance for your contributions!

<sub><a href="#top">Back to top.</a></sub>

# Documentation

Find the `i18n-check` documentation at [i18n-check.readthedocs.io](https://i18n-check.readthedocs.io/en/latest/). 

Documentation is an invaluable way to contribute to coding projects. It enables others to better understand and contribute to the project. 

Search for open documentation issues on GitHub by filtering for the [`documentation`](https://github.com/activist-org/i18n-check/labels/documentation) label.

## Function Docstrings

`i18n-check` follows [numpydoc conventions](https://numpydoc.readthedocs.io/en/latest/format.html) for documenting functions and Python code. 

Function docstrings should have this format:

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

## Build the Documentation Locally

To build the documentation locally, run these commands:

```bash
cd docs
make html
```

To view the documentation, in `docs/build/html` open `index.html`.

<sub><a href="#top">Back to top.</a></sub>
