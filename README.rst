=============
pytest-bandit
=============

.. image:: https://img.shields.io/pypi/v/pytest-bandit.svg
    :target: https://pypi.org/project/pytest-bandit
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-bandit.svg
    :target: https://pypi.org/project/pytest-bandit
    :alt: Python versions

.. image:: https://travis-ci.org/Wanderu/pytest-bandit.svg?branch=master
    :target: https://travis-ci.org/Wanderu/pytest-bandit
    :alt: See Build Status on Travis CI

A bandit plugin for pytest

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* Execute `bandit`_ testing against a repository


Requirements
------------

* Bandit > 1.4.0


Installation
------------

You can install "pytest-bandit" via `pip`_ from `PyPI`_::

    $ pip install pytest-bandit


Usage
-----

* add `bandit_targets` to your pytest configuration and add at least one directory to traverse
* you probably want `bandit_recurse = true` in your configuration as well

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-bandit" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/Wanderu/pytest-bandit/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`bandit`: https://github.com/PyCQA/bandit
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
