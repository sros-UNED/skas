========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/skas/badge/?style=flat
    :target: https://readthedocs.org/projects/skas
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/postdataproject/skas.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/postdataproject/skas

.. |requires| image:: https://requires.io/github/postdataproject/skas/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/postdataproject/skas/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/postdataproject/skas/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/postdataproject/skas

.. |codecov| image:: https://codecov.io/github/postdataproject/skas/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/postdataproject/skas

.. |version| image:: https://img.shields.io/pypi/v/skas.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/skas

.. |commits-since| image:: https://img.shields.io/github/commits-since/postdataproject/skas/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/postdataproject/skas/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/skas.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/skas

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/skas.svg
    :alt: Supported versions
    :target: https://pypi.org/project/skas

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/skas.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/skas


.. end-badges

Scansion tool for Spanish texts

* Free software: Apache Software License 2.0

Installation
============

::

    pip install skas

Documentation
=============


https://skas.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
