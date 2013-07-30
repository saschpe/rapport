Rapport: Work report generator for the lazy
===========================================

.. image:: https://travis-ci.org/saschpe/rapport.png?branch=master
        :target: https://travis-ci.org/saschpe/rapport

.. image:: https://pypip.in/d/rapport/badge.png
        :target: https://pypi.python.org/pypi/rapport

.. image:: https://pypip.in/v/rapport/badge.png
        :target: https://pypi.python.org/pypi/rapport

Writing work reports is tedious. Some people have custom hacks. This is meant
to be the last one. It's Apache-2.0 licensed and written in Python, not
VimScript, not Bash, not Ruby, not C, ..., you probably got it ;-)


Features
--------

- Asynchronously collects data from various resources:

  - Bugzilla
  - Gerrit
  - Github
  - Launchpad
  - MediaWiki
  - OpenBuildService
  - Trello
  - Twitter

- Supports plugins for extendability
- Simple ini-style config file
- (Almost) comprehensive unit and functional testsuite
- Supports creating work reports for arbitrary timeframes and provides some convenient ones:

  - Current week / month
  - Recent days
  - Week / month of of year
  - Generic


Installation
------------

To install rapport from the `Python Package Index`_, simply:

.. code-block:: bash

    $ pip install rapport

Or, if you absolutely must:

.. code-block:: bash

    $ easy_install rapport

But, you really shouldn't do that. Lastly, you can check your distro of choice
if they provide packages. For openSUSE, you can find packages in the `Open
Build Service`_ for all releases. If you happen to use openSUSE:Factory (the
rolling release / development version), simply:

.. code-block:: bash

    $ sudo zypper install rapport


Usage
-----

Rapport allows to query various upstream resources for modifications you made.
So before creating your first work report, you should check rapport's config
file and add your credentials to the resources you are interested in.

.. TODO: Explain configuration

By default, rapport creates a work report for the current weak, so from Monday
until *now* (And yes, i18n and i10n are on the TODO list). You can also set the
timeframe to consider explicitly. For instance, you could generate a work
report for the last 10 days:

.. code-block:: bash

    $ rapport create --recent-days 10

Check the help of the *create* command for other options:

.. code-block:: bash

    $ rapport create --help

You can show a list of all previous work reports:

.. code-block:: bash

    $ rapport list

And display details for a specific work report:

.. code-block:: bash

    $ rapport show 2013-05-21T09:27:43

Or display the latest work report by:

.. code-block:: bash

    $ rapport show

If you need further assistance, check rapport's help:

.. code-block:: bash

    $ rapport help


Hacking and contributing
------------------------

You can test rapport from your git checkout by executing the rapport.cli module:

.. code-block:: bash

    $ python -m rapport.cli

Alternatively, you can invoke the convenience script wrapper:

.. code-block:: bash

    $ ./scripts/rapport

Fork `the repository`_ on Github to start making your changes to the **master**
branch (or branch off of it). Don't forget to write a test for fixed issues or
implemented features whenever appropriate. You can invoke the testsuite from
the repository root directory via:

.. code-block:: bash

    $ python setup.py test

Or by running `nose`_ directly:

.. code-block:: bash

    $ nosetests

Both assume you have the test dependencies installed (available on PYTHONPATH)
on your system. If that doesn't work for you, you can create a `virtual
environment`_ instead:

.. code-block:: bash

    $ virtualenv .venv
    $ source .venv/bin/activate
    (.venv)$ pip install -r test-requirements.txt 
    (.venv)$ nosetests

Lastly, if using virtualenv is too tedious or you want to test different
configurations (py26, py27, py33, pep8), you can also use `tox`_:

.. code-block:: bash

    $ tox



.. _`Python Package Index`: https://pypi.python.org/pypi/rapport
.. _`Open Build Service`: https://build.opensuse.org/package/show?package=rapport&project=devel:languages:python
.. _`the repository`: https://github.com/saschpe/rapport
.. _`nose`: https://nose.readthedocs.org
.. _`virtual environment`: http://www.virtualenv.org
.. _`tox`: http://testrun.org/tox
