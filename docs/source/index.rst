.. image:: https://raw.githubusercontent.com/activist-org/i18n-check/main/.github/resources/i18nCheckGitHubBanner.png
    :width: 100%
    :align: center
    :target: https://github.com/activist-org/i18n-check

|rtd| |issues| |language| |pypi| |pypistatus| |license| |coc| |matrix|

.. |rtd| image:: https://img.shields.io/readthedocs/i18n-check.svg?label=%20&logo=read-the-docs&logoColor=ffffff
    :target: http://i18n-check.readthedocs.io/en/latest/

.. |issues| image:: https://img.shields.io/github/issues/activist-org/i18n-check?label=%20&logo=github
    :target: https://github.com/activist-org/i18n-check/issues

.. |language| image:: https://img.shields.io/badge/Python%203-306998.svg?logo=python&logoColor=ffffff
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

Installation
============

i18n-check is available for installation via `pip <https://pypi.org/project/i18n-check/>`_:

.. code-block:: shell

    pip install i18n-check

The latest development version can further be installed the `source code on GitHub <https://github.com/activist-org/i18n-check>`_:

.. code-block:: shell

    git clone https://github.com/activist-org/i18n-check.git
    cd i18n-check
    pip install -e .

To utilize the i18n-check CLI, you can execute variations of the following command in your terminal:

.. code-block:: shell

    i18n-check -h  # view the cli options
    i18n-check [command]

Commands
========

The following are example commands for `i18n-check`:

.. code-block:: shell

    i18n-check -gtf  # generate a test frontends to see how it works
    i18n-check -a  # run all checks
    # Available IDs are ki, ik, uk, nsk, rk, rv and nk.
    i18n-check -CHECK_ID  # run a specific check

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
