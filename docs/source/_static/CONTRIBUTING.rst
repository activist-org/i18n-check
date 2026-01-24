==========================
Contributing to i18n-check
==========================

Thank you for contributing to ``i18n-check``!

Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open-source project. In return, and in accordance with this project's `code of conduct <https://github.com/activist-org/i18n-check/tree/main/.github/CODE_OF_CONDUCT.md>`_, other contributors will reciprocate that respect in addressing your issue or assessing patches and features.

If you have questions or would like to communicate with the team, please `join us in our public Matrix chat rooms <https://matrix.to/#/#activist_community:matrix.org>`_. We'd be happy to hear from you!

.. _contents:

Contents
--------

* `First steps as a contributor`_
* `Learning the tech stack`_
* `Development environment`_
* `Linting`_
* `Testing`_
* `Issues and projects`_
* `Bug reports`_
* `Feature requests`_
* `Pull requests`_
* `Documentation`_

.. _first-steps:

First steps as a contributor
----------------------------

Thank you for your interest in contributing to activist community projects! We look forward to welcoming you :) The following are some suggested steps for people interested in joining our community:

* Please join the `public Matrix chat <https://matrix.to/#/#activist_community:matrix.org>`_ to connect with the community
    * `Matrix <https://matrix.org/>`_ is a network for secure, decentralized communication
    * We'd suggest that you use the `Element <https://element.io/>`_ client and `Element X <https://element.io/app>`_ for a mobile app
    * The `General <https://matrix.to/#/!uIGQUxlCnEzrPiRsRw:matrix.org?via=matrix.org&via=effektio.org&via=acter.global>`_ and `Development <https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz>`_ channels would be great places to start!
    * Feel free to introduce yourself and tell us what your interests are if you're comfortable :)
* Consider joining our `bi-weekly developer sync <https://etherpad.wikimedia.org/p/activist-dev-sync>`_!

.. _learning-the-tech-stack:

Learning the tech stack
-----------------------

``i18n-check`` is very open to contributions from people in the early stages of their coding journey! The following is a select list of documentation pages to help you understand the technologies we use.

.. admonition:: Docs for those new to programming

   * `Mozilla Developer Network Learning Area <https://developer.mozilla.org/en-US/docs/Learn>`_
      * Doing MDN sections for HTML, CSS and JavaScript is the best ways to get into web development!
   * `Open Source Guides <https://opensource.guide/>`_
      * Guides from GitHub about open-source software including how to start and much more!

.. admonition:: Python learning docs

   * `Python getting started guide <https://docs.python.org/3/tutorial/introduction.html>`_
   * `Python getting started resources <https://www.python.org/about/gettingstarted/>`_

.. _dev-env:

Development environment
-----------------------

1. First and foremost, please see the suggested IDE setup in the dropdown below to make sure that your editor is ready for development.

.. important::
   **Suggested IDE setup**

   VS Code

   Install the following extensions:

   * `charliermarsh.ruff <https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff>`_
   * `streetsidesoftware.code-spell-checker <https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker>`_

2. `Fork <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`_ the `i18n-check repo <https://github.com/activist-org/i18n-check>`_, clone your fork, and configure the remotes:

.. note::
   **Consider using SSH**

   Alternatively to using HTTPS as in the instructions below, consider SSH to interact with GitHub from the terminal. SSH allows you to connect without a user-pass authentication flow.

   To run git commands with SSH, remember then to substitute the HTTPS URL, ``https://github.com/...``, with the SSH one, ``git@github.com:...``.

   * e.g. Cloning now becomes ``git clone git@github.com:<your-username>/i18n-check.git``

   GitHub also has their documentation on how to `Generate a new SSH key <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_ 🔑

.. code-block:: bash

    # Clone your fork of the repo into the current directory.
    git clone https://github.com/<your-username>/i18n-check.git
    # Navigate to the newly cloned directory.
    cd i18n-check
    # Assign the original repo to a remote called "upstream".
    git remote add upstream https://github.com/activist-org/i18n-check.git

* Now, if you run ``git remote -v`` you should see two remote repositories named:
    * ``origin`` (forked repository)
    * ``upstream`` (``i18n-check`` repository)

3. Create a virtual environment for i18n-check (Python ``>=3.12``), activate it and install dependencies:

.. note::
   First, install ``uv`` if you don't already have it by following the `official installation guide <https://docs.astral.sh/uv/getting-started/installation/>`_.

.. code-block:: bash

    uv sync --all-extras  # create .venv and install all dependencies from uv.lock

    # Unix or macOS:
    source .venv/bin/activate

    # Windows:
    .venv\Scripts\activate.bat # .venv\Scripts\activate.ps1 (PowerShell)

After activating the virtual environment, set up `pre-commit <https://pre-commit.com/>`_ by running:

.. code-block:: bash

    pre-commit install
    # uv run pre-commit run --all-files  # lint and fix common problems in the codebase

.. note::
   If you change dependencies in ``pyproject.toml``, regenerate the lock file with the following command:

   .. code-block:: bash

      uv lock  # refresh uv.lock for reproducible installs

You're now ready to work on ``i18n-check``!

.. note::
   Feel free to contact the team in the `Development room on Matrix <https://matrix.to/#/!CRgLpGeOBNwxYCtqmK:matrix.org?via=matrix.org&via=acter.global&via=chat.0x7cd.xyz>`_ if you're having problems getting your environment setup!



.. _linting:

Linting
-------

`Ruff <https://github.com/astral-sh/ruff>`_ is installed via the required packages to assure that errors are reported correctly. We'd also suggest that VS Code users install the `Ruff extension <https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff>`_.

.. _testing:

Testing
-------

Please run the following commands from the project root to test:

.. code-block:: bash

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

.. _issues-projects:

Issues and projects
-------------------

The `issue tracker for i18n-check <https://github.com/activist-org/i18n-check/issues>`_ is the preferred channel for `Bug reports`_, `Feature requests`_ and `Pull requests`_. The activist community also organizes related issues into `projects <https://github.com/activist-org/i18n-check/projects>`_.

.. _bug-reports:

Bug reports
-----------

A bug is a *demonstrable problem* that is caused by the code in the repository. Good bug reports are extremely helpful — thank you!

Guidelines for bug reports:

1. **Use the GitHub issue search** to check if the issue has already been reported.

2. **Check if the issue has been fixed** by trying to reproduce it using the latest ``main`` or development branch in the repository.

3. **Isolate the problem** to make sure that the code in the repository is *definitely* responsible for the issue.

**Great Bug Reports** tend to have:

* A quick summary
* Steps to reproduce
* What you expected would happen
* What actually happens
* Notes (why this might be happening, things tried that didn't work, etc)

To make the above steps easier, the ``i18n-check`` team asks that contributors report bugs using the `bug report template <https://github.com/activist-org/i18n-check/issues/new?assignees=&labels=bug&projects=activist-org%2F1&template=bug_report.yml>`_, with these issues further being marked with the `Bug <https://github.com/activist-org/i18n-check/issues?q=is%3Aissue%20state%3Aopen%20type%3ABug>`_ type.

Again, thank you for your time in reporting issues!

.. _feature-requests:

Feature requests
----------------

Feature requests are more than welcome! Please take a moment to find out whether your idea fits with the scope and aims of the project. When making a suggestion, provide as much detail and context as possible, and further make clear the degree to which you would like to contribute in its development. Feature requests are marked with the `Feature <https://github.com/activist-org/i18n-check/issues?q=is%3Aissue%20state%3Aopen%20type%3AFeature>`_ type in the `issues <https://github.com/activist-org/i18n-check/issues>`_.

.. _pull-requests:

Pull requests
-------------

Good pull requests — patches, improvements and new features — are the foundation of our community making ``i18n-check``. They should remain focused in scope and avoid containing unrelated commits. Note that all contributions to this project will be made under `the specified license <LICENSE.txt>`_ and should follow the coding indentation and style standards (contact us if unsure).

**Please ask first** before embarking on any significant pull request (implementing features, refactoring code, etc), otherwise you risk spending a lot of time working on something that the developers might not want to merge into the project. With that being said, major additions are very appreciated!

When making a contribution, adhering to the `GitHub flow <https://docs.github.com/en/get-started/quickstart/github-flow>`_ process is the best way to get your work merged:

1. If you cloned a while ago, get the latest changes from upstream:

   .. code-block:: bash

       git checkout <dev-branch>
       git pull upstream <dev-branch>

2. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix:

   .. code-block:: bash

       git checkout -b <topic-branch-name>

3. Install `pre-commit <https://pre-commit.com/>`_ to ensure that each of your commits is properly checked against our linter and formatters:

   .. code-block:: bash

       # In the project root:
       pre-commit install

       # Then test the pre-commit hooks to see how it works:
       # uv run pre-commit run --all-files

.. note::
   pre-commit is Python package that can be installed via pip or any other Python package manager. You can also find it in our `uv.lock <./uv.lock>`_ file.

   .. code-block:: bash

       pip install pre-commit

.. note::
   If you are having issues with pre-commit and want to send along your changes regardless, you can ignore the pre-commit hooks via the following:

   .. code-block:: bash

       git commit --no-verify -m "COMMIT_MESSAGE"

4. Commit your changes in logical chunks, and please try to adhere to `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`_.

.. note::
   The following are tools and methods to help you write good commit messages ✨

   * `commitlint <https://commitlint.io/>`_ helps write `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`_
   * Git's `interactive rebase <https://docs.github.com/en/github/getting-started-with-github/about-git-rebase>`_ cleans up commits

5. Locally merge (or rebase) the upstream development branch into your topic branch:

   .. code-block:: bash

       git pull --rebase upstream <dev-branch>

6. Push your topic branch up to your fork:

   .. code-block:: bash

       git push origin <topic-branch-name>

7. `Open a Pull Request <https://help.github.com/articles/using-pull-requests/>`_ with a clear title and description.

Thank you in advance for your contributions!

.. _documentation:

Documentation
-------------

The documentation for ``i18n-check`` can be found at `i18n-check.readthedocs.io <https://i18n-check.readthedocs.io/en/latest/>`_. Documentation is an invaluable way to contribute to coding projects as it allows others to more easily understand the project structure and contribute. Issues related to documentation are marked with the `documentation <https://github.com/activist-org/i18n-check/labels/documentation>`_ label.

Function Docstrings
~~~~~~~~~~~~~~~~~~~

``i18n-check`` generally follows `numpydoc conventions <https://numpydoc.readthedocs.io/en/latest/format.html>`_ for documenting functions and Python code in general. Function docstrings should have the following format:

.. code-block:: python

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

Building the Docs
~~~~~~~~~~~~~~~~~

Use the following commands to build the documentation locally:

.. code-block:: bash

    cd docs
    make html

You can then open ``index.html`` within ``docs/build/html`` to check the local version of the documentation.
